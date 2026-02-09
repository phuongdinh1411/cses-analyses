# Through the Desert

## Problem Information
- **Source:** UVA
- **Difficulty:** Secret
- **Time Limit:** 1000ms
- **Memory Limit:** 512MB

## Problem Statement

Cross a desert with a jeep. The fuel tank must be large enough to complete the journey. Events along the way:
- **Fuel consumption n**: Truck uses n litres per 100 km
- **Leak**: Adds 1 litre/km leak rate (cumulative)
- **Gas station**: Fill up tank completely
- **Mechanic**: Fixes all leaks (leak rate becomes 0)
- **Goal**: Journey's end

Find the minimum tank size (in litres) to complete the journey.

## Input Format
- Multiple test cases (up to 50 events each)
- Events given by: distance (km from start) and event type
- First event: "0 Fuel consumption n"
- Last event: "d Goal"
- Events sorted by distance
- Input ends with "0 Fuel consumption 0"

## Output Format
For each test case, print minimum tank volume with 3 decimal places.

## Example
```
Input:
0 Fuel consumption 10
100 Gas station
200 Goal
0 Fuel consumption 0

Output:
10.000
```
Travel 200km with consumption 10L/100km, refuel at 100km. First 100km needs 10L, second 100km needs 10L. Since we refuel at 100km, tank capacity of 10L is sufficient.

## Solution

### Approach
Simulate the journey backwards or use binary search on tank size.

Key insight: The minimum tank size is determined by the segment that requires the most fuel between refills (gas stations or start).

For each segment between gas stations:
- Track fuel consumption rate and leak rate
- Calculate fuel needed for each sub-segment
- The tank must hold enough for the worst segment

### Python Solution

```python
def solve():
  while True:
    events = []

    while True:
      line = input().split()
      dist = int(line[0])
      event_type = line[1]

      if event_type == "Fuel":
        consumption = int(line[3])
        events.append((dist, "fuel", consumption))

        if dist == 0 and consumption == 0:
          return

      elif event_type == "Leak":
        events.append((dist, "leak", 0))
      elif event_type == "Gas":
        events.append((dist, "gas", 0))
      elif event_type == "Mechanic":
        events.append((dist, "mechanic", 0))
      elif event_type == "Goal":
        events.append((dist, "goal", 0))
        break

    # Simulate to find minimum tank size
    # Binary search on tank capacity

    def can_complete(tank_capacity):
      fuel = tank_capacity
      consumption = 0  # litres per 100 km
      leak_rate = 0    # litres per km
      prev_dist = 0

      for dist, event, val in events:
        delta = dist - prev_dist

        if delta > 0:
          # Fuel used = (consumption/100) * delta + leak_rate * delta
          fuel_used = (consumption / 100) * delta + leak_rate * delta
          fuel -= fuel_used

          if fuel < -1e-9:
            return False

        if event == "fuel":
          consumption = val
        elif event == "leak":
          leak_rate += 1
        elif event == "gas":
          fuel = tank_capacity
        elif event == "mechanic":
          leak_rate = 0
        elif event == "goal":
          pass

        prev_dist = dist

      return fuel >= -1e-9

    # Binary search for minimum tank capacity
    lo, hi = 0.0, 1e9

    for _ in range(100):  # Enough iterations for precision
      mid = (lo + hi) / 2
      if can_complete(mid):
        hi = mid
      else:
        lo = mid

    print(f"{hi:.3f}")

if __name__ == "__main__":
  solve()
```

### Alternative Solution - Segment Analysis

```python
def solve():
  while True:
    events = []

    while True:
      parts = input().split()
      dist = int(parts[0])
      event = parts[1]

      if event == "Fuel":
        rate = int(parts[3])
        if dist == 0 and rate == 0:
          return
        events.append((dist, "fuel", rate))
      elif event == "Leak":
        events.append((dist, "leak", 0))
      elif event == "Gas":
        events.append((dist, "gas", 0))
      elif event == "Mechanic":
        events.append((dist, "mech", 0))
      elif event == "Goal":
        events.append((dist, "goal", 0))
        break

    # Find min tank by checking each segment between gas stations
    # Tank must be large enough for worst segment

    def simulate(capacity):
      tank = capacity
      cons = 0
      leak = 0
      pos = 0

      for d, e, v in events:
        dist = d - pos

        if dist > 0:
          usage = cons * dist / 100 + leak * dist
          tank -= usage
          if tank < -1e-9:
            return False

        if e == "fuel":
          cons = v
        elif e == "leak":
          leak += 1
        elif e == "gas":
          tank = capacity
        elif e == "mech":
          leak = 0

        pos = d

      return True

    lo, hi = 0, 2e7
    for _ in range(100):
      mid = (lo + hi) / 2
      if simulate(mid):
        hi = mid
      else:
        lo = mid

    print(f"{hi:.3f}")

if __name__ == "__main__":
  solve()
```

### Complexity Analysis
- **Time Complexity:** O(E × log(MAX_CAPACITY)) where E is number of events
- **Space Complexity:** O(E)

### Key Insight
Binary search on tank capacity. For each candidate capacity, simulate the journey: track fuel level, consumption rate, and leak rate. The tank is filled at gas stations and at the start. Leaks accumulate (each "Leak" event adds 1 L/km). Mechanic resets leak rate to 0. The minimum capacity is the smallest value that allows completing the journey without running out.
