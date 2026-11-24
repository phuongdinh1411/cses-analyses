---
layout: simple
title: "Handling Large Files Pattern — System Design School"
permalink: /system_design/sds/concepts/patterns-large-files
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

The 10 PatternsScaling Reads & WritesAsynchronous JobsReal-Time TransportHandling Large Files

Key Technologies5

Networking EssentialsTechnology ChoicesRedisTries & Prefix Search

Show all 5 →

# Handling Large Files: Object Storage, Presigned URLs, and CDNs

mediumObject storagePresigned URLsCDN

Large files strain a design in ways ordinary records do not. Take a 2GB video sent as a normal POST to an application server that then stores it. That path breaks three ways at once.

First, the app server must hold the upload in memory or a temp file while it streams in, so a few concurrent 2GB uploads exhaust one instance's memory and bandwidth. Second, the request runs for minutes, past most gateway and proxy timeouts, and a dropped connection near the end wastes the whole transfer. Third, storing the bytes in a database column means every backup, table scan, and cache now drags gigabytes of binary data that no query ever filters on.

## The core split: bytes in object storage, pointer in the database

A database is built for small structured rows, not multi-gigabyte blobs. The fix is to separate the two concerns. The raw bytes go into object storage, a flat store built to hold large objects cheaply and durably. The database keeps only a small row that points to the object.

Object key. The identifier for one object in the store, like a file path: uploads/2026/u42/a8f3c1.mp4. The database row holds this string, not the bytes. Reading the file means fetching the object by its key.

The metadata row stays tiny no matter how large the file. It carries the owner, the object key, the content type, the byte size, and a status such as pending, processing, or ready. A query like "list this user's videos, newest first" scans small rows and never touches the blobs.

The dotted line is the whole idea: the small row in the database references the large object by key, and the bytes never live in the database. This split is why the database stays fast while files grow without bound.

## Uploads: split the file into parts

A single 2GB upload is fragile. One network blip at 90% forces the client to start over. Object stores solve this with multipart upload: the client splits the file into parts and uploads each part on its own.

The store accepts parts independently, then reassembles them into one object after a final "complete" call. A failed part is retried alone, not the whole file. Parts can upload in parallel to use more bandwidth, and the transfer can pause and resume across network changes. For a deeper treatment of splitting files this way, see File Chunking.

Multipart carries overhead: a start call, one call per part, and a complete call. That cost only pays off above a deliberate size threshold. A 200KB avatar goes up in a single PUT; a 2GB video is worth chunking. The threshold is a design choice, not a fixed number.

## Presigned URLs: the client uploads directly to storage

Splitting the file helps, but the bytes still should not pass through the app server. The mechanism that keeps them off it is the presigned URL.

Presigned URL. A URL the app server generates by signing a specific request with its storage credentials. The signature encodes one operation on one object key, and an expiry a few minutes out. The object store trusts the signature, so the holder can perform exactly that operation without any credentials of its own.

The flow inverts the naive upload. The client asks the app server for permission to upload. The server checks authorization, writes a pending metadata row, and returns a presigned URL that grants a PUT to one object key. The client uploads the bytes straight to object storage using that URL. When the upload finishes, the client tells the app server, which flips the row to ready.

The app server touches two small messages and never the 2GB payload. Its memory, bandwidth, and request timeouts stop scaling with file size. For multipart, the same idea repeats per part: the server hands out one presigned URL for each part, and the client uploads them directly. Worked examples of this exact path appear in the Dropbox and YouTube solutions.

Design checkpoint

You route a 2GB upload through your app server. What breaks, and how do you keep the bytes off it?

Add more app servers and raise the request timeoutCompress the file before uploadHand the client a presigned URL so it uploads straight to object storage

## Serving: CDN for public media, signed URLs for private

Downloads split by access. Public media, like profile photos and product images, is read far more than written and often from around the world. Serving every read from the origin store means repeated long-distance fetches for the same bytes.

A content delivery network (CDN) caches these objects at edge locations near users. The first request pulls from the origin; later requests for the same object are served from a nearby edge. The metadata row's object key maps to the CDN URL, so origin load stays low as reads climb.

Private content, like tax documents or paid downloads, cannot be openly cacheable. Here the app server runs its permission check, then returns a short-lived presigned download URL, the read-side mirror of the upload URL. It grants a GET on one object for a few minutes, so a leaked link stops working after it expires. Access lives in the server's authorization logic, not in whoever holds the link.

## What a strong answer sounds like

A user uploads a 2GB video. Design the upload path.

BadPOST the whole file to the app server▾

GoodObject storage plus direct presigned upload▾

GreatAdd multipart, metadata status, CDN, and signed reads▾

## The transferable pattern

Any system moving large blobs follows this shape. Keep the bytes out of the database; store them in an object store and hold a small pointer row. Keep the bytes out of your app servers; issue a presigned URL and let the client and store move the data directly. Make the transfer resumable by splitting it into independently retried parts. Serve reads from a CDN when the content is public, and from short-lived signed URLs when it is private. Video platforms, file sync, backups, and image hosting all reduce to these four moves.

The bytes and the metadata then travel separate paths, which lets each scale on its own terms: cheap durable storage for the blobs, a fast small database for the queries.

Key idea. The bytes belong in object storage and the pointer in the database, and a presigned URL keeps the file off your servers so the client uploads straight to storage.

## Sources and further reading

- Uploading and copying objects using multipart upload — AWS S3 docs — how a large object is split into parts, uploaded independently, and reassembled.

- Sharing objects with presigned URLs — AWS S3 docs — how a signed, time-limited URL grants one operation on one object.

- How caching works — Cloudflare — how a CDN caches objects at edge locations near users to cut origin load.

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

The core split: bytes in object storage, pointer in the databaseUploads: split the file into partsPresigned URLs: the client uploads directly to storageServing: CDN for public media, signed URLs for privateWhat a strong answer sounds likeThe transferable patternSources and further reading

Read0%

Need help?Ask about this section

On this pageThe core split: bytes in object storage, pointer in the database0%

Send feedback
