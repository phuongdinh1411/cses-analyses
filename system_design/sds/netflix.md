---
layout: simple
title: "Design Netflix — System Design School"
permalink: /system_design/sds/netflix
---

# Design Netflix

**Difficulty:** Medium  
**Topics:** Video streaming · CDN & delivery economics · Adaptive bitrate · Pre-positioning · Object storage · Async processing

## Summary

- **Key challenge:** Serve terabits per second of egress to tens of millions of concurrent viewers; no origin can, so almost every byte must come from a nearby cache.
- **Core design:** Studio masters are transcoded offline into an encoding ladder, sliced into short segments listed in a manifest; players fetch segments over HTTP from edge caches into a buffer.
- **Techniques:** encoding ladder for every device/network; segments + HLS/DASH manifest as cacheable units; client-side ABR to avoid rebuffering; efficient codecs to cut egress; pre-positioning predictable popular titles at the edge.

## Problem statement

Design a service that streams a curated catalog of movies and shows to a global audience, smoothly, on any device and any connection. A studio delivers a high-quality master file for each title; the service transcodes it, stores it, and plays it back on demand. Viewers expect playback to start within a second or two, to stay smooth as bandwidth changes, to seek anywhere in a title, and to resume on a television where they left off on a phone.

The scope here is ingest and delivery: taking a master and making it watchable, then serving it at scale. Home-page ranking and search are a separate recommendation problem; billing is a separate payment problem; the internals of digital rights management (DRM) are named where they touch delivery and otherwise deferred.

## Clarifying questions

Each question below fixes an assumption the rest of the design leans on.

- Video-on-demand or live? Video-on-demand (VOD) serves pre-recorded files transcoded ahead of time. Live transcodes in real time under tight latency and is a different system, covered as a variant. Assume VOD.

- User-generated or a curated catalog? Curated and licensed. Studios deliver a high-quality master (also called a mezzanine file), so there is no upload firehose, transcoding runs offline and unhurried, and — the load-bearing point — which titles will be popular is predictable in advance.

- Global? Yes, and it is central. Viewers are worldwide, so per-region storage and caches placed close to users are first-order concerns from the start.

- Recommendations and search in scope? Deferred as a separate ranking-and-retrieval problem. Assume a catalog browse exists; focus on ingest and delivery.

- Billing, profiles, DRM? Billing is the payment-system problem. DRM (encrypting segments, issuing license keys) is real and named where it interacts with caching, its internals deferred. Profiles are a light per-user layer.

- What sizes the system? Peak concurrent-stream egress bandwidth. The catalog is large but bounded; both the cost and the engineering live in moving bytes to viewers.

## What makes this problem distinctive

A basic answer stores each title and streams the bytes back from a server. Two forces break that, and the second determines the delivery architecture.

The first is that one file cannot play everywhere. A phone on a weak cellular signal and a television on fiber cannot share a single encoding, so each title becomes an encoding ladder — the same video at many resolutions and bitrates — sliced into short segments a player switches between second by second. This part Netflix shares with any video platform.

The second force dominates: delivery economics. Streaming to tens of millions of concurrent viewers is an egress-bandwidth problem measured in terabits per second, and a single origin cannot serve that, so almost every byte must come from a cache near the viewer. What sets this problem apart from a general video platform is a lever it can use to reach that hit rate: the catalog is finite, and which titles will be popular is predictable in advance. A platform flooded with unpredictable user uploads has no such foresight; a licensed catalog does. How the design turns that predictability into a near-complete hit rate is worked out in the high-level design.

Ingress and egress. Ingress is data entering the system — here, the studio masters, a modest trickle. Egress is data leaving it — the bytes streamed to viewers. For a streaming service egress dwarfs ingress by orders of magnitude, because a small catalog is watched an enormous number of times. Egress is the quantity that shapes the design.

The tension the whole design resolves: every byte served from the origin costs origin bandwidth the system cannot afford, yet a byte can only be served from the edge if it is already there. The diagram shows the forces, not the answer.

Key idea. Netflix's defining trait is delivery economics, and its defining lever is a predictable catalog that can be pushed to the edge before demand arrives.

## Key concepts

This section covers the concepts needed to solve this problem — prerequisites for the design work that follows. These are the streaming fundamentals the later sections assume as known vocabulary; they are reviewed here directly rather than derived from a failure.

Playback is a client-driven loop. The player downloads a small manifest listing the available qualities and the URLs of the segments that make up the video, then fetches segments a few seconds at a time into a buffer — a short queue of already-downloaded video waiting to play. It plays from the buffer while downloading ahead, so a brief network dip drains the buffer instead of stalling, and at each segment boundary the player can switch quality. The widget shows the loop.

Play Restartidle

manifest .m3u8

→lists 20 segments

segments — played, buffered ahead, not yet downloaded

Buffer ahead

0.0 segments

Network (download speed)

Playback (the line) drains the buffer at a steady rate; downloads refill it. When the network drops below the playback rate, the buffer shrinks — and if it empties, playback has to pause and rebuffer.

### Rendition

