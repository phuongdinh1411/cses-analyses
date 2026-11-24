---
layout: simple
title: "Geospatial Search — System Design School"
permalink: /system_design/sds/concepts/domain-geospatial
---

System Design School

- Learn

- Practice

- Primer

- Roadmap

- Pricing

Ask AI TutorStart learning

Lessons

Your progress0%

AllSaved

Concurrency & Transactions

Distributed Systems

Search, Feeds & Spatial

Search Engine Mechanics

- Inverted Index Fundamentals

- TF-IDF Scoring Explained

- BM25 and Parameter Tuning

- Elasticsearch Architecture Essentials

- Advanced Search Patterns

Feeds & Ranking

- Two-Stage Ranking

Geospatial Search

- Geospatial Search Introduction

- Geohash

- QuadTrees

- H3 Hexagonal Hierarchical Spatial Index

- Space-Filling Curves and Hilbert’s Curve

- Google's S2 Library

- Designing a Map Rendering Service

- Choosing a Spatial Index

Specialized Systems & Data Structures

# Geospatial Search Introduction

Start quizSave

Proximity search asks a database for every point within a given distance of a target coordinate (lat, lng). Standard relational indexes organize records along one ordered dimension, so they cannot narrow latitude and longitude at the same time. Spatial indexing bridges this gap by organizing two-dimensional coordinates into grids or hierarchical trees that prune distant regions before exact distance math runs.

## Why B-Trees Fail on 2D Range Queries

A B-tree stores keys in one linear sort order. That order supports exact lookups and range scans on a single column such as a timestamp or user ID. Proximity search requires filtering on two independent coordinates simultaneously: latitude (lat) and longitude (lng).

Indexing lat alone lets the database jump directly to a horizontal band around the target latitude. Every record in that band still spans all longitudes around the globe, so the engine must inspect thousands of distant east-west candidates and run distance math on each one. Adding a separate B-tree on lng creates the same problem along a vertical north-south strip, and intersecting two large candidate lists in memory remains expensive.

A composite B-tree index on (lat, lng) does not solve two-dimensional range queries either. In a composite index, records sort first by lat and break ties by lng. A range condition such as lat BETWEEN 40.74 AND 40.77 spans many distinct latitude values, so the longitude values inside that range appear out of order. The database can use the index to bound lat, then must scan every matching row to check lng.

Computing spherical distance for every row in a large dataset does not scale. Exact distance on Earth uses the Haversine formula, which computes great-circle distance between two (lat, lng) pairs using trigonometric functions. Spatial indexes turn that full scan into a two-stage query:

- Coarse filter (index lookup): Use a bounding box or spatial cell index to discard points far outside the search radius.

- Exact filter (distance refinement): Compute Haversine distance only on the small candidate set returned by the index.

Bounding box. A bounding box is the smallest axis-aligned rectangle (min_lat, min_lng) to (max_lat, max_lng) that encloses a circular search radius. Checking whether a point lies inside a rectangle takes four numeric comparisons, which avoids trigonometry until the final candidate check.

## Two Families of Spatial Indexes

Spatial indexes fall into two main architectural families: adaptive trees that partition two-dimensional space directly, and fixed grids that map two-dimensional cells onto one-dimensional keys.

### Adaptive Tree Partitioning

A QuadTree partitions a two-dimensional plane recursively into four equal quadrants: northwest, northeast, southwest, and southeast. Each leaf node holds up to a configured capacity of points. When an insertion pushes a leaf over capacity, the leaf splits into four child quadrants and redistributes its points.

Because splits happen only where points accumulate, tree depth adapts to local density. Dense urban centers subdivide deeply so each leaf remains small, while sparse rural regions stay as single large cells. A range query starts at the root and descends only into quadrants whose bounding boxes intersect the query rectangle, pruning entire subtrees in one comparison.

Tree-based indexes carry a write trade-off. When stored locations move frequently or points are deleted in bulk, nodes must split, merge, or rebalance. Maintaining balanced spatial trees also requires either a dedicated in-memory service or a database spatial extension such as PostGIS GiST (which implements an R-tree variant over bounding rectangles).

### Grid-to-1D Key Mapping

Grid-based indexes cover the Earth with a deterministic hierarchy of cells and assign each cell a one-dimensional identifier. Nearby cells usually receive nearby identifiers or shared string prefixes. Because each location becomes a single scalar string or 64-bit integer, a standard B-tree index or sorted set can store and query it without custom spatial tree code.

Geohash is the simplest member of this family. It alternates binary splits of longitude and latitude, interleaves the resulting bits, and encodes every 5 bits as a base32 character. Because 5 bits represent 32 values, each extra character subdivides a cell into 32 smaller subcells. Nearby points typically share a prefix, turning a proximity query into a standard B-tree prefix scan.

Grid-based updates are inexpensive because moving a point overwrites one scalar column or sorted-set entry without rebalancing a shared tree. The trade-off is fixed cell geometry: dense areas pack many records into one cell while sparse areas leave empty cells unused, and points near cell borders require querying adjacent neighbor cells.

## Comparing Adaptive Trees and Grid Indexes

Data distribution, update rate, and database support determine which family fits a workload.

FactorAdaptive Tree (QuadTree / R-Tree)Grid-to-1D Key (Geohash / H3 / S2)

Dense clustersSubdivides deeper automaticallyFixed cell size at a chosen precision

Sparse regionsUses a single large leaf cellEmpty cells take no DB rows, but queries span more cells

Write and update costRequires splits, merges, or rebalancingDirect scalar key update

Database supportNeeds spatial extension or custom serviceWorks with standard B-tree or sorted-set index

Query patternRecursive bounding-box pruningPrefix or cell-ID IN (...) lookup plus exact filter

## Geometric Limits of Rectangular Grids

Rectangular latitude-longitude grids introduce three geometric issues that motivate more advanced spatial indexes:

- Boundary discontinuities: Two points meters apart on opposite sides of a grid line receive different cell keys. Queries must inspect the center cell plus surrounding neighbor cells before running the exact distance filter.

- Latitude distortion: Lines of longitude converge toward the poles. A rectangular cell defined by fixed degree increments spans roughly 40,075 km around the equator divided by its horizontal grid count, but narrows by a factor of cos(latitude) as latitude moves north or south.

- Non-uniform neighbor distances: A square cell has 4 edge neighbors at distance d and 4 diagonal corner neighbors at distance √2·d ≈ 1.414d. That mismatch introduces directional bias in radius queries and spatial heatmaps.

## Advanced Spatial Indexes

Modern production systems refine grid-based indexing to correct rectangular distortion and boundary jumps:

- H3 Hexagonal Indexing projects Earth onto a 20-faced icosahedron and tiles it with hexagons. Each hexagon has 6 neighbors at one uniform center-to-center distance, removing the corner-versus-edge bias of squares.

- Google S2 projects the sphere onto a cube, subdivides each face hierarchically, and orders cells along a Hilbert curve into 64-bit integer IDs. Cube projection reduces polar area distortion compared to equirectangular grids.

- Space-Filling Curves (Hilbert curves) improve how two-dimensional grids map onto one-dimensional keys. While simple bit interleaving (Z-order) makes sudden spatial jumps across major boundaries, a Hilbert curve keeps consecutive one-dimensional keys adjacent in two-dimensional space more consistently.

The next lessons examine each technique in detail: Geohash, QuadTrees, H3 Hexagonal Indexing, Space-Filling Curves, and Google S2.

Explain

Add to Chat

Start QuizLoading

Send feedback
