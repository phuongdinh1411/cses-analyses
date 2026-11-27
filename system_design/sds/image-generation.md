---
layout: simple
title: "Design Image Generation Service — System Design School"
permalink: /system_design/sds/image-generation
---

# Design an Image Generation Service

**Difficulty:** Hard  
**Topics:** GPU serving · Batching · Async processing · Object storage · CDN & delivery economics · Caching

## Problem statement

Design a service that turns a text prompt into an image. A user submits a prompt plus parameters: the image size, the number of denoising steps, a random seed, and how many images to make. The user gets back one or more generated images.

The model already exists and is trained. The service serves it. In scope are submitting a request, showing progress while the image forms, storing and delivering the finished images, and checking the prompt and the output for safety. Training and fine-tuning the model, a language model that rewrites prompts before generation, and video generation are out of scope. The last two come back as variants.

## Clarifying questions

Each question below fixes an assumption that the rest of the design depends on.

- Serving only, or training too? Serving an already-trained model. Training and fine-tuning are a separate offline system.

- Synchronous or asynchronous? Asynchronous. Generation runs for seconds to tens of seconds, so the request is a job with progress, not a blocking call.

- One model, one modality? One diffusion model that outputs still images. A prompt-rewriting model in front and video output are deferred.

- What can the user control? Size, step count, seed, and image count. These four set the compute shape and the cost of each request.

- Preview or final image only? The job streams progress and an optional low-resolution preview while it runs, so the user sees the image form.

- Is safety in scope? Yes. The input prompt and every output image are checked before delivery.

- What is the unit of scale? GPU-seconds per image times images per day. Each image holds a scarce accelerator for a fixed span, so the request rate alone does not size the system.

## What makes this problem distinctive

A text-to-image request looks like any API call: a short string goes in and an image comes out. Three properties make it different from a typical request-response service.

The work is heavy and fixed. The model runs on a graphics processing unit (GPU), an accelerator built for large parallel math. It runs a set number of steps per image. The cost of one image is therefore known before the work starts, but it is large, and the GPU is the scarce, expensive resource.

The output is a large binary, not a row or a token stream. It must be stored and delivered like media, not returned through the application tier.

Safety sits on both ends. A prompt can ask for something disallowed. An allowed prompt can still produce a disallowed image. Either failure reaches a real person.

GPU-seconds. The unit of GPU work: one GPU busy for one second. If one image needs 30 steps at 40 ms each, it costs 1.2 GPU-seconds. A fleet of 10 GPUs supplies 10 GPU-seconds of work every wall-clock second.

The diagram shows the tension. A small, cheap request turns into a large, expensive artifact, and the path between them has a gate at each end.

Key idea. Image generation is a fixed-cost GPU job that emits a large binary, with a safety gate on both ends.

## Key concepts

This section covers the concepts needed to solve this problem — prerequisites for the design work that follows.

### Diffusion and denoising steps

A diffusion model makes an image by starting from random noise and removing a little of that noise in each step. After a fixed number of steps, the noise has become a picture that matches the prompt. Each step is one pass of the model on the GPU. A run of 30 steps is 30 passes, and every pass for a given size costs about the same.

The widget runs this loop. Move the step slider and watch the cost change before the run starts. The right panel shows the preview the client receives every few steps.

Denoise Resetsteps 30 ms/step 40 seed

Worker: step 0 of 30

Client: last preview (step 0)

a preview every 5 steps

Cost per image (known before start)

30 × 40 ms = 1.20 GPU-s

GPU time spent so far

0.00 GPU-s

Previews pushed to the client

0

Illustrative: per-step time depends on the model, resolution, and hardware. The same seed gives the same starting noise, so the same image.

Two properties follow from the loop. The cost is steps × time per step, so it is known when the request arrives. And the step count is a quality dial: fewer steps are faster and cheaper but give a rougher image, while more steps cost more for smaller gains.

### Seeds and reproducibility

The starting noise comes from a seed, a number that drives a pseudo-random generator. The same seed gives the same starting noise. With the same prompt, parameters, seed, and model version, the run produces the same image, assuming a pinned model and runtime environment.

