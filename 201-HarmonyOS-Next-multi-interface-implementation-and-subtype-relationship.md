
# HarmonyOS Next multi-interface implementation and subtype relationship

In HarmonyOS Next development, multi-interface implementation and subtype relationships are the core technology for building flexible and scalable systems.By allowing types to implement multiple interfaces at the same time and strictly follow subtype conversion rules, developers can define type capabilities in a combined manner to implement the design pattern of "interfaces are capabilities units".This article combines the "Cangjie Programming Language Development Guide" to analyze the syntax rules, subtype collaborative logic and typical application scenarios implemented by multi-interfaces.


## 1. Syntax rules and capabilities combinations of multi-interface implementation
A type can implement multiple interfaces simultaneously through the `&` operator, and the syntax is as follows:
```cj
class TypeName <: InterfaceA & InterfaceB & InterfaceC {
// Implement member functions of all interfaces
}
```  

### 1. Merge implementation of interface members
When a type implements multiple interfaces, a unique implementation needs to be provided for the abstract members of each interface.If there are members of the same name between interfaces, they need to be handled uniformly in the implementation:
```cj
interface Printable { func print(): Unit }
interface Loggable { func print(message: String): Unit }

// Functions with the same name are distinguished by parameters
class Console <: Printable & Loggable {
public func print() { printLine() } // Implement Printable
public func print(message: String) { // Implement Loggable
        println("[LOG] \(message)")
    }
    private func printLine() { println("Default print") }
}
```  

### 2. Collaboration between interface inheritance and combination
The sub-interface can inherit multiple parent interfaces to form an interface chain:
```cj
interface Shape { func area(): Float64 }
interface Colorable { func setColor(color: String) }

// Sub-interface inherits multiple parent interfaces
interface ColoredShape <: Shape & Colorable {}

// Implementing the class requires all parent interface members
class Circle <: ColoredShape {
    private let radius: Float64
    private var color: String = "red"
    public func area(): Float64 { 3.14 * radius * radius }
    public func setColor(color: String) { self.color = color }
}
```  


## 2. Application of subtype relationships in multi-interface scenarios
### 1. Subtype determination of multi-interface type
If the type `T` implements interfaces `A` and `B`, then `T` is a subtype of `A` and `B` and can be used in any scenario where `A` or `B` is required:
```cj
interface A {}
interface B {}
class C <: A & B {}

let obj: A = C() // Legal: C is a subtype of A
let obj: B = C() // Legal: C is a subtype of B
```  

### 2. Multi-interface matching in generic constraints
Generic functions can be used to constrain the type of `where` clause to implement multiple interfaces to improve code reusability:
```cj
func process<T: Printable & Loggable>(item: T) {
item.print() // Call Printable interface
item.print(message: "Processing item") // Call the Loggable interface
}

let console = Console()
process(item: console) // Legal: Console implements dual interfaces
```  

### 3. Mixed use of interface and class inheritance
Abstract classes can be used as base classes for multi-interface implementations, providing default implementations of some interfaces:
```cj
abstract class AbstractDevice <: Communicable {
public func connect(): Bool { /* general connection logic */ return true }
public abstract func send(data: String) // Abstract function, subclass implementation
}

class WirelessDevice <: AbstractDevice & Configurable {
public func send(data: String) { /* Implement send logic */ }
public func configuration(settings: Dictionary<String, Any>) { /* Implement configuration interface */ }
}
```  


## 3. Typical scenarios for multi-interface implementation

### 1. Capability modeling of IoT devices
Smart devices often need to have communication, storage, display and other capabilities at the same time, and can be achieved through multiple interface combinations:
```cj
// Define the capability interface
interface Communicable { func send(data: String) }
interface Storable { func save(data: String) }
interface Displayable { func show(text: String) }

// Smart terminal implements all interfaces
class SmartTerminal <: Communicable & Storable & Displayable {
public func send(data: String) { /* Communication logic */ }
public func save(data: String) { /* Storage logic */ }
    public func show(text: String) { println(text) }
}

// Multi-capacity call
let terminal: SmartTerminal = SmartTerminal()
terminal.send("hello") // Communication capability
terminal.save("log") // Storage capability
terminal.show("status") // Display capability
```  

### 2. Combination optimization of algorithm interfaces
By combining sorting, searching, and filtering interfaces, a multifunctional data structure is realized:
```cj
interface Sorter {
    func sort<T: Comparable>(array: [T]): [T]
}

interface Searcher {
    func search<T: Equatable>(array: [T], target: T): Int
}

class Utility <: Sorter & Searcher {
    public func sort<T: Comparable>(array: [T]): [T] { array.sorted() }
    public func search<T: Equatable>(array: [T], target: T): Int {
        array.firstIndex(of: target) ?? -1
    }
}

// Use example
let util = Utility()
let sorted = util.sort(array: [3, 1, 2])
let index = util.search(array: sorted, target: 2)
```  

### 3. Capability expansion for existing types
Adding interface implementations to non-custom types via extension (`extend`) without modifying the original code:
```cj
// Add Loggable interface to Int type
extend Int <: Loggable {
    public func print(message: String) {
        println("\(message): \(self)")
    }
}

// Use example
let number: Int = 42
number.print(message: "value") // Output: value: 42
```  


## 4. Design principles and trap avoidance

### 1. Practice of Interface Isolation Principle (ISP)
Avoid unnecessary interfaces for type implementation and split into small-grained interfaces:
```cj
// Counterexample: Large interface results in redundant type implementation
interface AllInOne {
    func connect()
    func print()
    func encrypt()
}

// Positive example: Split into independent interface
interface Networkable { func connect() }
interface Printable { func print() }
interface Secureable { func encrypt() }
```  

### 2. Interface order and readability
The interface list is sorted by capability importance, and the core capability is pre-positioned:
```cj
class Robot <: Activatable & Movable & Communicable { 
// Activatable is the core capability, priority statement
}
```  

### 3. Visibility management of cross-packet interfaces
Ensure that both interface and implementation classes are `public` and are exported correctly to avoid cross-packet access failures:
```cj
package devices.core
public interface RemoteControllable {}
public class SmartTV <: RemoteControllable {}

// Other package references
import devices.core.*
let tv: RemoteControllable = SmartTV() // Legal
```  


## 5. In-depth application of subtype relationships: type-safe polymorphic scheduling
### 1. Dynamic distribution of multi-interface types
When the function parameter is interface type, the runtime calls the corresponding implementation according to the actual type:
```cj
func operate(device: Communicable & Storable) {
device.send("data") // Call the send implementation of the specific class
device.save("log") // Call the save implementation of the specific class
}

// Pass in different implementation classes and dynamic scheduling
let terminal: SmartTerminal = SmartTerminal()
operate(device: terminal) // Call SmartTerminal implementation
```  

### 2. Security guarantee for subtype conversion
Use the `is` operator to determine whether the object supports multiple interfaces to avoid invalid conversion:
```cj
let device: Any = SmartTerminal()
if device is Communicable && device is Storable {
    let communicable = device as! Communicable
    let storable = device as! Storable
// Secure access to members of different interfaces
}
```  


## 6. Summary: The architectural value of interface combination
HarmonyOS Next's multi-interface implementation and subtype relationship mechanism provides developers with the following core capabilities:
- **Support modularity**: Package different functions into independent interfaces, combine them on demand, and reduce coupling;
- **Flexible extension**: Add functions to existing types by implementing new interfaces, which complies with the principle of opening and closing;
- **Type Safety**: The compiler forces the interface to achieve integrity, and the conversion security is guaranteed through subtype relationships during runtime.