A rendition is the same title encoded at one resolution and bitrate — a single rung of the ladder. A lower bitrate means a smaller file and lower quality; a higher bitrate means better quality and more bytes to move. Because every byte moved is an egress cost multiplied across millions of streams, the bitrate of each rung is not a cosmetic choice — it is the cost knob.

Reading bitrate. Bitrate is measured in megabits per second (Mbps) — the rate at which the stream delivers data. Eight bits make a byte, so 5 Mbps is about 0.6 MB per second. To play without stalling, the connection must sustain at least the rendition's bitrate.

Bitrate3.0 Mbps

Size for a 10-min clip

225 MB

Typical use

1080p / broadband

### Codec

A codec compresses each rendition. It stores one full keyframe and then only the differences between frames, which is where the compression comes from. A more efficient codec reaches the same quality at a lower bitrate — and lower bitrate at equal quality is a permanent egress saving, so codec choice trades encoding CPU for delivery cost.

keyframe + deltasevery frame full

1 · I-frame

2 · delta

3 · delta

4 · delta

5 · delta

6 · delta

10

2

2

2

2

2

Bar heights are illustrative: a delta frame stores only what changed, so it costs far less than a full keyframe. Real ratios depend on motion in the footage.

### Encoding ladder

The encoding ladder is the set of renditions produced from one master — for example 240p through 4K, one rung per device and network class. The same title exists at every rung, so the player can drop to a lower quality when the connection can sustain one of the available rungs.

source master

4K H.265

240p

0.4 Mbps

slow mobile

480p

1.2 Mbps

3G phone

720p

2.5 Mbps

4G tablet

1080p

4.5 Mbps

laptop / broadband

4K

16 Mbps

TV / fiber

### Segments and the manifest

A rendition is not fetched as one file. Each is divided into short segments of a few seconds — the unit that is requested and cached. A manifest lists the renditions and, per rendition, the ordered segment URLs. Two manifest formats dominate: HLS (HTTP Live Streaming, Apple's .m3u8) and DASH (Dynamic Adaptive Streaming over HTTP, the open .mpd standard); both follow the same manifest-plus-segments model. The player reads the manifest and fetches segments in order.

Play RestartA rendition is one long file.

1080p rendition, sliced into ~4s segments

s1

s2

s3

s4

s5

s6

s7

s8

s9

s10

manifest · index.m3u8

#EXTM3U

seg1.ts

seg2.ts

seg3.ts

seg4.ts

seg5.ts

seg6.ts

seg7.ts

seg8.ts

seg9.ts

seg10.ts

player

idle

buffer: 0 segments

### Adaptive bitrate (ABR)

The player, not the server, selects the quality. It measures available bandwidth and buffer level and, at each segment boundary, requests the next segment at the highest rung it can sustain — stepping down when the signal weakens and back up when it recovers. The server serves plain cacheable segments and holds no per-viewer state, which is what lets a cache absorb nearly all the traffic.

Play RestartPress play

1

2

3

4

5

6

7

8

9

10

11

12

13

14

15

16

1080p720p480p240p

### Rebuffering

If the buffer empties, playback stalls until new data arrives — a rebuffer, the spinning-wheel pause. It happens when the network cannot deliver the chosen quality fast enough. Preventing it is why ABR exists: in the widget, a fixed high-quality stream stalls during a bandwidth dip, while adaptive mode drops to a lower rung the network can sustain and keeps playing. Viewers tolerate a brief quality drop far better than a stall.

fixed 1080padaptive (ABR)

Play Restart

Bandwidth

8.0 Mbps

Quality

1080p

Buffer

0.0 s

idlerebuffers: 0

Key idea. Playback is a client-driven loop — read the manifest, fill a buffer, switch rendition per segment — and every rung's bitrate is an egress cost.

## Grasping the building blocks ("the lego pieces")

This part of the guide will focus on the various components that are often used to construct a system (the building blocks), and the design templates that provide a framework for structuring these blocks.

### Core Building blocks

At the bare minimum you should know the core building blocks of system design

- Scaling stateless services with load balancing

- Scaling database reads with replication and caching

- Scaling database writes with partition (aka sharding)

- Scaling data flow with message queues

### System Design Template

With these building blocks, you will be able to apply our template to solve many system design problems. We will dive into the details in the Design Template section. Here’s a sneak peak:

### Additional Building Blocks

Additionally, you will want to understand these concepts

- Processing large amount of data (aka “big data”) with batch and stream processing

- Particularly useful for solving data-intensive problems such as designing an analytics app

- Achieving consistency across services using distribution transaction or event sourcing

- Particularly useful for solving problems that require strict transactions such as designing financial apps

- Full text search: full-text index

- Storing data for the long term: data warehousing

On top of these, there are ad hoc knowledge you would want to know tailored to certain problems. For example, geohashing for designing location-based services like Yelp or Uber, operational transform to solve problems like designing Google Doc. You can learn these these on a case-by-case basis. System design interviews are supposed to test your general design skills and not specific knowledge.

## Working through problems and building solutions using the building blocks

Finally, we have a series of practical problems for you to work through. You can find the problem in /problems. This hands-on practice will not only help you apply the principles learned but will also enhance your understanding of how to use the building blocks to construct effective solutions. The list of questions grow. We are actively adding more questions to the list.

*(The rest of this article is behind a login on the source site.)*
