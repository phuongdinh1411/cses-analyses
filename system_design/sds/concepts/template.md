---
layout: simple
title: "The System Design Template — System Design School"
permalink: /system_design/sds/concepts/template
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

Networking EssentialsTechnology ChoicesRedisTries & Prefix Search

Show all 5 →

# The System Design Template

## The Template in One Sentence

Many system design interview questions use the same basic design. Writes go into a message queue. Workers do the actual work, then update the database and the cache. Reads come from the cache.

The write path runs from the client through the load balancer and an app server into the queue, and workers save the result to the database and update the cache. The read path runs from the client through the load balancer and an app server to the cache, and goes to the database only on a miss. This diagram is the part to learn. The rest of this page shows why each box is there and then works through example interview questions with the same diagram. These are only examples. The template fits many other questions too.

If you prefer video, this one covers the same template and the same example questions.

## Build It One Box at a Time

Each box in the template exists because a specific problem forces it. Click Next to add the boxes in order; each step names the problem that forces the next box.

1. One server, one database

◀ BackNext ▶Step 1 / 7

Why The smallest design that works: the client calls one app server, which reads and writes one database.

The build has five steps:

- One app server and one database is the smallest design that works.

- One server has a limit on requests per second. Run several stateless app servers behind a load balancer. Stateless means that a server keeps no user data in its own memory between requests, so any server can take any request.

- Most requests read the same rows again and again. Put an in-memory cache in front of the database. If 9 of 10 reads hit the cache, the database sees 1 read in 10.

- One database is still one machine. Add read replicas. The primary takes the writes and copies them to the replicas, which serve reads. A replica can be a little behind the primary.

- Some writes are slow, and some arrive in bursts. Put a message queue between the app servers and the work. The server puts the write in the queue and answers at once. Workers take jobs from the queue, do the work, and update the database and the cache.

## The Queue Is the Center

The write path is the part the template is built around. A write request returns as soon as the job is in the queue, so the user does not wait for slow work. Workers then save the result and update the cache.

The queue also absorbs bursts. When more writes arrive than the workers can process, the jobs wait in the queue instead of overloading the servers.

The read path is short. The server asks the cache, and it goes to the database only on a miss.

## Plug-In Boxes

Some questions need a box that the core template does not have. Each plug-in is a larger or more specialized version of a box that is already in the template.

- Object storage keeps large files such as images and video. It is the database for file bytes. The database keeps only a row with the file's address.

- A CDN (content delivery network) keeps copies of files on servers near the users. It is the cache for large files, placed close to the viewers.

- A search index answers text search. It is a copy of the data built for one kind of read, kept current by the queue and workers, the same way a cache is.

## How to Read a Question

The words in a question tell you which part of the template it depends on. For more detail, see the Problem Decomposition Framework in the primer.

Word typeWhat it gives youExample

VerbsThe use cases. Each verb becomes an API call on the read path or the write path.submit, upload, search, send

NounsThe data that goes in the database.submission, video, post, message

AdjectivesThe constraints. They usually point at the box that carries the design.fast, real-time, reliable

## Example Questions on One Template

Each question below uses the same template. The difference is which part does most of the work.

QuestionThe part that carries itFull solution

Design LeetCodeThe queue and workers run submitted code in sandboxes.Online judge

Design YouTubeThe queue and workers convert uploads. Object storage and a CDN serve video.YouTube

Design a URL shortenerThe read path. The cache answers most redirects.URL shortener

Design post searchThe search index plug-in, fed by the queue and an indexing worker.Post search

Design a chat appEvery box. The app servers become gateways that hold open connections.Chat app

Design TicketmasterThe template, plus one atomic hold on each seat.Ticketmaster

Design a news feedThe template, plus hybrid fan-out for very large accounts.News feed

### 1. LeetCode: the Queue Does the Work

A user reads a problem, writes code, and submits it. Reading a problem is a read, and many users read the same few problems, so the problem pages come from the cache. Submitting is a write that is slow and arrives in bursts when a contest starts. A slow, bursty write is the job the queue is for.

LeetCode

Write pathRead path

Write Submit: the job goes into the queue and returns an ID; sandboxed workers run the code and save the verdict.

Carries it The queue and workers. Running code is a slow write that arrives in bursts when a contest opens.

Running submitted code takes a few seconds. The code compiles, runs against hidden tests, and runs in a sandbox, an isolated environment, because the code is untrusted. The submit request cannot wait for all of that. It puts a job in the queue and returns a submission ID with the status queued. Workers run the code and write the verdict to the database. The app checks the submission ID until the verdict is there.