This makes a generated image a pure function of its inputs: same inputs, same output. Two design levers come from this fact later in the article.

### Batching on a GPU

A single denoising run does not keep a modern GPU fully busy. Batching runs several requests through the model together in one pass. The GPU does more useful work per second, and each request pays a small extra latency.

A batch only works when its requests have the same tensor shape, the dimensions of the arrays the model processes. For an image model, the shape comes from the width, height, and step count. Two requests for 1024×1024 at 30 steps can share a batch. A 1024×1024 request and a 512×768 request cannot.

### Asynchronous jobs

An asynchronous job separates "accept the request" from "do the work." The client submits and gets a job id at once. A queue holds the job. A worker picks it up, does the work, and records the result. The client checks the job's status, or keeps a connection open to receive updates. For the full pattern, see Asynchronous Jobs.

### Object storage and a CDN

Large binaries do not belong in a database. Object storage holds files by key and returns them by URL. A content delivery network (CDN) is a set of edge servers near users that cache those files, so most views never reach the origin. See Object Storage and CDN for the mechanics.

### Safety classifiers

A safety classifier is a model that labels an input as allowed or disallowed. A text classifier checks the prompt. An image classifier checks the pixels. Every classifier makes two kinds of error: a false positive blocks something safe, and a false negative lets something unsafe through. Tuning moves the balance between the two; it cannot remove both.

Key idea. A diffusion image is a fixed number of same-cost GPU steps from a seeded noise start, so its cost is known up front and its output is reproducible.

## 1. Requirements

Before reading on. Name three functional and three non-functional requirements. Then name the one resource to size first.

### 1.1 Functional requirements

The verbs in the problem statement become the functional requirements.

- Submit a prompt plus parameters (size, steps, seed, count) and receive one or more images.

- Track progress. The request is a job. The user sees its status and an optional low-resolution preview while it runs.

- Store and deliver the images. They persist and load fast, by URL, from anywhere.

- Gate for safety. The prompt and every output image pass a check before delivery.

Training, prompt rewriting, and video generation are named and deferred.

### 1.2 Non-functional requirements

- Throughput and cost. Maximize images per GPU-second. GPU capacity is the dominant cost and the scarce resource.

- Time to first preview and total time. The user waits seconds. An early preview shows that work is happening. Total time to the final image is the main latency number.

- Modest durability. Users expect their images to persist. But an image can be regenerated from its inputs when the model version is pinned, so the requirement is softer than for uploaded photos.

- Graceful degradation. Under GPU saturation, the system queues with an honest wait estimate, sheds load, or lowers steps or size. It does not collapse.

- Safety is non-negotiable. An unsafe image that reaches a user is worse than a slow one. The gates stay on under load.

### 1.3 The constraint versus the property

These two pull against each other. Safety is the property the design will not compromise: the input and output gates are never skipped. GPU economics is the constraint that shapes the design: nearly every decision that follows — same-shape batching, the steps dial, the input cache, admission control — exists to raise images per GPU-second.

They collide at the output gate. The image classifier is itself model inference on every image, and it competes for the same accelerators. It must stay cheap relative to generation, or it consumes the throughput the rest of the design gains. That is why the safety pipeline gets its own deep dive.

Key idea. Safety is the property you protect; images per GPU-second is the constraint you design around.

## 2. Back-of-the-envelope estimation

The estimate shows that GPU-seconds, not the request rate, size the system. All inputs are illustrative anchors. The calculator recomputes each figure as you move the inputs.

Images per day: 50MDenoising steps: 30GPU time per step: 40 msReal GPU utilization: 50%Request-hash cache hit rate: 0%Bytes per image: 1 MBHot retention: 90 days

GPU-seconds per image

1.20

30 steps × 40 ms

GPU-seconds per day

60.0M

50M × (1 − 0%) × 1.20

GPU fleet

1,389 GPUs

60.0M ÷ 86,400 ÷ 50%

Average submit rate

579 /s

50M ÷ 86,400

New image bytes per day

