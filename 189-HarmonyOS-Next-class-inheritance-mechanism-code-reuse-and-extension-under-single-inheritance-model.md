
# HarmonyOS Next class inheritance mechanism: code reuse and extension under single inheritance model

In HarmonyOS Next development, the class inheritance mechanism is the core feature of implementing code reuse and polymorphism.Through a single inheritance model, subclasses can inherit members of the parent class (except private members) and extend behavior through override.This article combines document knowledge points to analyze inherited rules, best practices and applications in actual scenarios.


## 1. Basic rules and grammar of inheritance
HarmonyOS Next supports single inheritance, and subclasses inherit the parent class through the `<:` keyword declaration. The syntax is as follows:
```cj
open class Parent { /* Parent class definition */ }
class Child <: Parent { /* Subclass inherits parent class */ }
```  

### 1. Inheritable members and access control
- **Inheritable Members**:
- Member variables, member functions, and static members that are not `private`;
- The constructor of the parent class is not inheritable, but can be called with `super()`.
- **Not inherited members**:
- `private` member (only accessed internally by the parent class);
- Constructor (subclasses need to be customized).

**Example**:
```cj
open class Animal {
    public var name: String
protected var age: Int // Protected members can be accessed by subclasses
    public init(name: String, age: Int) {
        self.name = name
        self.age = age
    }
}

class Dog <: Animal {
    public var breed: String
    public init(name: String, age: Int, breed: String) {
        self.breed = breed
super.init(name: name, age: age) // Call the parent class constructor
    }
// Access the protected member of the parent class
    public func getAge() -> Int { age }
}
```  

### 2. `open` modifier and inheritance permissions
- The non-open class is not inheritable by default, and the `open` needs to be explicitly declared:
  ```cj
class SealedClass {} // Not inheritable
open class OpenClass {} // Inheritable
  ```  
- The `open` member allows subclass overrides, non-open` members cannot be overridden by default:
  ```cj
  open class Base {
public func fixedFunc() {} // non-open, subclasses cannot be overwritten
public open func overriddenFunc() {} // open, subclasses can override
  }
  ```  


## 2. Inheritance and call order of constructors
### 1. Type of constructor
- **Main constructor**: The same name as the class, initializes member variables when declared;
- **Normal constructor**: declared with `init`, supporting overloading.

### 2. Rules of subclass constructors
- The parent class constructor (`super()`) or other constructor (`this()`) must be called, and it must be called on the first line of the constructor body:
  ```cj
  open class Vehicle {
      public var speed: Int
      public init(speed: Int) { self.speed = speed }
  }

  class Car <: Vehicle {
      public var brand: String
      public init(speed: Int, brand: String) {
          self.brand = brand
super.init(speed: speed) // The parent class constructor must be called first
      }
  }
  ```  
- If the parent class has no parameter constructor, the child class must explicitly call the parent class parameter constructor:
  ```cj
  open class Parent {
public init(value: Int) {} // No default constructor
  }
  class Child <: Parent {
      public init() {
super.init(value: 0) // The parent class parameter constructor must be called
      }
  }
  ```  

### 3. Initialization order
1. Initialize subclass member variables;
2. Call the parent class constructor;
3. Execute constructor body logic.

**Example**:
```cj
open class A {
    public var a = 10 { didSet { println("A.a = \(a)") } }
public init() { a = 20 } // The parent class constructor modifies the value of a
}
class B <: A {
public var b = a + 5 // When the subclass member variable is initialized, the parent class a has been initialized
    public init() {
super.init() // Call the parent class constructor (a=20 at this time)
b = 30 // Further modify the value of b
    }
}
let b = B() // Output: A.a = 20
```  


## 3. Override and Redefine (Redef)
### 1. Override of instance functions
Subclasses can override the `open` instance function of the parent class, and need to be modified with `override` (optional but explicit declaration is recommended):
```cj
open class Shape {
public open func area(): Float64 { 0.0 } // The default implementation of the parent class
}
class Circle <: Shape {
    private let radius: Float64
    public init(radius: Float64) { self.radius = radius }
public override func area(): Float64 { // Override parent class method
        3.14 * radius * radius
    }
}
```  

### 2. Redefinition of static functions (Redef)
Subclasses can redefine parent class static functions and use `redef` to modify (optional):
```cj
open class Utility {
    public static func version(): String { "1.0" }
}
class AdvancedUtility <: Utility {
public redef static func version(): String { "2.0" } // Redefine static functions
}
```  

### 3. Coverage rules
- The function signature must be exactly the same as the parent class (parameter type, return value);
- Subclass member access modifiers must be consistent with or more relaxed with the parent class (such as parent class `protected`, subclasses can be `public`).


## 4. Inheritance and practical application of polymorphism
### Scenario: Implement the device driver framework and support unified control of different hardware types

#### 1. Define parent class: general device driver
```cj
open class DeviceDriver {
    public var deviceName: String
    public open func connect(): Bool {
println("Connecting device:\(deviceName)")
return true // default implementation
    }
    public init(name: String) {
        self.deviceName = name
    }
}
```  

#### 2. Subclass: specific hardware drivers (such as serial drivers, network drivers)
```cj
class SerialDriver <: DeviceDriver {
    private let port: Int
public override func connect(): Bool { // Override the connection logic
println("Connect the device through the serial port\(port):\(deviceName)")
return super.connect() // Call the default logic of the parent class
    }
    public init(name: String, port: Int) {
        self.port = port
        super.init(name: name)
    }
}

