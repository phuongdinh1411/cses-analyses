---
layout: simple
title: "Networking Essentials — System Design School"
permalink: /system_design/sds/concepts/tech-networking
---

System Design School

- Learn

- Practice

- Primer

- Roadmap

- Pricing

Ask AI TutorStart learning

System Design Primer12

★The TemplateIntroductionWhat Is System Design?What Are System Design Interviews?Level Expectations

Show all 12 →

Design Solutions35

LeetCode (Online Judge)Typeahead / AutocompleteDistributed Rate LimiterTicketmasterNews Feed

Show all 35 →

AI System Design6

RAG SystemChatGPTImage Generation ServiceCoding Agent CLI (Claude Code)

Show all 6 →

Patterns5

The 10 PatternsScaling Reads & WritesAsynchronous JobsReal-Time Transport

Show all 5 →

Key Technologies5

Networking EssentialsTechnology ChoicesRedisTries & Prefix SearchFail-Open vs Fail-Closed

# Networking Essentials: DNS, TCP/UDP, HTTP, and Load Balancing

mediumNetworkingLoad balancingDNS

Between a browser and your service sits a chain of networking systems, and each one drives a design decision. A request resolves a name to an address, opens a connection, encrypts itself, routes to the right server pool, and crosses a physical distance. DNS, TCP, TLS, load balancing, and latency are those hops.

Interviewers rarely ask you to explain DNS outright. They ask you to walk a request from the browser to your service, and the networking surfaces in the seams: where TLS terminates, why a live-video feature picks a different protocol, which load-balancer layer routes by path.

## The path of one request

Follow a single request from browser to server. Four hops matter, and each is owned by a different concept.

First the browser turns the hostname into a numeric address (DNS). Then it opens a transport connection and secures it (TCP and TLS carrying HTTP). The connection lands at a load balancer, which decides which server pool should handle it (L4 or L7 routing). Finally the request reaches an app server and the response travels the whole distance back (latency). Each hop below is framed by the choice it forces.

## DNS: turning a name into an address

Computers route by numeric IP address, not by name. The Domain Name System (DNS) is the lookup that converts a hostname like api.example.com into an address the network can reach. It is the internet's phone book: you know the name, DNS returns the number.

The lookup is cached at several layers so it rarely runs in full. The browser caches recent answers, the operating system caches below it, and shared resolvers cache for many users at once. Each cached answer skips the round trips to authoritative servers. A record's time-to-live (TTL) controls how long a cache may keep it.

TTL (time-to-live). A DNS record carries a number of seconds it stays valid. A low TTL, such as 60 seconds, lets you redirect traffic quickly during a failover but sends more lookups. A high TTL cuts lookups but makes changes propagate slowly.

The design decision DNS drives is geo-routing. DNS can hand different users different addresses based on where they are. A user in Europe resolves the hostname to a European data center; a user in Asia resolves the same hostname to an Asian one. This routing happens before any request reaches your servers, which makes DNS the first place to steer traffic toward the nearest region.

## TCP vs UDP: reliability or speed

Once the browser has an address, it needs a transport protocol to carry bytes there. Two dominate, and they sit at opposite ends of a trade-off between reliability and latency.

TCP (Transmission Control Protocol) sets up a connection with a handshake, then guarantees delivery. Every byte arrives, in order, and lost packets are resent. This is what normal APIs use, because a truncated JSON response or an out-of-order database write is a bug. The cost is the handshake before data flows and the wait when a lost packet must be resent.

UDP (User Datagram Protocol) sends packets with no connection setup and no delivery guarantee. Packets can arrive out of order, or not at all, and nothing is resent. That sounds worse until the workload is live media. In a video call, a packet that arrives late is useless: the moment it describes has already passed. Resending it would only delay the frames behind it. UDP drops the straggler and keeps moving, which is why live video, voice, and multiplayer games prefer it.

The choice comes down to what a late byte is worth. If every byte must arrive and order matters, use TCP. If freshness beats completeness and a dropped packet is cheaper than a delayed one, use UDP. Real-time features lean on this trade-off, covered further in Real-Time Transport.

## HTTP and HTTPS: the request and its encryption

HTTP is the request-response format that rides on top of TCP. The client sends a method, a path, and headers; the server returns a status code and a body. It is stateless: each request stands on its own, which is what lets any server in a pool handle any request.

HTTPS is HTTP wrapped in TLS (Transport Layer Security), the encryption layer that protects data in transit. Setting up a secure connection stacks two handshakes: TCP first to open the connection, then TLS to negotiate keys, before any HTTP data flows. That setup cost is why connection reuse matters later.