50 TB

50M × 1 MB

Hot storage

4.5K TB

50 TB × 90 days

Inputs are illustrative anchors, not measured values. The fleet follows GPU-seconds, not the request rate.

### 2.1 Cost per image

Assume 30 denoising steps at roughly 40 ms of GPU time per step for a mid-size image (illustrative). One image is then 30 × 40 ms = 1,200 ms, about 1.2 GPU-seconds. This number is fixed as soon as size and steps are set. A language model that streams tokens cannot know its cost in advance, because the output length is unknown. An image model can.

### 2.2 The GPU fleet

Assume 50 million images per day (illustrative). That is 50M × 1.2 = 60M GPU-seconds of work per day. A day has 86,400 seconds, so 60M ÷ 86,400 ≈ 700 GPUs must be busy at all times. At roughly 50% real utilization, the fleet is about 1,400 GPUs. The method matters more than the result: images per day × GPU-seconds per image ÷ seconds per day ÷ utilization.

For contrast, 50 million images per day is only about 580 submits per second on average. That rate is small for an API tier. The GPU work behind it is not.

### 2.3 Storage and delivery

At roughly 1 MB per finished image, new bytes are 50M × 1 MB = 50 TB per day. Ninety days of hot images is 50 TB × 90 = 4,500 TB, a few petabytes. That is real, but cheap next to the GPU fleet.

A finished image never changes, so a CDN can cache it indefinitely. As in YouTube, the goal is for nearly all bytes to serve from the edge so that origin egress stays small.

### 2.4 Queue wait at peak

A burst at several times the average fills the queue. Because each image has a fixed cost, the wait is computable: jobs ahead × GPU-seconds per image ÷ GPUs serving that shape. The system can show the user an honest estimate instead of a spinner.

Key idea. Size the fleet by GPU-seconds: 50M images × 1.2 GPU-seconds ≈ 700 busy GPUs, about 1,400 at half utilization. Storage and request rate are secondary.

## 3. API design

Design checkpoint

A generation takes 5 to 20 seconds. What should POST /v1/images/generate return?

The image bytes, after the model finishesA URL to the image, after the model finishesA job id at once, with progress and the image URL delivered later

The calls follow the life of one request: submit, watch, fetch, and cancel. The user identity comes from the authenticated session, never from the request body.

### 3.1 Submit a generation

POST/v1/images/generate

Request & response

Width, height, and steps set the compute shape, which decides which batch a request can join. The seed makes the result reproducible. When the client omits it, the server picks one and stores it on the job. count asks for N variations of one prompt.

### 3.2 Watch the job

GET/v1/jobs/{job_id}

Request & response

GET/v1/jobs/{job_id}/events

Request & response

The events endpoint pushes updates over one held connection, using Server-Sent Events (SSE) or a WebSocket (see Real-Time Transport). There is no partial answer to stream, only progress and a coarser version of the one image.

The status distinguishes failed (an error) from blocked (a safety refusal). A job can finish generation and still be blocked by the output classifier. The product must explain the difference, so the response carries a reason.

### 3.3 Fetch the image

GET{image_url}

Request & response

The finished image is an immutable object with its own URL. The generate response never carries image bytes.

### 3.4 Cancel

POST/v1/jobs/{job_id}/cancel

Request & response

A job the user abandoned still burns GPU-seconds if it keeps running. Cancel propagates to the worker and frees the slot.

Key idea. Submit returns a job handle, not an image; the parameters define the compute shape that later decides batching.

## 4. Data model

Start with the one obvious entity. Each thing it cannot represent introduces the next.

### 4.1 The generation job

The core record is one request: the prompt, the parameters, who asked, and a status. The status moves queued → running → done, or ends in blocked or failed.

### 4.2 The image

A job produces one or more images, and each is a large file. The bytes do not fit in a database row. The image becomes its own entity: a reference to bytes stored elsewhere, plus the few fields that queries use.

### 4.3 The safety result

A job has two verdicts: one for the prompt, one for each output image. Each verdict has a stage and a reason that must stay answerable long after ("why was this blocked?"). A boolean on the job cannot hold that, so each verdict is its own record.

