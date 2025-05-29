
# HarmonyOS Next struct and mut function: Boundary control of variable value types

In HarmonyOS Next development, `struct` is the core carrier of value type, and its immutability ensures the thread safety and state isolation of data.The mut function, as the only way to allow modification of struct instances, achieves controllable variability through strict scope restrictions.This article is based on the document "0010 Creating a struct Example - Struct Type - Cangjie Programming Language Development Guide - Learning Cangjie Language.docx", and deeply analyzes the collaborative rules and practical scenarios of `struct` and `mut` functions.


## 1. Syntax rules and scope restrictions of mut function

### 1.1 Required modifiers for mut function
The mut function must be modified with the mut keyword, otherwise the member variables of the struct instance cannot be modified.
```typescript  
struct Counter {  
  var count: Int64 = 0  
public mut func increment() { // Mut modifier must be added
count += 1 // Legal modification
  }  
}  
var counter = Counter()  
counter.increment() // count becomes 1 after calling the mut function
```  

### 1.2 Special semantic limitations of this
Inside the mut function, `this` allows modifying instance members, but prohibits being captured by closures or nested functions.
```typescript  
struct Foo {  
  var value: Int64 = 0  
  public mut func update() {  
let closure = { => this.value = 1 } // Error: This is not captured
value = 2 // Direct modification is legal
  }  
}  
```  

### 1.3 Let's declare instance call prohibition
The `struct` instance declared using `let` is immutable, and the call to the `mut` function is prohibited during the compilation period.
```typescript  
let fixedCounter = Counter()  
// fixedCounter.increment() // Error: The mut function cannot be called in the instance declared by let
```  


## 2. Applicable scenarios and implementation logic of mut function

### 2.1 Atomic operation of numerical counters
The atomic increment/decrement of value type instances is realized through the mut function to ensure the atomicity of the operation.
```typescript  
struct AtomicCounter {  
  var count: Int64 = 0  
  public mut func increment() {  
count += 1 // Atomic operation, value type isolation ensures thread safety
  }  
  public mut func decrement() {  
    count -= 1  
  }  
}  
var counter = AtomicCounter()  
counter.increment() // count = 1  
counter.decrement() // count = 0  
```  

### 2.2 In-situ modification of coordinate transformation
In a graphical rendering scenario, use the mut function to modify the coordinate instance in situ to reduce the overhead of copy generation.
```typescript  
struct Point {  
  var x: Int64, y: Int64  
  public mut func translate(dx: Int64, dy: Int64) {  
x += dx // Modify x coordinates in place
y += dy // Modify the y coordinate in place
  }  
}  
var p = Point(x: 10, y: 20)  
p.translate(dx: 5, dy: -3) // The coordinates become (15, 17)
```  

### 2.3 Dynamic operation of buffers
In data processing scenarios, the dynamic expansion and shrinking of the buffer is realized through the mut function.
```typescript  
struct Buffer {  
  var data: [UInt8]  
  public mut func append(data: [UInt8]) {  
self.data += data // Append data in place
  }  
  public mut func clear() {  
self.data.removeAll() // Clear the buffer
  }  
}  
var buffer = Buffer(data: [1, 2, 3])  
buffer.append(data: [4, 5]) // The buffer becomes [1,2,3,4,5]
```  


## 3. Coordination rules between mut function and interface

### 3.1 Declaration and implementation of mut function in interface
The mut` function declared in the interface must retain the mut` modifier when implementing the `struct`, and there is no need to modify the class when implementing it.
```typescript  
interface Mutable {  
mut func update(value: Int64) // Declare mut function in the interface
}  
struct MutStruct : Mutable {  
public mut func update(value: Int64) { /*...*/ } // struct must be added mut
}  
class MutClass : Mutable {  
public func update(value: Int64) { /*...*/ } // The class does not require mut modification
}  
```  

