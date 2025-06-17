
# HarmonyOS Next struct and interface collaborative practice: type adaptation and polymorphic design

In HarmonyOS Next development, the collaborative use of `struct` and interface (interface) is an important means to achieve polymorphism and type adaptation.Although `struct` does not support inheritance as a value type, its implementation ability of interfaces can meet the needs of lightweight polymorphic scenarios.This article combines the document "0010 Creating a struct Example - Struct Type - Cangjie Programming Language Development Guide - Learning Cangjie Language.docx" to analyze the collaborative rules and practical applications of `struct` and interfaces.


## 1. Basic rules for implementing interfaces in struct

### 1.1 Interface definition and struct implementation
`struct` can implement interfaces through the `<:` keyword, and it is necessary to ensure that all interface members are implemented.

**Example: Geometric interface and struct implementation**
```typescript  
interface Shape {  
func area(): Float64 // Calculate area
var color: String { get set } // Color attribute
}  
struct Circle : Shape {  
  var radius: Float64  
  var color: String = "red"  
  public func area(): Float64 {  
    return 3.14159 * radius * radius  
  }  
}  
```  

### 1.2 Visibility requirements for interface members
Members declared in the interface must have the same or higher access permissions in `struct`.

**Error case: Interface member permissions are inconsistent**
```typescript  
interface PublicInterface {  
  var data: String { get set }  
}  
struct PrivateData : PublicInterface {  
private var data: String // Error: private member cannot meet the public interface requirements
}  
```  

### 1.3 Interface adaptation of mut function
If the `mut` function is declared in the interface, the `mut` modifier must be used when implementing the `struct`, and there is no need to modify the class when implementing it.

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


## 2. The speciality of the polymorphism of value type

### 2.1 Copy semantics of interface assignment
When the `struct` instance is assigned to an interface type variable, value copying will occur. The interface variable holds a copy of `struct`, and the modification will not affect the original instance.

**Status isolation case**
```typescript  
struct Counter : Mutable {  
  public var count: Int64 = 0  
  public mut func update(value: Int64) { count = value }  
}  
var counter = Counter()  
var i: Mutable = counter // Copy the instance, i holds the copy
i.update(value: 10) // Modify the count value of the copy
print(counter.count) // Output: 0 (the original instance has not been changed)
```  

