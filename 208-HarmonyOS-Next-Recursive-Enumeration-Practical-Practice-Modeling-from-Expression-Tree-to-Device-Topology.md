# HarmonyOS Next Recursive Enumeration Practical Practice: Modeling from Expression Tree to Device Topology

> I still remember the first time I used recursive enumeration to model the topology of smart home devices, because the recursive termination condition was not handled properly, the stack overflow was caused. Debug discovered that the enumeration constructor lacked basic types until the early morning.Today I will sort out these practical experiences and help you avoid the pit of recursive enumeration and master this modeling tool.


## 1. Recursive enumeration: "Lego building blocks" of hierarchical data

### 1.1 Basic definitions and core rules
The essence of recursive enumeration is to allow the enumeration constructor to refer to its own type, just like building a multi-layer structure with Lego bricks of the same shape.Taking the topology of smart home devices as an example:

```cj
// Device topology enumeration (including devices and packets)
enum DeviceNode {
| Device(id: String, type: DeviceType) // Basic constructor: single device
| Group(name: String, children: [DeviceNode]) // Recursive constructor: Device grouping
}

// Device type enumeration
enum DeviceType { .Light, .Lock, .Sensor }
```  

**Core Rules**:
- Must include at least one non-recursive constructor (such as `Device`) as a recursive termination condition
- Recursive constructor parameters need to explicitly refer to the enumerated type (such as `children: [DeviceNode]`)


### 1.2 Expression tree modeling practice
Recursive enumerations represent arithmetic expressions, which are more concise than class inheritance:

```cj
// Enumeration of arithmetic expressions
enum Expr {
| Num(Int64) // Numbers
| Add(Expr, Expr) // Add
| Sub(Expr, Expr) // Subtraction
| Mul(Expr, Expr) // Multiplication
}

// Expression evaluation (recursive pattern matching)
func evaluate(expr: Expr) -> Int64 {
    match expr {
case .Num(n) => n // Basic situation: return the value directly
case .Add(l, r) => evaluate(l) + evaluate(r) // Recursively calculate left and right subexpressions
        case .Sub(l, r) => evaluate(l) - evaluate(r)
        case .Mul(l, r) => evaluate(l) * evaluate(r)
    }
}

// Build expression: 3 + (4 * 2)
let expr = Add(
    .Num(3),
    Mul(
        .Num(4),
        .Num(2)
    )
)

println(evaluate(expr)) // Output 11
```  


## 2. Pattern matching: the "deconstruction key" of recursive enumeration

### 2.1 Termination strategy for recursive matching
When matching patterns, the basic constructor must be processed first, and then the recursive constructor must be processed, just like peeling an onion:

```cj
// Calculate the total number of devices in the device topology
func countDevices(node: DeviceNode) -> Int {
    match node {
case .Device(_, _) => 1 // Basic situation: single device count 1
case .Group(_, children) => children.map(countDevices).reduce(0, +) // Recursively compute child nodes
    }
}

// Build a device topology
let topology = Group(
name: "living room",
    children: [
        .Device(id: "light001", type: .Light),
        Group(
name: "Security",
            children: [
                .Device(id: "sensor001", type: .Sensor),
                .Device(id: "lock001", type: .Lock)
            ]
        )
    ]
)

println(countDevices(topology)) // Output 3
```  

### 2.2 Matching techniques for nested structures
When dealing with multi-layer nesting, deep data can be extracted through ** binding:

```cj
// Find the device ID
func findDevice(id: String, node: DeviceNode) -> Bool {
    match node {
        case .Device(deviceId, _) => deviceId == id
        case .Group(_, children) => children.any { findDevice(id, $0) }
    }
}

println(findDevice("lock001", topology)) // Output true
```  


## 3. Practical scenario: topology management of smart home devices

### 3.1 Construction and traversal of device trees
Recursive enumeration is great for modeling device networks with hierarchical relationships:

