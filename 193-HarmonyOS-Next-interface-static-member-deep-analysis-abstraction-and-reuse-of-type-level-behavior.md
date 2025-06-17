
# HarmonyOS Next interface static member deep analysis: abstraction and reuse of type-level behavior

In HarmonyOS Next development, static members of the interface (static functions, static properties) are important tools for implementing type-level behavior abstraction.Unlike instance members, static members belong to the interface itself rather than instances and can be used to define public logic or specifications related to types.This article combines the "Cangjie Programming Language Development Guide" to analyze the characteristics, application scenarios and collaborative rules with classes of static interface members.


## 1. Basic definition and syntax of static members
Static members of an interface are declared via the `static` keyword, including static functions and static properties, and can include default implementations.

### 1. Definition and implementation of static functions
```cj
interface MathOps {
static func add(a: Int, b: Int): Int // Abstract static functions
static func multiply(a: Int, b: Int) -> Int { // Static function with default implementation
        a * b
    }
}

// Class implements interface static functions
class Calculator <: MathOps {
    public static func add(a: Int, b: Int): Int {
        a + b
    }
}
```  

### 2. Declaration and constraints of static properties
```cj
interface FileFormat {
static prop extension: String // Abstract static properties
static mut prop version: Int { // Abstract static read and write properties
        get()
        set()
    }
}

// Implementation class provides static attribute implementation
class JSONFormat <: FileFormat {
    public static prop extension: String { get() { "json" } }
    private static var _version = 1
    public static mut prop version: Int {
        get() { _version }
        set { _version = newValue }
    }
}
```  


## 2. The core characteristics of static members

### 1. Default implementation and code reuse
Interfaces can provide common logic through static members to reduce subclass duplication:
```cj
interface Logger {
static func logLevel(): LogLevel { .Info } // Default log level
    static func log(message: String) {
println("[\(logLevel())] \(message)") // Use the default implementation
    }
}

// Subclasses can directly use default logic
class FileLogger <: Logger {}
FileLogger.log(message: "File Operation Log") // Output: [Info] File Operation Log
```  

### 2. Type-level constraints and generic adaptation
Static members can be used for type constraints of generic functions to ensure that types meet specific behaviors:
```cj
func processData<T: FileFormat>(data: T.Type) { // T.Type represents the type itself
println("File extension:\(T.extension)") // Call static properties
T.log(message: "Data processing starts") // Call static functions
}

// Call example
processData(data: JSONFormat.self) // Pass in type itself (JSONFormat.self)
```  

### 3. Collaboration with static class members
Classes can unify the type-level behavior of different classes by implementing static interface members:
```cj
open class Animal {
    public static func speciesName(): String { "Animal" }
}

class Dog <: Animal, Named { // Dog implements the interface Named at the same time
    public static func speciesName(): String { "Canis lupus familiaris" }
}

interface Named {
static func speciesName(): String // The interface static function is the same as the class static function.
}
```  


## 3. Application scenarios of static members

### 1. Factory pattern and type creation
Define object creation logic through interface static functions to achieve decoupling:
```cj
interface Vehicle {
static func create(): Vehicle // Static factory method
    func start(): Unit
}

class Car <: Vehicle {
    public static func create(): Vehicle { Car() }
public func start(): Unit { println("car start") }
}

// Create an object using a static factory
let vehicle: Vehicle = Vehicle.create() // Actually call Car.create()
```  

### 2. Configuration Management and Metadata Storage
Interface static properties can be used to store type metadata or configuration information:
```cj
interface Device {
static prop deviceID: String // Unique ID of the device
static mut prop settings: Dictionary<String, Any> // Device configuration
}

class SmartBulb <: Device {
    public static prop deviceID: String { get() { "BULB_001" } }
    private static var _settings: Dictionary<String, Any> = [:]
    public static mut prop settings: Dictionary<String, Any> {
        get() { _settings }
        set { _settings = newValue }
    }
}

// Access type-level configuration
SmartBulb.settings["brightness"] = 80
println(SmartBulb.deviceID) // Output: BULB_001
```  

### 3. Algorithm interface and default implementation
When defining an algorithm interface, the basic algorithm is provided by static members, and subclasses can be optimized to implement:
```cj
interface SortAlgorithm {
static func sort<T: Comparable>(array: [T]): [T] { // Basic sorting implementation
        array.sorted()
    }
}

class QuickSort <: SortAlgorithm {
public static override func sort<T: Comparable>(array: [T]): [T] { // Redefine static functions
// Quick sorting implementation
    }
}
```  


## IV. Limitations and best practices of static members

### 1. Access rules and modifiers
- The default `public` of static interface members is `public`, and the implementation class needs to use the same or more relaxed access modifier;
- Static members of the `sealed` interface are only accessible within packages:
  ```cj
  sealed interface InternalAPI {
static func internalFunc(): Unit // visible in the package
  }
  ```  

### 2. Avoid circular dependencies
Avoid direct or indirect reference of static members among other interfaces to prevent compilation errors:
```cj
interface A {
static func a(): Unit { B.b() } // Depend on static functions of interface B. If B depends on A, an error will be reported
}
interface B {
    static func b(): Unit { A.a() }
}
```  

### 3. Collaboration with instance members
Static members can call instance members, but need to be referenced through the instance:
```cj
interface Factory {
static func create(): Self // Self represents the interface implementation class itself
    func initialize()
}

class MyClass <: Factory {
    public static func create(): MyClass { MyClass() }
public func initialize() { /* instance initialization logic */ }

    public static func setup() {
        let instance = create()
instance.initialize() // Use instance members in static functions
    }
}
```  


## 5. Summary: The design value of static members
Static members of the HarmonyOS Next interface provide the following capabilities for type-level behavior:
- **Abstract Specification**: Defines the static behavior that types must implement (such as factory methods, configuration interfaces);
- **Code reuse**: Reduce subclass duplication logic through default implementation to improve development efficiency;
- **Generic Constraints**: Force types to follow specific rules in generic programming to enhance type safety.
