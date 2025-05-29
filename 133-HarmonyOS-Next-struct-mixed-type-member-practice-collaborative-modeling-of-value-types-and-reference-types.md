
# HarmonyOS Next struct mixed type member practice: collaborative modeling of value types and reference types

In HarmonyOS Next development, `struct` allows for a mixed member of value type and reference type (such as `class`), a feature that balances data independence and sharing capabilities in data modeling.Combined with the document "0010 Creating a struct Example - Struct Type - Cangjie Programming Language Development Guide - Learning Cangjie Language.docx", this article analyzes the design rules and practical scenarios of mixed-type members, covering memory behavior, access control and performance optimization.


## 1. Definition and memory rules of mixed type members

### 1.1 Coexistence of value types and reference types
The `struct` member can contain both value types (such as `Int64/struct`) and reference types (such as `class`). The two are stored in memory differently:
- **Value type member**: directly store data values ​​and generate a copy when copying.
- **Reference type member**: Stores the object reference address and shares the same object when copying.

```typescript  
class SharedLogic {  
func process() { /* Shared logic */ }
}  
struct DataContainer {  
var id: Int64 // Value type member
let logic: SharedLogic // Reference type member (immutable reference)
var config: ConfigStruct // Value type structure member
}  
```  

### 1.2 Differentiated performance of replication behavior
```typescript  
let logic = SharedLogic()  
var c1 = DataContainer(id: 1, logic: logic, config: ConfigStruct())  
var c2 = c1 // Copy struct instance
c1.id = 2 // c2.id is still 1 (value type isolation)
c1.logic.process() // c2.logic synchronous call (reference type sharing)
```  


## 2. Mixed types of access control and thread safety

### 2.1 Immutability design of reference type members
Declare reference type members through `let` to avoid accidentally modifying the reference address and improve thread safety.
```typescript  
struct SafeContainer {  
let sharedObject: SharedData // Immutable reference
  var value: Int64  
  public init(sharedObject: SharedData, value: Int64) {  
self.sharedObject = sharedObject // Reference cannot be changed after initialization
    self.value = value  
  }  
}  
```  

### 2.2 Thread safety advantages of value type members
The replication isolation feature of value type members is naturally suitable for multi-threaded scenarios and avoids race conditions.
```typescript  
struct ThreadSafeData {  
var counter: Int64 // Value type counter
let lock: Lock // Reference type lock (guaranteed atomicity)
  public mut func increment() {  
    lock.acquire()  
    defer { lock.release() }  
counter += 1 // Value type members cooperate with lock to achieve thread safety
  }  
}  
```  


## 3. Practical scenarios: typical applications of mixed types

### 3.1 Device status modeling: value type data + reference type driver
```typescript  
class DeviceDriver {  
func readSensor() -> Float64 { /* Hardware Read Logic */ }
}  
struct SensorData {  
let driver: DeviceDriver // Reference type: Driver logic
var temperature: Float64 // Value type: Sensor value
  public mut func update() {  
temperature = driver.readSensor() // Get data through reference type and update value type members
  }  
}  
```  

### 3.2 UI component status: immutable configuration + variable rendering data
```typescript  
struct UIConfig {  
let font: Font // Value type: Font configuration
let color: Color // Value type: Color configuration
}  
class RenderContext {  
var canvas: Canvas // Reference type: Rendering context
}  
struct ButtonState {  
  let config: UIConfig // 不可变值类型配置  
var isPressed: Bool // Variable value type state
let context: RenderContext // Reference type: Shared rendering resource
}  
```  

### 3.3 Network request encapsulation: value type parameter + reference type callback
```typescript  
struct RequestParams {  
let url: String // Value type: Request address
let method: String // Value type: Request method
}  
class RequestCallback {  
func onSuccess(data: Data) { /* callback logic */ }
}  
struct NetworkRequest {  
var params: RequestParams // Value type: Request parameter
let callback: RequestCallback // Reference type: callback object
  public func send() {  
// Use params to initiate a request and process the result through callback
  }  
}  
```  


## 4. Common Errors and Best Practices

### 4.1 null reference risk for reference type members
**Error case**: Uninitialized reference type member causes a runtime crash.
```typescript  
struct Uninitialized {  
let obj: SharedObject // Not initialized
}  
// let instance = Uninitialized() // Error: Reference type member is not initialized
```  

**Solution**: Make sure that the reference type member is not empty in the constructor.
```typescript  
struct Initialized {  
  let obj: SharedObject  
public init(obj: SharedObject = SharedObject()) { // Default value initialization
    self.obj = obj  
  }  
}  
```  

### 4.2 Performance loss of hybrid type replication
**Counterexample**: The mixing of large-value type members and reference types leads to high replication overhead.
```typescript  
struct HeavyStruct {  
var largeData: [Int64] // Value type: 1000 element array
let handler: DataHandler // Reference type
}  
var h1 = HeavyStruct(largeData: Array(repeating: 0, count: 1000), handler: DataHandler())  
var h2 = h1 // Copy large array, poor performance
```  

**Optimization**: Split value types and reference types, copy on demand.
```typescript  
struct LightData {  
  var largeData: [Int64]  
}  
class HeavyHandler {  
  var handler: DataHandler  
}  
struct OptimizedStruct {  
var data: LightData // Independent value type
let handler: HeavyHandler // Shared reference type
}  
```  

### 4.3 Granularity management of access control
Avoid exposing the mutability of reference type members in `struct` and control access through value type members.
```typescript  
struct SecureContainer {  
private let internalObject: SharedObject // Private reference type
public var safeValue: Int64 // Public value type interface
  public func fetchValue() -> Int64 {  
return internalObject.calculate(safeValue) // Access through the value type interface
  }  
}  
```  


## 5. Design principles and performance optimization

### 5.1 Principle of separation of responsibilities
- **Value type member**: Store independent data to ensure state isolation.
- **Reference type member**: Encapsulate shared logic or resources to avoid repeated creation.

### 5.2 The principle of immutable priority
For reference type members that do not involve state changes, use the `let` declaration to ensure immutability.
```typescript  
struct ImmutableWrapper {  
let service: NetworkService // Immutable reference: Network service singleton
var request: RequestParams // Variable value type: Request parameter
}  
```  

### 5.3 Optimization of memory layout during compilation period
Use the compiler to optimize the memory alignment of value types to improve the access efficiency of mixed types.
```typescript  
struct AlignedStruct {  
var intValue: Int64 // 8 byte alignment
let objValue: SmallObject // Small object reference, compiler optimization pointer is targeted
}  
```  


## Conclusion
The hybrid type member design of `struct` is an important capability for flexible modeling in HarmonyOS Next.By reasonably combining value types and reference types, developers can find a balance between data independence, sharing logic and performance:
1. **Lightweight data value type**: Ensure simple state thread safety and copy isolation;
2. **Reference types for sharing logic**: Avoid duplicate resource occupation and improve efficiency;
3. **Access control refinement**: Accurately manage variability and visibility of members through `let/var` and access modifiers.

Mastering the design rules of hybrid types can build clear-level and efficient data models in Hongmeng applications, especially in scenarios such as IoT device control and complex UI component state management, so as to give full play to the advantages of different types of synergies.