The queue matters most during a contest. The online judge solution assumes about 60 submissions per second on a normal day and about 670 per second when a contest opens. At about 3 seconds per run, the peak needs about 2,000 sandboxes, or about 250 worker machines at 8 sandboxes each.

While new machines start, the extra submissions wait in the queue, and the submit request still returns at once.

### 2. YouTube: the Same Write Path, Plus Plug-Ins

LeetCode's slow write runs code. YouTube's slow write is a large upload. Check the requirements before you add boxes. Uploading is a slow write, because each video must be converted into several sizes, so it uses the queue and workers. Watching is a read, and views far outnumber uploads, so it uses the read path. The only difference is size: a video is gigabytes, not a row. That is why the two plug-ins appear.

YouTube

Write pathRead path

Write Upload: the file goes to object storage, a job goes into the queue, and workers convert it into several sizes.

Carries it The queue and workers for the slow upload, plus the plug-ins for large files: object storage and the CDN.

The file does not go through the app servers. The app gives the phone a pre-signed URL, a link that works for a few minutes and allows an upload straight into object storage. When the upload finishes, a job goes into the queue. Workers convert the video into several sizes, so a phone on a weak connection can play a small one and a television can play a large one. The YouTube solution assumes about 500 hours of new video each minute, so the conversion work is large.

Watching is the read path, and the CDN carries most of it. The video is served in chunks of a few seconds each, and the CDN keeps copies of popular chunks on servers near the viewers. A viewer in Tokyo usually gets a popular video from a server near Tokyo.

### 3. URL Shortener: the Read Path Does the Work

The first two questions depend on the write path. The URL shortener is almost all reads. Shortening is a write and opening a link is a read, so it uses the same two paths. The URL shortener solution assumes 100 million daily users, about 1 million new links per day, and 100 redirects for each link. That is about 12 writes per second and about 1,200 reads per second.

URL shortener

Write pathRead path

Write Shorten a link: about 12 writes per second, so the queue has little to do.

Carries it The read path. A short code and its URL is a small key and value that many people open.

A short code and its long URL is a small key and value, and popular links are opened many times, so the cache answers most redirects. The queue has little to do in this question. The template stays the same, and a different part carries the load.

The one new part is the code generator. Each link needs a code that no other link has, and two app servers could create the same code. Each machine gets its own ID and counts up on its own, with its ID in front. The number is then written in base 62 (digits, lowercase letters, and uppercase letters). Six characters give about 56.8 billion codes: one character for the machine and five for the counter.

### 4. Post Search: a Search Index Fed by the Queue

Post search uses both paths, and its read is one that a cache cannot do. Publishing a post is a write that can finish in the background, so it uses the queue. Searching is a read, but a search is not a lookup by key. The search index plug-in does the reading.

A database cannot search the text of billions of posts at query time. An inverted index maps each word to the list of posts that contain it, like the index at the back of a book. A search for two words reads two lists and keeps the posts that are in both.

When a user publishes a post, the post is saved and a job goes into the queue. An indexing worker adds the post to the list for each of its words, so the post appears in search results a few seconds later. A cache in front of the index keeps results for popular searches.

Post search

Write pathRead path

Write Publish: a job goes into the queue, and an indexing worker adds the post to the index.

Carries it The search index plug-in, kept fresh by the queue. It plays the same part as the cache, for text search.

### 5. Chat: Every Box in the Template

In the first four questions, the client asks and the server answers. In chat, the server must send a message that the user did not ask for. Sending a message is a write that must be saved, so it uses the database. Receiving messages is a read that the server pushes. Online status is small data that changes often, so it is kept in memory.

Each client keeps a WebSocket open, a connection that stays open in both directions. The servers that hold these connections are called gateways, and they are no longer stateless. With 100 million users online and about 100,000 connections for each gateway, that is about 1,000 gateway servers. The gateways are the one box that changes. Every other box keeps its usual job.

Chat

Write pathRead path

Write Send: the gateway saves the message first, then gives the sender a check mark.

Carries it Every box. The one change is the app servers: they hold open WebSockets, so they become gateways.

The database saves each message before delivery, with the next number in its conversation, and only then does Alice see her check mark. If Bob is offline, a job goes into a queue and a worker sends a push notification. When Bob reconnects, his app asks for the messages after the last number that it saw.

## Where You Add One More Piece

In the five questions above, each slow write can wait its turn in a queue. In the next two, the template still does most of the work, and one part needs an extra piece.

### 6. Ticketmaster: an Atomic Hold

Ticketmaster

Waiting (no token)Hold (with token)

Waiting (no token) A buy-flow request with no admission token: the load balancer (or CDN edge) sends it to the waiting room, which serves the waiting page and later issues a token. Search and other pages still go straight to the app servers.

