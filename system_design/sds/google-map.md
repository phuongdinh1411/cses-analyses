---
layout: simple
title: "Design Google Maps — System Design School"
permalink: /system_design/sds/google-map
---

# Design Google Maps

**Topics:** Geospatial indexing · Route planning · CDN

Designing a mapping service like Google Maps involves integrating multi-source data — road geometry, landmarks, and live traffic — and processing location updates from 100M daily active users at roughly 41,667 writes per second. The service should be able to load specified areas' streets and buildings, display real-time traffic conditions, search for streets, buildings, and landmarks, and plan navigation routes (providing both the shortest and fastest routes).

## Summary

- **Key challenge:** Turn a location stream from 100M DAU (~41,667 writes/s, rush-hour spikes) into live traffic for a read-heavy (~10:1, ~417K reads/s) map service.
- **Core design:** Clients stream locations over WebSocket into a message queue; a Real-time Traffic Service stores and analyzes them and caches traffic conditions; a Search Service queries a derived geospatial index; a Routing Service returns shortest and fastest routes.
- **Techniques:** message queue (absorb rate gaps, failures); geohash prefix cells + 8 neighbours (2-D search on a B-tree); geographic sharding (locality); TTL + event-driven cache invalidation (fresh, fast); Flink/Kafka streaming (traffic within seconds).

## Functional Requirements

- Real-Time Traffic Information: The service should provide real-time traffic information and adjust routes based on traffic conditions.

- Route Planning: Given a starting point and a destination, the service should be able to calculate both the shortest and the fastest route (with the least time taken).

- Map Rendering: Refer to Design Map Rendering Service for reference.

- Geo-based Search: Refer to Yelp System Design.

## Non-Functional Requirements

- 100M Daily Active Users

- Read:write ratio = 1000: 1

- Data retention for 5 years

- High availability

- Low latency

- High durability

- Security

## Resource Estimation

Assuming an average usage of 30 minutes per user per day, with a read request made every 5 seconds, the service handles far more read requests than writes. Given this usage pattern, each user would make approximately 360 read requests daily. This translates to approximately 416,667 read requests (360 × 100M ÷ 86,400) and 41,667 write requests per second, about 10:1.

The storage requirement, considering that each entry is 1KB and data is retained for 5 years, is approximately 6 PB.

The resource estimator provides the corresponding calculation.

## API Endpoint Design

- The client needs to frequently send real-time locations to the server. Considering the frequency, we use Websocket to implement:
ws://location, the message is in JSON format:

{
"lon": // Longitude coordinate, double, -180.0 ~ 180.0
"lat": // Latitude coordinate, double, -90.0 ~ 90.0
}

- /route?src_lon={source longitude}&src_lat={source latitude}&dst_lon={destination longitude}&dst_lat={destination latitude}, specify the longitude and latitude of the starting point and destination to provide the shortest and fastest routes. The response body is as follows:

{
"shortestPath": {
"description": "The path with the shortest distance",
"distance": "The specific distance value",
"duration": "The specific time value",
"path": [
{
"lon": // double
"lat": // double
},
...
]
},
"fastestPath": {
"description": "The path with the shortest time taken",
"distance": "The specific distance value",
"duration": "The specific time value",
"path": [
{
"lon": // double
"lat": // double
},
...
]
}
}

## High-Level Design

Real-time traffic conditions and the calculation of the shortest time for navigation both require the user's real-time location. This is the data that is updated most frequently. The client maintains a websocket connection, periodically sending location information to the server.

That stream cannot go straight into the database. It arrives at roughly 41,667 writes per second and spikes at rush hour, while the analysis that turns raw pings into traffic conditions is slower and more variable. The two rates have to be separated, and a message queue does that.

A message queue is a durable buffer between a producer and a consumer. The producer appends messages and returns immediately; the consumer reads them at its own pace. Two properties matter here. It decouples rates: the queue absorbs the difference between arrival and processing speed instead of pushing back on the websocket connections. It decouples failure: if the consumer restarts, messages accumulate in the queue rather than being dropped, and processing resumes from the last acknowledged position.

With that buffer in place, the ingestion path is: the Websocket Server receives a location update and writes it into the message queue. The Real-time traffic Service reads from the queue, saves the information to the database, and analyzes it. The traffic conditions derived from the analysis are written into the cache.

