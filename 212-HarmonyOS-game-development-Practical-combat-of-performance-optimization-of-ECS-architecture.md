# HarmonyOS game development: Practical combat of performance optimization of ECS architecture

> ECS architecture is like the Lego building blocks developed by game development - if you use it correctly, you can build a skyscraper, but if you use it wrong, you will have a bunch of parts.This article combines experience in car game projects to share ECS' performance optimization tips under Hongmeng.


## 1. Component design: "Lego block" philosophy for lightweight data

### 1. Memory slimming technique for tuple components
Defining components with tuples is like pinching Lego pieces, each component does only one thing:
```cj
// Position component (2 Floats, 8 bytes)
typealias Position = (x: Float, y: Float)

// Animation component (status ID only, 1 byte)
enum AnimState { | Idle | Run | Jump }

// Role entity (combining two components)
let playerEntity = (position: Position(x: 10.5, y: 20.3), animState: AnimState.Run)
```  

**Optimization Points**:
- Avoid large structures, each component is controlled within 16 bytes
- State class components replace boolean/integer with enumeration (1 byte)


### 2. Component pool reuse policy
In racing games, reusing components is more efficient than creating new ones:
```cj
// Component pool design
class ComponentPool<T> {
    private var pool: [T] = []
    
    func borrow() -> T {
        if pool.isEmpty {
            return createNew()
        } else {
            return pool.popLast()!
        }
    }
    
    func recycle(component: T) {
        pool.append(component)
    }
}

// Use example (particle effect component pool)
let particlePool = ComponentPool<Position>()
```  


## 2. System scheduling: "blocking tactics" of multi-thread traversal

### 1. Parallel optimization of interval segmentation
In Monster AI system, block processing is 3 times faster than single thread:
```cj
func MonsterAISystem(monsters: [Entity]) {
    let threadCount = 4
    let chunkSize = monsters.count / threadCount
    let tasks = (0..threadCount).map { idx in
        async {
            let start = idx * chunkSize
            let end = (idx == threadCount-1) ? monsters.count : (idx+1)*chunkSize
            for i in start..end {
                updateMonsterAI(monsters[i])
            }
        }
    }
    awaitAll(tasks)
}
```  

### 2. Thread-safe component updates
Avoid lock competition with immutable components (for rendering systems):
```cj
// Immutable position component
typealias ImmutablePos = (x: Float, y: Float)

// Thread-safe update method
func moveEntity(entity: inout (pos: ImmutablePos, anim: AnimState), dx: Float, dy: Float) {
    entity.pos = (x: entity.pos.x + dx, y: entity.pos.y + dy)
}
```  


## 3. Memory optimization: "Cache-friendly" layout in SoA mode

### 1. Performance comparison of AoS vs SoA
In shooting games, SoA is 40% more rendering efficiency than AoS:
```cj
// AoS mode (traditional layout)
struct EntityAoS {
    var pos: Position
    var health: Int
}

// SoA mode (cache-friendly)
typealias PosArray = [Position]
typealias HealthArray = [Int]

let allPositions: PosArray = [...]
let allHealths: HealthArray = [...]
```  

### 2. SoA’s practical conversion
Conversion function from AoS to SoA (reducing memory fragmentation):
```cj
func convertToSoA(entities: [EntityAoS]) -> (PosArray, HealthArray) {
    let positions = entities.map { $0.pos }
    let healths = entities.map { $0.health }
    return (positions, healths)
}
```  


## 4. Practical cases: ECS optimization of racing games

### 1. Component design plan
```cj
// Racing components (lightweight tuple)
typealias CarControl = (steer: Float, throttle: Float)
typealias CarPhysics = (speed: Float, angle: Float)
typealias CarRender = (modelId: Int, color: UInt32)

// Racing entity (combining three components)
let raceCar = (control: CarControl(steer: 0, throttle: 1),
               physics: CarPhysics(speed: 0, angle: 0),
               render: CarRender(modelId: 101, color: 0xFF00FF00))
```  

### 2. System scheduling optimization
```cj
// Physical system (block calculation)
func PhysicsSystem(cars: [Entity]) {
    let chunks = divideIntoChunks(cars, chunkCount: 4)
    let tasks = chunks.map { chunk in
        async {
            for car in chunk {
                updatePhysics(car)
            }
        }
    }
    awaitAll(tasks)
}
```  


## 5. Avoiding Pits: "Blood and Tears" developed by ECS

1. **Component expansion trap**:
Performance starts to degrade when a single component exceeds 32 bytes. It is recommended to split into multiple widgets.

2. **Misconceptions about thread competition**:
Avoid multiple systems modifying the same component at the same time and decoupling with event systems

3. **SoA over-optimization**:
Small games (<1000 entities) are easier to use AoS, and large games are converted to SoA