Carries it Two changes to the template: one new box beside the app servers (the waiting room, for the hot event's buying routes only) and one changed arrow (the hold goes to the in-memory store instead of the job queue).

A popular concert goes on sale. The Ticketmaster solution assumes about 1 million buyers in the first minute for 50,000 seats, which is about 20 buyers for each seat. Browsing seats is a read, and many users look at the same seat map, so the cache handles it. A seat map that is a second old is acceptable.

Holding a seat is a write. If each click goes into the job queue and returns "accepted", all 20 buyers think that they have the seat, and 19 of them get bad news later.

The template changes in two places:

- One new box: a waiting room beside the app servers, for the hot event's buying routes only. The routing layer (the load balancer, or the CDN edge) checks each request. Search, concert pages, and account pages go straight to the app servers as usual. Requests for the hot event's seat map, holds, and checkout that carry no admission token go to the waiting room instead. The waiting room is its own small service: it serves the "you are number 40,000 in line" page and keeps each buyer's token and place in line in an in-memory store, for example a sorted set keyed by arrival time, so the app servers never handle a million people refreshing a waiting page. When a buyer's turn comes, it issues a short-lived admission token, usually a cookie; requests with a valid token pass through to the app servers, which check the token again before they accept a hold. Hosted waiting rooms work this way: Cloudflare Waiting Room serves the waiting page from its edge for the routes it is configured on, Queue-it redirects visitors without a token to a waiting room on its own servers and sends them back in order, and the AWS Virtual Waiting Room issues tokens that let users in in controlled waves.

- One changed arrow: the hold skips the job queue. The app server claims the seat in the in-memory store with one atomic operation: set the seat to held only if it is free, with an expiry (for example SET hold:A12 alice NX EX 600). The first request wins, and the other 19 are refused at once. If the buyer does not pay in time, the hold expires and the seat goes back on sale. The database is written only at purchase, with a conditional write that sells the seat only if it is still available. That write is the final guard if the in-memory store ever loses a hold.

Everything else stays as it was: browsing uses the cache, and work such as confirmation emails can still use the job queue.

### 7. News Feed: Hybrid Fan-Out

News feed

Write pathRead path

Write Post: a fan-out worker copies the post ID into each follower's feed.

Carries it No new box. One extra arrow on the read path: for accounts above about 100K followers, the app server pulls their posts at read time instead of pushing them.

Posting is a write, and opening a feed is a read that happens much more often. The usual design does the work at write time: a worker copies each new post ID into the feed of each follower, so opening a feed is one cache read. For an account with 50 million followers, one post means 50 million feed writes, and other posts wait behind it in the queue.

Here no box is added. The change is one extra arrow on the read path. The news feed solution still pushes posts from accounts below about 100,000 followers through the queue and the fan-out workers. Posts from larger accounts are not pushed: when a reader opens the feed, the app server also reads their recent posts and merges them into the feed. Most readers follow only a few very large accounts, so the pull usually adds one or two reads.

For more patterns of this kind, see Scaling Reads and Writes and the other pattern articles.

## How to Use the Template in an Interview

Do not start by drawing the template. Start from the question, and draw the template only once the requirements show that it fits.

- Understand the problem. Ask clarifying questions, and list the verbs (the use cases), the nouns (the data), and the adjectives (the constraints).

- Sort the verbs into reads and writes. Note which writes are slow or arrive in bursts, and which reads repeat the same data.

- Decide whether the template fits, and which part carries it. Slow or bursty writes point to the queue and workers. Repeated reads point to the cache. Large files, text search, or real-time delivery point to a plug-in or to gateways. If many users compete for one item, or one write must reach millions of readers, plan the one extra piece.

- Draw the design one box at a time. Name the requirement that each box serves as you add it, then trace one read and one write through the diagram.

## Next Steps

- Read the System Design Primer for the full method, from requirements to deep dives.

- Practice with the interview questions. Each question has a full written solution.

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

The Template in One SentenceBuild It One Box at a TimeThe Queue Is the CenterPlug-In BoxesHow to Read a QuestionExample Questions on One Template1. LeetCode: the Queue Does the Work2. YouTube: the Same Write Path, Plus Plug-Ins3. URL Shortener: the Read Path Does the Work4. Post Search: a Search Index Fed by the Queue5. Chat: Every Box in the TemplateWhere You Add One More Piece6. Ticketmaster: an Atomic Hold7. News Feed: Hybrid Fan-OutHow to Use the Template in an InterviewNext Steps

Read0%

Need help?Ask about this section

On this pageThe Template in One Sentence0%

Send feedback