### 2.2 Limitations of interface method calls
When `struct` calls the mut` function through the interface, the actual operation is a copy and the original instance state cannot be modified.

**Principle Analysis**
```typescript  
struct Point : Moveable {  
  public var x: Int64, y: Int64  
  public mut func move(dx: Int64, dy: Int64) {  
    x += dx  
    y += dy  
  }  
}  
var p = Point(x: 0, y: 0)  
var moveable: Moveable = p  
moveable.move(dx: 5, dy: 3) // In the copy operation, the coordinates of p are still (0,0)
```  

### 2.3 Core differences from class polymorphisms
| **Properties** | **struct value type polymorphism** | **class reference type polymorphism** |
|------------------|-----------------------------|-----------------------------|  
| Assignment behavior | Copy instance, status isolation | Shared reference, status synchronization |
| mut function affects the range | only act on the interface variable copy | act on the original instance |
| Memory overhead | Stack allocation, high replication efficiency | Heap allocation, indirect access by pointers |


## 3. Practical scenarios: interface abstraction and type adaptation

### 3.1 Polymorphic implementation of data parser
Through the interface unifies the parsing logic of different data formats, `struct` implements a specific parser.

```typescript  
interface DataParser {  
  func parse(data: String) -> Any  
}  
struct JsonParser : DataParser {  
  public func parse(data: String) -> Any {  
// JSON parsing logic
    return JSONDecoder().decode(data)  
  }  
}  
struct XmlParser : DataParser {  
  public func parse(data: String) -> Any {  
// XML parsing logic
    return XmlDecoder().decode(data)  
  }  
}  
//Use interface to call
func processData(parser: DataParser, data: String) {  
  let result = parser.parse(data: data)  
// Subsequent processing
}  
```  

### 3.2 Device driver interface adaptation
Define a general device interface, and the `struct` driver of different hardware implements this interface, which is convenient for unified management at the system level.

```typescript  
interface Device {  
  var deviceId: String { get }  
  func connect() -> Bool  
}  
struct UsbDevice : Device {  
  let deviceId: String  
  public func connect() -> Bool {  
// USB connection logic
    return UsbController.connect(deviceId)  
  }  
}  
struct BluetoothDevice : Device {  
  let deviceId: String  
  public func connect() -> Bool {  
// Bluetooth connection logic
    return BluetoothController.connect(deviceId)  
  }  
}  
```  

### 3.3 Dynamic switching of algorithm strategies
Through interface encapsulation algorithm logic, `struct` implements different strategies and dynamic selection at runtime.

```typescript  
interface SortStrategy {  
  func sort<T: Comparable>(array: [T]) -> [T]  
}  
struct QuickSort : SortStrategy {  
  public func sort<T: Comparable>(array: [T]) -> [T] {  
// Quick sorting implementation
  }  
struct BubbleSort : SortStrategy {  
  public func sort<T: Comparable>(array: [T]) -> [T] {  
// Bubble sorting implementation
  }  
}  
// Policy mode application
func sortArray<T: Comparable>(array: [T], strategy: SortStrategy) -> [T] {  
  return strategy.sort(array: array)  
}  
```  


## IV. Limitations and Best Practices

### 4.1 Avoid interfaces as variable state carriers
Since the interface assignment of `struct` will produce a copy, it is not suitable for scenarios where shared state is required.

**Counterexample: Trying to modify the original struct state through the interface**
```typescript  
struct SharedState : Mutable {  
  public var value: Int64 = 0  
  public mut func update(value: Int64) { self.value = value }  
}  
var state = SharedState()  
var i: Mutable = state  
i.update(value: 10)  
print(state.value) // Output: 0 (expected inconsistent)
```  

### 4.2 Priority to using classes to implement complex polymorphism
For polymorphic scenarios that require shared state or complex behavior, it is recommended to use classes instead of `struct`.

**Recommended scenario: Graphic renderer (context state required)**
```typescript  
class Renderer : GraphicRenderer {  
private var context: RenderContext // Internal state
  public func render(shape: Shape) {  
// Rendering logic that depends on context
  }  
}  
```  

### 4.3 Utilization of type checking during compilation period
With the help of strict verification of interface implementation by the compiler, ensure that `struct` meets all interface constraints and avoids runtime errors.

```typescript  
struct IncompleteShape : Shape {  
  var color: String = "blue"  
// The area() function is not implemented, and an error occurred during the compilation period
}  
```  


## 5. Summary: Applicable boundaries of struct interface collaboration

The collaboration between `struct` and interfaces is suitable for the following scenarios in HarmonyOS Next:
- **Lightweight polymorphic**: stateless or read-only logic such as simple data conversion, algorithm strategies;
- **Value type adaptation**: Scenarios where independent replicas need to be passed (such as cross-thread data passing);
- **Interface Unified Abstraction**: Block the differences in different `struct` implementations and provide a consistent calling interface.

Note:
1. **状态独立性**：始终将接口变量视为`struct`的副本，避免依赖状态共享；  
2. **Performance sensitive scenarios**: Use the stack allocation characteristics of value types to prioritize the implementation of interfaces in high-frequency calling scenarios;
3. **Design mode limitation**: Policy mode, factory mode, etc. can cooperate with the `struct` interface, while observer mode and other modes that rely on shared state are more suitable for class implementation.

By rationally using the combination of `struct` and interfaces, developers can build a simple and efficient polymorphic system in Hongmeng applications, especially in performance-sensitive scenarios such as embedded devices and lightweight services, and give full play to the advantages of value types.