class NetworkDriver <: DeviceDriver {
    private let ip: String
public redef static func version(): String { // Redefine the static version number
        "NetworkDriver v1.2"
    }
    public init(name: String, ip: String) {
        self.ip = ip
        super.init(name: name)
    }
}
```  

#### 3. Polymorphic calls: Unified interface handles different drivers
```cj
func testDrivers() {
    let serial = SerialDriver(name: "COM1", port: 1)
    let network = NetworkDriver(name: "Server", ip: "192.168.1.1")
    
    let drivers: [DeviceDriver] = [serial, network]
    drivers.forEach { driver in
driver.connect() // Dynamically call subclass implementation
    }
println(NetworkDriver.version()) // Output the result of the redefined static function
}
```  

**Output result**:
```
Connect the device through serial port 1: COM1
Connecting device: Server
NetworkDriver v1.2
```  


## 5. Inheritance restrictions and alternatives
### 1. Single inheritance restriction and combination mode
- HarmonyOS Next does not support multiple inheritance, multi-capability integration can be achieved through a combined interface (`class <: I1 & I2`) or includes object instances:
  ```cj
  interface Printable { func printData() }
  interface Connectable { func connect() }
  class MultiFunctionDevice <: Printable, Connectable {
private let printer: Print // Combining printer objects
private let connector: Connector // Combining connector objects
      public func printData() { printer.print() }
      public func connect() { connector.link() }
  }
  ```  

### 2. `sealed` class and closed design
Use `sealed` to modify the class, prohibiting it from inheriting, and is applicable to tool classes or final implementation classes:
```cj
sealed class FinalLogger { /* final log class, not inheritable */ }
```  

### 3. Inheritance constraints of abstract classes
Abstract classes force subclasses to implement abstract members to ensure logical integrity:
```cj
abstract class AbstractParser {
public abstract func parse(data: String): Any // Abstract function
public func logError(message: String) { /* Specific error handling */ }
}
class JSONParser <: AbstractParser {
public override func parse(data: String): Any { /* Implement parse logic */ }
}
```  


## 6. Summary: Inheritance Design Trade-offs
HarmonyOS Next's single inheritance mechanism ensures clear code structure while realizing reuse and extension through the following methods:
- **Code reuse**: inherit the parent class members and avoid repeated implementation of general logic;
- **Behavior extension**: Modify parent class behavior by overriding, or add new member extension capabilities;
- **Polymorphic Abstract**: The parent class refers to subclass instances to realize differentiated processing under the unified interface.