### 3.2 The replication semantic impact of interface assignment
When the `struct` instance is assigned to an interface variable, a copy will be generated, and the modification of the `mut` function only applies to the copy.
```typescript  
struct Value : Mutable {  
  public var data: Int64 = 0  
  public mut func update(value: Int64) { data = value }  
}  
var instance = Value()  
var i: Mutable = instance // Copy the instance, i holds the replica
i.update(value: 10) // Modify the data value of the copy
print(instance.data) // Output: 0 (the original instance has not been changed)
```  


## 4. Common Errors and Best Practices

### 4.1 Non-mut functions call mut functions
Non-mut functions prohibit calling mut functions, and need to be solved by reconstructing logic or improving the mutability level.
```typescript  
struct DataProcessor {  
  var data: String  
  public func process() {  
// cleanData() // Error: Non-mut functions prohibit calling mut functions
  }  
  public mut func cleanData() {  
    data = data.trim()  
  }  
  public mut func processAndClean() {  
cleanData() // The mut function can call other mut functions
  }  
}  
```  

### 4.2 Escape issues caused by closure capture
If the closure in the `mut` function tries to capture instance members, it will trigger a compile-time error and need to be replaced by parameter passing.
```typescript  
struct LogCounter {  
  var count: Int64 = 0  
  public mut func incrementAndLog() {  
let oldValue = count // Capture the current value
    count += 1  
log("Incremented from \(oldValue) to \(count)") // Avoid closure capture
  }  
}  
```  

### 4.3 Side effects of overuse of mut function
Avoid performing operations that are independent of instance state in the mut function and keep the function responsibilities single.
```typescript  
struct NetworkClient {  
  public mut func connect() {  
// Counterexample: Execute logging in mut function
    log("Connecting to server")  
// Legal modification: mark connection status
    isConnected = true  
  }  
}  
```  


## 5. Performance optimization and design principles

### 5.1 inout parameter reduces replication overhead
Use the `inout` modifier in function parameters to avoid generating copies when passing `struct` instance.
```typescript  
func processCounter(inout counter: AtomicCounter) {  
counter.increment() // directly modify the original value to reduce copy overhead
}  
var counter = AtomicCounter()  
processCounter(inout: &counter)  
```  

### 5.2 Batch operation merge
Merge multiple modifications into a single mut function call to reduce the number of replica generations.
```typescript  
struct Matrix {  
  var data: [[Float64]]  
  public mut func applyTransform(scale: Float64, offset: Int64) {  
data = data.map { $0.map { $0 * scale + Float64(offset) } } // Merge scale and offset operations
  }  
}  
```  

### 5.3 Immutable Design Priority
Use the mut function only when necessary, with priority to implementing logic through immutable designs that return new instances.
```typescript  
// Recommended: Immutable design
struct Point {  
  let x: Int64, y: Int64  
  public func moved(dx: Int64, dy: Int64) -> Point {  
    return Point(x: x + dx, y: y + dy)  
  }  
}  
var p = Point(x: 0, y: 0).moved(dx: 5, dy: 3) // Explicitly create a new instance

// Counterexample: Overuse of mut function
struct MutPoint {  
  var x: Int64, y: Int64  
  public mut func move(dx: Int64, dy: Int64) { x += dx; y += dy }  
}  
```  


## Conclusion
The collaboration between `struct` and `mut` functions reflects the refined design of HarmonyOS Next in value type variability control.In development, the following principles must be followed:
1. **Minimum mutability principle**: Use the `mut` function only when necessary to ensure the visibility and controllability of mutability operations;
2. **Scope isolation**: Use the `mut` function to limit the modification scope to avoid side effects from spreading outside the instance;
3. **Performance sensitive optimization**: For high-frequency modification scenarios, reduce the value type copy overhead in combination with `inout` parameter or batch operations.

By rationally using the mut function, developers can achieve safe and efficient variable operations in Hongmeng applications, especially in scenarios with high performance and security requirements such as real-time data processing and embedded device control, and give full play to the unique advantages of value types.