```cj
// Device status enumeration
enum DeviceStatus { .Online, .Offline, .Error }

// Enumeration of device topology with state
enum DeviceTree {
    | DeviceInfo(id: String, type: DeviceType, status: DeviceStatus)
    | DeviceGroup(name: String, children: [DeviceTree])
}

// Build a device tree with state
let smartHome = DeviceGroup(
name: "Smart Home",
    children: [
        DeviceInfo(
            id: "light001",
            type: .Light,
            status: .Online
        ),
        DeviceGroup(
name: "Bedroom",
            children: [
                DeviceInfo(
                    id: "lock001",
                    type: .Lock,
                    status: .Offline
                )
            ]
        )
    ]
)
```  

### 3.2 Device status update and traversal optimization
Use **Iteration instead of recursion** to avoid stack overflow (for deep device trees):

```cj
// Iteratively update all device status
func updateStatus(root: DeviceTree, newStatus: DeviceStatus) {
    var stack = [root]
    
    while !stack.isEmpty {
        let node = stack.pop()!
        match node {
            case .DeviceInfo(id, type, _):
// Update the device status (the device API will be called in the actual project)
println("Update device \(id) status is \(newStatus)")
            case .DeviceGroup(_, children):
stack.append(contentsOf: children) // Children nodes are stacked
        }
    }
}

updateStatus(smartHome, .Online) // Output update log
```  


## 4. Performance optimization: "Pipe Protection Guide" for Recursive Enumeration

### 4.1 Three solutions for stack overflow
**Scenario**: When the depth of the device tree exceeds 100 layers, recursive traversal will cause stack overflow

#### Solution 1: Iterative traversal (most general)
```cj
// Iterative computing device tree depth
func calculateDepth(root: DeviceTree) -> Int {
    if case .DeviceInfo = root { return 1 }
    
    var maxDepth = 0
    var queue = [(node: root, depth: 1)]
    
    while !queue.isEmpty {
        let (node, depth) = queue.removeFirst()
        if case .DeviceGroup(_, let children) = node {
            maxDepth = max(maxDepth, depth)
            queue.append(contentsOf: children.map { ($0, depth + 1) })
        }
    }
    
    return maxDepth
}
```  

#### Solution 2: Tail recursive optimization (requires compiler support)
```cj
@tailrec
func calculateDepthTailRecursive(node: DeviceTree, currentDepth: Int = 1) -> Int {
    match node {
        case .DeviceInfo: return currentDepth
        case .DeviceGroup(_, children):
            let childDepths = children.map { calculateDepthTailRecursive($0, currentDepth + 1) }
            return childDepths.max() ?? currentDepth
    }
}
```  

#### Solution 3: Block processing (big data scenario)
```cj
// Block processing of deep equipment trees
func processLargeTree(root: DeviceTree) {
    let chunkSize = 100
    var nodes = [root]
    
    while !nodes.isEmpty {
        let chunk = nodes.splice(0, chunkSize)
        chunk.forEach { processNode($0) }
        nodes.append(contentsOf: chunk.flatMap {
            if case .DeviceGroup(_, let children) = $0 { return children }
            return []
        })
    }
}
```  


## 5. Enumeration philosophy in architectural design

In a distributed device management system, recursive enumeration has three major advantages over class inheritance:
1. **Lightweight Modeling**: Enumerations take up less memory than classes, suitable for resource-constrained devices
2. **Type Safety**: Pattern matching forces all constructors to avoid runtime errors
3. **Scalability**: Adding new device types only requires modifying the enumeration definition without changing the traversal logic

**Lesson of Blood and Tears**: I used class inheritance to model the device tree in the on-board system. All traversal functions need to be modified when adding new device types; after using recursive enumeration, the new device types only need to add a constructor, and the traversal logic is completely reused, and the maintenance cost is reduced by 80%.


## Conclusion
Recursive enumeration is a powerful tool for processing hierarchical data in HarmonyOS Next. The key to mastering it lies in understanding the core logic of "the basic constructor as a recursive termination condition".From expression trees to device topology, recursive enumeration makes modeling of complex data structures as intuitive as Lego.In actual projects, combining iterative optimization and tail recursion techniques can allow this tool to find the best balance between performance and readability.