When the client loads the map, it first needs to render the underlying maps (referring to Design Map Rendering Service for details), which depict basic shapes such as some roads, buildings (outlines), bodies of water, and green spaces.

Real-time traffic information is loaded through the Real-time traffic Service.

Search runs against a dedicated structure rather than the spatial database. The Search Index is a separate read-optimized copy of the searchable fields, storing per landmark the tokenized name, the type, and the location under a geospatial index.

With that index defined, the search path follows: the Search Service queries it, and a request like "coffee near me" resolves in two steps. A text match on the tokenized name and type narrows the corpus, then the geospatial index restricts results to the caller's neighbourhood, after which candidates are ranked by distance and relevance.

##### How the Geospatial Index Works

A latitude/longitude pair is two independent numbers, and an ordinary B-tree index can only sort on one of them. An index on latitude alone finds every landmark in a horizontal band across the planet — the correct latitude, but any longitude. The service would then have to compute distance for every one of them.

A geospatial index solves this by reducing two dimensions to one. The map is recursively divided into cells, and each cell is given a short string identifier where the prefix encodes location: cells that share a prefix are physically adjacent. A landmark is stored under the identifier of the cell containing it, so the index becomes an ordinary sorted structure that a B-tree can handle.

Each added character narrows the cell. A search for landmarks near a point computes the point's cell identifier at the precision matching the search radius, then does a prefix range scan — 9q8yy* returns everything in that roughly 5 km cell directly, with no distance computation on the rest of the planet.

One correctness detail: a landmark 100 m away can sit in a neighbouring cell if the query point falls near a cell boundary. A prefix scan on one cell would miss it. Implementations therefore query the target cell plus its eight neighbours, then filter the combined candidates by true distance.

Which subdivision scheme to use is a design choice on its own — geohash uses fixed grid cells, quadtrees subdivide only where density demands it, and S2 projects onto a sphere to avoid distortion near the poles. Choosing a spatial index compares them.

It is a derived store. Landmark rows in the spatial database remain the source of truth, and the index is rebuilt from them asynchronously — a change to a landmark is queryable once that propagation completes, not at the instant of the write. Serving search from a derived index rather than the primary keeps full-text scans off the database that route planning depends on. Yelp System Design covers the indexing and ranking details.

The Routing Service implements the navigation feature, analyzing the shortest and fastest routes based on the user's provided starting point and destination.

## Detailed Design

### Data Store

#### Database Type

A service like Google Maps uses several database types, each matched to a different access pattern:

- Spatial Database: To store and query data related to locations and geographic information. Examples include PostGIS (an extension of PostgreSQL) and Google's proprietary solutions.

- NoSQL Database: For scalable, high-performance storage of unstructured data, such as real-time traffic conditions. Examples include Cassandra or MongoDB.

- Time-Series Database: To handle time-dependent data like historical traffic patterns, which can be used for predicting future conditions. Examples include InfluxDB.

- Graph Database: To store the road network as nodes and edges and run shortest-path queries over it. Examples include Neo4j.

#### Data Schema

- Map Data:

- MapTile (id, northEastBound, southWestBound, imageUrls, lastUpdated)

- Landmark (id, name, location, type)

- Road (id, name, type, coordinates, trafficCondition)

- User Data:

- User (id, username, hashedPassword, preferences)

- UserLocation (userId, timestamp, location)

- Traffic Data:

- TrafficSnapshot (timestamp, roadId, trafficSpeed, trafficCondition)

#### Database Partitioning (Sharding)

Data can be partitioned as follows:

-

Geographic Partitioning (Sharding): The map data can be partitioned based on geographic boundaries. For example, the world can be divided into regions such as North America, Europe, Asia, etc., and each region's data is stored on separate database clusters. Within each region, further partitioning can occur at the country or city level.

- Fields for Partitioning:

- MapTile: Partitioned by northEastBound and southWestBound coordinates, which define the bounding box of the map tile.

- Landmark: Partitioned by location, which includes latitude and longitude.

- Road: Partitioned by coordinates, which is an array of latitude and longitude pairs that define the road's path.

-

Functional Partitioning: Different types of data are stored in different databases optimized for their access patterns.

-

