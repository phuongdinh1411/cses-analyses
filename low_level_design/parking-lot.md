---
layout: simple
title: "Design Parking Lot"
permalink: /low_level_design/parking-lot
---

# Design Parking Lot

**Difficulty**: Easy | **Source**: [awesome-low-level-design](https://github.com/ashishps1/awesome-low-level-design/blob/main/problems/parking-lot.md)

---

## Requirements

1. Multiple levels, each with parking spots
2. Different vehicle types: cars, motorcycles, trucks
3. Each spot accommodates a specific vehicle type
4. System assigns spot on entry, releases on exit
5. Real-time tracking of spot availability
6. Multiple entry/exit points with concurrent access

---

## Class Diagram

![Class Diagram](https://raw.githubusercontent.com/ashishps1/awesome-low-level-design/main/class-diagrams/parkinglot-class-diagram.png)

---

## Classes, Interfaces and Enumerations

| Class/Interface | Description |
|----------------|-------------|
| **ParkingLot** | Singleton; maintains list of levels, methods to park/unpark |
| **ParkingFloor** | A level with list of spots; handles parking within that level |
| **ParkingSpot** | Individual spot; tracks availability and current vehicle |
| **Vehicle** | Abstract base class; extended by Car, Motorcycle, Truck |
| **VehicleSize** | Enum for vehicle types |

---

## Design Patterns Used

| Pattern | Application |
|---------|------------|
| **Singleton** | ParkingLot has a single instance managing the entire system |
| **Factory** (optional) | Create vehicles based on type without exposing instantiation logic |
| **Observer** (optional) | Notify displays or systems when spot availability changes |

---

## Code Implementations

| Language | Source Code |
|----------|-----------|
| Java | [View on GitHub](https://github.com/ashishps1/awesome-low-level-design/tree/main/solutions/java/src/parkinglot) |
| Python | [View on GitHub](https://github.com/ashishps1/awesome-low-level-design/tree/main/solutions/python/parkinglot) |
| C++ | [View on GitHub](https://github.com/ashishps1/awesome-low-level-design/tree/main/solutions/cpp/parkinglot) |
| C# | [View on GitHub](https://github.com/ashishps1/awesome-low-level-design/tree/main/solutions/csharp/parkinglot) |
| Go | [View on GitHub](https://github.com/ashishps1/awesome-low-level-design/tree/main/solutions/golang/parking_lot) |