### 4.4 The request-hash cache

Identical requests should not spend the GPU twice. Because the output is a pure function of its inputs, a cache entry maps hash(prompt, params, seed, model_version) to an existing image_id. A hit skips generation.

### 4.5 Where each entity lives

One job produces many images and many safety results. A cache entry points at one image. Each entity has a natural home:

- The job and safety results live in a durable job store, keyed by job_id and partitioned by tenant_id. The queue that workers pull from sits in front of it. Durability means a crashed worker's job runs again rather than vanishing.

- The image record sits in the same metadata store. The image bytes live in object storage behind the CDN. This is the metadata/media split from YouTube.

- The request-hash cache lives in a fast key-value store, in front of everything.

Key idea. The job is a small row; the image is a row plus a blob; the cache is an index that exists because the output is reproducible.

## 5. High-level design

Start with the simplest design that could work. Each failure adds one component.

Reading the diagrams. Each step marks the components added at that step with a dashed outline and a NEW badge.

### 5.1 One server runs the model

The app server takes the prompt, runs the model in-process, and returns the image bytes in the response.

Five things break once real traffic arrives:

- The model needs a GPU and runs for seconds. A stateless app server cannot hold it, and one user's request occupies the GPU while everyone else waits.

- One image per GPU at a time wastes most of an expensive accelerator.

- The output is a large binary. Returning it inline, and re-serving it through the app tier on every view, puts bytes on the wrong path.

- Nothing checks the prompt or the image.

- The user waits with no feedback, so a slow call looks like a broken one.

### 5.2 Fix 1: an async job and a GPU worker fleet

Split the work. A stateless API tier validates the request, writes a GenerationJob, enqueues it, and returns the job id. A pool of GPU workers pulls jobs, runs the denoising loop, and writes results back.

A worker holds a job for a known span and is then free. Unlike a language model, it carries no per-token state between steps, because there is no growing key-value (KV) cache — the memory a language model keeps for every token it has generated.

The fleet now scales independently of the API tier. But each worker still runs one image at a time.

### 5.3 Fix 2: batch same-shape requests

Requests with the same width, height, and step count have identical shapes. A batch scheduler between the queue and the GPUs groups them and runs each group as one batch. Every request in the batch runs the same number of steps, so they start and finish together.

Throughput per GPU rises. The first deep dive covers the scheduling problem this creates.

### 5.4 Fix 3: object storage and a CDN for the images

The worker writes each finished image to object storage and the small image record to the metadata store. Clients fetch the image by an immutable URL from the CDN. Image bytes never flow back through the API tier.

### 5.5 Fix 4: a safety gate on both ends

An input prompt filter runs before a job enters the queue. A disallowed prompt never spends a GPU-second. An output image classifier runs after generation and before the image is written for delivery. A blocked image never gets a deliverable URL, and the job status becomes blocked. Both gates sit inline, so nothing can route around them under load.

### 5.6 Fix 5: stream progress and a preview

While the worker denoises, it reports progress (step k of N). Every few steps, it can decode a cheap low-resolution preview from the current intermediate. A progress channel carries these events to the API tier, which relays them to the client over the held events connection.

### 5.7 Fix 6: a request-hash cache in front

Popular prompts with default parameters repeat. Each repeat would spend another 1.2 GPU-seconds to produce a pixel-identical image. Because the output is a pure function of its inputs, the API tier first looks up hash(prompt, params, seed, model_version). A hit returns the existing image and skips the queue and the GPU.

The cache hit still passed both safety checks when the image was first made, so returning it does not bypass the gate.

### 5.8 The composed design

The boxes are the data model's homes. The API tier writes the job. The GPU workers write image bytes and status. The output classifier decides what becomes deliverable. The CDN serves it. One data-model entity becomes two boxes: the image is a row in the metadata store, which queries read, and an object in storage, which viewers download.

Key idea. Each component answers one failure of the single-server design: the async split for GPU-bound work, batching for GPU cost, object storage and CDN for the binary, two gates for safety, streaming for the wait, and the cache for repeats.