User Data:

- User: Can be partitioned by id if the user base is large enough, with IDs hashed to distribute across shards evenly.

- UserLocation: Partitioned by userId to keep all location updates for a user on the same shard, so a query for one user's history reads a single shard.

-

Traffic Data:

- TrafficSnapshot: Partitioned by timestamp and roadId. The timestamp allows for partitioning data into time-based chunks (e.g., per day or per hour), while roadId ensures that all traffic data for a specific road segment is stored together.

For more detailed content, refer to Partitioning (Sharding).

#### Database Replication

- Read Replicas: To handle the high read load and improve read performance.

- Multi-Region Replication: To ensure low latency access across different geographical locations and provide disaster recovery.

See Replication.

#### Data Retention and Cleanup

- Old Traffic Data: Aggregate and anonymize old traffic data for historical analysis and delete individual records after a certain period.

- User Data: Implement GDPR-compliant data retention policies, allowing users to request data deletion.

#### Cache

-

In-memory Data Stores:

Utilize in-memory data stores like Redis or Memcached to cache frequently accessed data. This includes:

- Map Tiles: Cache the most commonly requested map tiles at various zoom levels to speed up map loading times. Each tile can be identified by a unique key based on its geographic coordinates and zoom level.

- Search Results: Cache the results of common search queries, such as popular landmarks or addresses, to reduce latency for repeated searches.

- User Sessions: Store session data, including user preferences and recent searches, to personalize the user experience without querying the database repeatedly.

-

Local Caching:

Implement local caching on the client side (e.g., mobile apps, web browsers) to store recently viewed map tiles and search results. This reduces redundant network requests and improves the user experience, especially in areas with poor connectivity.

-

Cache Invalidation:

Cache invalidation bounds how stale a served tile or traffic reading can be. Two mechanisms combine:

- Time-based Expiration: Set a time-to-live (TTL) for each cached item, after which it is automatically refreshed from the source data.

- Event-driven Invalidation: Invalidate cache entries when underlying data changes, such as when a new road is added to the map or when traffic conditions change.

See Caching.

#### The usage of CDN

A Content Delivery Network (CDN) is used to serve static assets like icons, stylesheets, and scripts. By caching these assets at edge locations around the world, the CDN reduces latency for end-users and decreases the load on the origin servers.

#### Analytics

For the analysis of large datasets, such as traffic patterns and map usage statistics, big data processing tools like Apache Hadoop and Spark are employed. These tools run over the historical TrafficSnapshot and usage data in scheduled batches, where results are needed within hours rather than seconds. For real-time analytics, technologies such as Apache Kafka and Apache Flink process data streams as they arrive, so current traffic conditions reflect location pings within seconds of ingestion rather than waiting for the next batch.

### Real-time Traffic Service

The Real-time Traffic Service is responsible for processing and providing up-to-date traffic information to users. This service must handle a continuous stream of data from various sources, including user devices, sensors, and third-party feeds.

#### Key Components:

-

Data Ingestion: Real-time traffic data is ingested from multiple sources, including:

- User location updates from the Websocket Server.

- Traffic sensors and cameras deployed on roads.

- Third-party data providers offering traffic updates.

-

Data Processing:

The Data Processing component reads real-time traffic data from the Message Queue and stores it in the Database. For data analytics, it is necessary to analyze the current traffic conditions and travel times for each Road. Subsequently, the analyzed data is updated in the cache.

- Stream Processing: Utilize a stream processing framework such as Apache Kafka Streams or Apache Flink to handle incoming traffic data in real-time.
Refer to the stream processing section for more details.

- Traffic Pattern Analysis: Implement machine learning algorithms to identify anomalies, forecast traffic congestion, and calculate travel times.

- Aggregation: Compile data over specific time intervals to provide a snapshot of the current traffic conditions.

-

Data Storage:

- Store processed traffic data in a time-series database for historical analysis and real-time access.

- Use a spatial database to correlate traffic data with specific road segments.

-

Data Dissemination:

- Push notifications to inform users about traffic incidents or congestions.

- Update map overlays with color-coded traffic conditions.

-

Request Handler:

- Provide RESTful APIs for clients to access real-time traffic information.

- Support filtering by geographic area, road segments, or user preferences.

### Routing Service

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