The design decision here is where TLS terminates. Decrypting TLS costs CPU, and doing it on every app server means every server needs certificates and spends cycles on cryptography. Instead, TLS usually terminates at the edge: the load balancer decrypts once, then talks to app servers over plain HTTP inside the trusted network.

This centralizes certificate management in one place and keeps decryption off the app servers. The internal network is treated as trusted, so plain HTTP between the load balancer and the app tier is an accepted trade in most designs.

## L4 vs L7 load balancing: how deep it looks

The load balancer spreads traffic across a pool of servers so no single one is overwhelmed. It can make that decision at two depths, named for layers of the network stack, and the depth changes what routing is possible. (For the full treatment, see Load Balancer.)

A Layer 4 (L4) load balancer routes on addresses and ports alone. It sees a connection, not its contents, and forwards it to a server. Because it never reads the request, it is fast and cheap, but it cannot make decisions based on what the request asks for.

A Layer 7 (L7) load balancer reads the HTTP request itself: the path, the host, the headers. That lets it route by content. Requests for /images/* can go to one pool and /api/* to another, or different hostnames can map to different services. It is also the natural place to terminate TLS, since it already parses the request. The cost is more work per request than L4.

The decision is whether routing needs to know what the request contains. Pure connection spreading at high throughput favors L4. Path-based or host-based routing, or TLS termination at the edge, requires L7.

Design checkpoint

Your design sends /api/* to an application pool and /static/* to a pool serving images. The load balancer must pick the pool from the URL path. Which layer do you need?

L4, because it is faster and cheaperL7, because path-based routing requires reading the requestEither works; the layer does not affect routing

## Latency: the cost of distance and round trips

Every request is at least one round trip: out to the server and back. Signals travel at a finite speed, so distance sets a floor on latency that no amount of server tuning removes. A round trip across a continent costs far more than one across a data center.

Two techniques cut this cost, and both appear constantly in designs. The first is connection reuse. Opening a new HTTPS connection pays for the TCP handshake and then the TLS handshake before data moves. Keeping the connection alive and sending many requests over it (keep-alive) pays that setup once instead of per request. The second is moving data closer to users. A content delivery network (CDN) caches copies at locations near users, so a static asset is served from a nearby edge rather than the origin across the world. Both attack the same enemy: the round trip.

Round trip time (RTT). The time for a request to reach the server and the response to return. It is bounded below by physical distance and the speed of light in fiber. Reducing round trips, or shortening their distance, is often the largest latency win available.

Latency reasoning is what turns a component list into a defensible design. It justifies the CDN, the keep-alive connections, and the DNS geo-routing that put users on a nearby region in the first place. For the full model, see Latency; for edge caching, CDN vs Application Cache.

## What a strong answer sounds like

Walk me through what happens when a user hits your API.

BadThe request just reaches the server▾

GoodName the hops in order▾

GreatName each hop and the decision it drives▾

## The transferable pattern

Networking questions reduce to one habit: trace the request end to end and name the decision at each hop. Distance and round trips set the latency floor, so push work and data toward the user with geo-routing and CDNs. Encryption costs CPU, so terminate TLS once at the edge. Routing intelligence costs processing, so pick L4 for blind speed and L7 when the request's content must steer it. Protocol choice follows the value of a late byte: TCP when every byte must arrive, UDP when freshness beats completeness. The same trace works for any system; only the hops you emphasize change.

Key idea. Trace one request from browser to server and name the decision each hop forces: DNS for locality, TCP or UDP for the value of a late byte, TLS termination for encryption cost, L4 or L7 for routing depth, and round trips for latency.

## Sources and further reading

- What is DNS? — Cloudflare Learning Center — how name resolution, resolvers, and caching work, with the phone-book model.

- An overview of HTTP — MDN — the request-response model, methods, status codes, and statelessness.

- How Elastic Load Balancing works — AWS — L4 (Network) vs L7 (Application) load balancers and when each applies.

Explain

Add to Chat

The System Design Courses

Go beyond memorizing solutions to specific problems. Learn the core concepts, patterns and templates to solve any problem.

Start Learning

Was this lesson clear?

👍👎

### How to Solve Any System Design Interview

#### Comments

Join the Discussion

The System Design Courses

Go beyond memorizing solutions to specific problems. Learn the core concepts, patterns and templates to solve any problem.

Start Learning

On this page

The path of one requestDNS: turning a name into an addressTCP vs UDP: reliability or speedHTTP and HTTPS: the request and its encryptionL4 vs L7 load balancing: how deep it looksLatency: the cost of distance and round tripsWhat a strong answer sounds likeThe transferable patternSources and further reading

Read0%

Need help?Ask about this section

On this pageThe path of one request0%

Send feedback