## 6. Deep dives

### 6.1 The GPU serving profile: batching a fixed-step model

Before reading on. A fleet of GPUs receives requests of many sizes and step counts. How do you keep the GPUs full, and why is this easier than for a language model?

Same-shape batching raises throughput. Compare it with continuous batching for a language model, as in ChatGPT-style serving. A language-model batch mixes requests that finish at unpredictable times: one wants a word, another wants an essay. The scheduler must add and remove requests at every token step, and it must manage a KV cache that grows with every token. An image batch is uniform. Every request runs the same fixed step count, so the batch starts and finishes together. There is no KV cache, and the shapes match. A plain fixed batch is enough.

The fixed step count also gives a precise cost lever. Cost is steps × time per step, so halving steps roughly halves GPU-seconds. Fewer steps give a rougher image, and more steps give diminishing gains. The product can expose this as presets (fast, standard, high) or cap steps under load. Research on faster samplers and distilled models reduces the step count needed for good quality (see Sources).

The real scheduling problem is shape fragmentation. Batching only helps within one shape. If users request any size, the queue splits into many small groups, and each group rarely fills a batch. The GPU runs half-empty batches or waits.

Design checkpoint

Users can request any width and height. Batch fill rate is low and GPUs run mostly half-empty batches. What fixes it?

Add more GPUs so each small group gets its ownPad every request to the largest size so all requests share one shapeOffer a small menu of supported sizes and cap how long a batch waits to fill

The fix has two parts. First, constrain sizes to a small menu so requests land in a few batchable buckets. Second, set a maximum wait to fill a batch, then run a partial batch. This trades latency for utilization: a longer wait fills more slots but delays the first request in the group. A count of N is the same shape run with N seeds, so it fills a batch on its own.

Run the widget in each mode. "One image per GPU" lets the queue grow. "Batch, any size" splits requests across eight shapes and the fill stays low. "Batch, size menu" fills batches and drains the queue. Move the fill-wait slider to see the latency trade.

one image per GPUbatch, any sizebatch, size menu

Play Restart

max fill wait 6 ticks

Waiting requests, grouped by shape (tick 0 of 120)

512²

640×480

768²

800×600

1024²

720×1280

896²

1152×768

GPU

idle

Images finished

0

Avg batch fill

0.0 / 4

Images per busy GPU tick

0.00

Queue now · avg wait

0 · 0.0t

Illustrative model: one GPU, batches of up to 4, a batch takes 4–5 ticks regardless of fill. Real speedups depend on the model and hardware.

An admission controller in front of the queue protects the wait time. Under saturation it has three options: queue with an honest estimate, which is cheap to compute because the cost per image is fixed; shed new requests; or degrade by lowering default steps or size. Each is better than a queue that grows without limit.

A worker that dies mid-generation loses only that job's intermediates. The job is durable and reproducible from its seed, so it runs again on another worker at a known retry cost. The signals to watch are GPU utilization, batch fill rate (low fill means fragmentation), images per GPU-second, queue depth, p99 wait, and retry rate.

What separates answers — GPU serving

BadOne image per GPU, or mixed shapes in one batch▾

GoodSame-shape fixed batches plus a steps dial▾

GreatSize menu, bounded fill wait, honest estimates, contrast with LLM batching▾

### 6.2 Storage and delivery of generated media

Before reading on. Each generated image is a large binary that may be viewed many times or never again. How do you store and serve it cheaply, and what can you avoid storing at all?

The metadata/media split carries over from YouTube with one difference: the bytes come from the GPU fleet, not from an uploading user. Small image records go in the metadata store. The bytes go in object storage behind immutable URLs.

A finished image never changes, so the CDN can cache it indefinitely. Nearly all views should serve from the edge. A multi-tier CDN, with regional tiers behind the edge, raises the combined hit rate, so origin egress stays small.

The request-hash cache is the highest-value cache in the system. A hit saves seconds of GPU work, not milliseconds of a database read (see Caching). Hits concentrate at the head of the distribution: popular prompts with default parameters. The seed decides whether that head exists. If the server assigns a fresh random seed to every request that omits one, no two requests share a key and the hit rate drops to near zero. A product that wants variety on each click accepts that loss; one that wants repeat requests to be cheap uses a default seed.

Design checkpoint

The request-hash cache keys on hash(prompt, params, seed, model_version). The hit rate is near zero even though many users type the same prompts. What is the likely cause?

The cache is too small to hold the popular promptsThe server picks a fresh random seed for every request that omits oneThe CDN is serving the hits before the cache sees them

The widget plays a skewed request stream. Compare a default seed with a fresh seed per request, and watch the GPU-seconds saved.

Play requests Restartdefault seed when omittedfresh random seed per request

Latest requests → key = hash(prompt, params, seed, model_version)

press play

Requests · hit rate

0 · 0%

GPU-seconds spent (misses × 1.2)

0.0

GPU-seconds saved (hits × 1.2)

0.0

Illustrative stream: a few popular prompts repeat, most prompts appear once. Real hit rates depend on the product and how seeds are assigned.

Retention follows the view pattern. Most images are viewed soon after creation and rarely afterward. Tier storage by age and popularity: hot images on fast storage near the CDN, cold ones on cheap archival storage.

Determinism adds a lever that uploaded media lacks. Because the output is a pure function of (prompt, params, seed, model_version), the system can drop the bytes of the cold tail and regenerate them on demand. This trades GPU-seconds to recreate against the storage cost to keep. It only works while that model version stays available to serve. A user-uploaded photo has no generator, so it must be stored.

Object storage is the durability anchor. An edge failure only lowers the hit rate, and origin absorbs it. An origin shield — one designated cache tier that all edges consult before origin — coalesces misses, so a suddenly popular image does not flood the origin. Watch the CDN hit rate (the egress bill), the request-hash hit rate (GPU-seconds saved), storage growth per tier, and the per-image view distribution.

What separates answers — storage and delivery

BadBytes inline, served from the app tier▾

GoodMetadata/media split, CDN, request-hash cache▾

GreatHit rate as the egress budget, tiered retention, regenerate the cold tail▾

### 6.3 The safety pipeline

Before reading on. A prompt can ask for something disallowed, and an innocent prompt can still produce a bad image. Where do the checks go, and what is the blast radius of one bad image getting through?

Two gates are needed because each covers what the other cannot. The input prompt filter is cheap and runs before generation, so a disallowed request never spends a GPU-second. But it cannot foresee everything the model will render. The output image classifier checks the pixels after generation and before the image is delivered or marked done. It is the last line before a user sees the image.

The output classifier is compute paid on every image. This is the collision named in the requirements: the classifier is model inference, and it competes for accelerators with generation. Keep it cheap relative to a full denoising run — a small classifier, not a second diffusion model. Run it as a fast stage right after the loop, on the same worker or on a dedicated cheap fleet, so it does not double the pipeline's cost.

A miss has a wide blast radius. One unsafe image delivered is a first-order failure, with reputational and possibly legal cost. And because delivery is a cacheable CDN URL, an escaped image is now cached at the edge. Containment means the ability to purge that URL across the CDN and revoke it fast. This is why the gate is inline and cannot be bypassed, rather than a sampled audit after delivery.

The classifier trades false positives (a safe image blocked, an annoyed user) against false negatives (an unsafe image delivered, the serious failure). Tune it to favor catching the worst categories, and send borderline cases to human review instead of delivering them automatically. A blocked status with a reason lets the product explain the refusal.

Design checkpoint

At peak, the output classifier fleet saturates and its queue grows. What should happen to finished images waiting for a verdict?

Deliver them unchecked until the classifier catches upWait for a verdict, and apply backpressure to new generationsSample 10% for checking and deliver the rest

Degradation must not open the gate. Under load, the system may shed or slow generation, but it does not skip the output classifier. Safety fails closed (see Fail-open vs Fail-closed): if the classifier fleet saturates, jobs wait rather than being delivered unchecked. Watch block rates per stage, the false-positive appeal rate, classifier latency (it is on the critical path), and the human-review queue depth.

What separates answers — safety

BadPrompt check only, or skipped under load▾

GoodInput filter, output classifier, blocked status▾

GreatInline, cheap, tuned, fail-closed, purgeable▾

Key idea. Batching, delivery, and safety are the three dives because each one protects images per GPU-second or the safety property — the two forces named in the requirements.

## 7. Variants

### 7.1 10× scale

More images per day scale the GPU fleet roughly linearly. Because the cost per image is fixed, the fleet math stays a clean multiply, unlike a token-streaming model. The levers are efficiency and offload: fewer default steps through faster samplers or distilled models, a higher request-hash hit rate on the head, larger batches within the latency budget, and regeneration of the cold tail instead of storage. Storage and CDN egress grow with the catalog and are tiered as before.

### 7.2 Video generation

An output is many frames, so GPU cost and storage grow roughly with the frame count. Delivery becomes the segmented-media path from YouTube: an encoding step, segments, and adaptive bitrate, rather than one image. The serving profile stays fixed-step, and batching and the steps dial still apply, but each request costs far more.

### 7.3 A prompt-rewriting model in front

Many services expand a short prompt into a richer one with a language model before generation. That adds a small text-generation stage with its own GPU cost and latency. It also changes the cache key: cache on the rewritten prompt, or on the original prompt plus the rewriter's version and settings. The image pipeline behind it does not change.

Key idea. The design scales by multiplication because cost per image is fixed; video multiplies the cost and borrows the video delivery path.

## 8. The transferable pattern

Image generation is GPU inference serving with the unit of work changed from a token stream to a fixed-step job, whose output is a large binary. It is half an inference-serving problem and half a media-delivery problem, with a safety gate across the seam.

When the expensive work is a fixed, known block of accelerator compute, the shape repeats. Separate the GPU fleet from the stateless tier. Make the request an async job with progress. Batch the uniform, fixed-cost units. Store the output in object storage and serve it from a CDN. Cache on the inputs, because the output is a function of them. Gate both ends for safety. The same shape fits text-to-speech, 3D-asset generation, and video generation.

## Review: the 30-second answer

- Fixed-step GPU job. Each image is a set number of denoising steps, so its cost is known up front and GPU-seconds are the bill.

- Async with progress. Submit returns a job id; the client receives progress and a preview, then the URL.

- Batch same-shape requests. A size menu and a bounded fill wait keep batches full; no KV cache or continuous batching is needed.

- Object storage plus CDN. The response never carries bytes; a request-hash cache skips the GPU for repeats.

- Two safety gates. Filter the prompt before the GPU, classify the image before delivery, and fail closed under load.

## Quiz

Image Generation Design Quiz

Hide AllReveal All

1)Why is the GPU fleet sized from GPU-seconds per image rather than from requests per second?

2)Why does batching an image model need a simpler scheduler than batching a language model?

3)What is shape fragmentation, and how is it fixed?

4)What can an image generation service avoid storing that a photo-sharing service cannot?

5)Why can the seed policy decide the request-hash cache hit rate?

6)Why is the output classifier needed when the prompt already passed the input filter?

7)The output classifier saturates at peak. Why must jobs wait instead of being delivered?

## Sources and further reading

- Denoising Diffusion Probabilistic Models — Ho, Jain, Abbeel (2020) — the denoising loop that starts from noise and removes it over a fixed number of steps.

- High-Resolution Image Synthesis with Latent Diffusion Models — Rombach et al. (2022) — running diffusion in a compressed latent space, the basis of many deployed text-to-image models.

- Denoising Diffusion Implicit Models — Song, Meng, Ermon (2021) — a sampler that produces good images with far fewer steps, the basis of the steps-versus-quality dial.

- Progressive Distillation for Fast Sampling of Diffusion Models — Salimans, Ho (2022) — distilling a model to need fewer steps, a lever for 10× scale.

- Server-sent events — MDN Web Docs — the one-way streaming transport used for progress and previews.
