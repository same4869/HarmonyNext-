
# HarmonyOS Next Abstract Class and Interface Collaboration Practice: Building a Scalable Polymorphic System

In HarmonyOS Next development, abstract classes and interfaces are the core tools for implementing polymorphic programming.Abstract classes restrict subclass behavior by defining abstract members, while interfaces regulate type capabilities in the form of contracts.When the two are used together, a system architecture with clear hierarchy and easy to expand can be built.This article combines document knowledge points and practical scenarios to analyze how to realize code reuse and behavioral abstraction through abstract classes and interfaces.


## 1. Abstract class foundation: Defining behavioral skeleton
Abstract classes are declared through the `abstract` keyword, allowing non-abstract functions that contain abstract functions (functions without implementation) and concrete implementations to force subclasses to complete key logic.

### 1. Abstract class definition and implementation rules
```cj
// Abstract class: Graphic base class
abstract class Shape {
public abstract func area(): Float64 // Abstract function: calculate area
public func draw() { // Specific function: draw the default implementation
println("Draw Graphics")
    }
}

// Subclasses must implement abstract functions
class Circle <: Shape {
    private let radius: Float64
    public init(radius: Float64) { self.radius = radius }
public override func area(): Float64 { // override is optional, but explicit declaration is clearer
        3.14159 * radius * radius
    }
}
```  

### 2. Inheritance restrictions of abstract classes
- Non-abstract subclasses must implement all abstract members, otherwise an error will be reported in the compilation;
- Abstract classes cannot be instantiated and exist only as base classes:
  ```cj
let shape: Shape = Circle(radius: 5.0) // Legal: Abstract class references subclass instances
let abstractInstance: Shape = Shape() // Compilation error: Unable to instantiate abstract class
  ```  


## 2. The core difference between interfaces and abstract classes
| ** Features** | ** Abstract Class** | ** Interface** |
|------------------|-------------------------------------|-------------------------------------|  
| **Define Purpose** | Provides abstract templates for partial implementations | Define pure behavior contracts (no implementation) |
| **Inheritance Limit** | Single Inheritance (`class <: Abstract Class`) | Multiple Implementations (`class <: Interface 1 & Interface 2`) |
| **Member type** | Can contain abstract/non-abstract functions, variables | Abstract functions only, static functions (can be implemented by default) |
| **Usage scenarios** | Algorithm skeleton (such as sorting process) | Capability abstraction (such as network requests, data serialization) |

**Example comparison**:
- The abstract class `AbstractLogger` provides log-level judgment logic, and subclasses implement specific output (file/network log);
- The interface `Transmittable` specifies data transmission capabilities, and different protocols (HTTP/WebSocket) implement this interface.


## 3. Collaborative design: a hybrid architecture for abstract classes to implement interfaces
Abstract classes can be used as part of the implementation carrier of the interface, providing public logic for subclasses and reducing duplicate code.

### 1. Abstract classes implement interfaces and provide default behaviors
```cj
// Define interface: can save data
interface Savable {
    func save(data: String): Bool
}

// Abstract class implements interface and provides general error handling
abstract class FileBasedSavable <: Savable {
    public func save(data: String): Bool {
if !checkStorageAvailable() { // General logic: Check storage availability
logError("Storage is not available")
            return false
        }
return saveToFile(data) // Abstract function: subclass implements specific writing
    }
protected abstract func saveToFile(data: String): Bool // Protected abstract function
}

// Subclasses only need to implement core logic
class LocalFileSavable <: FileBasedSavable {
    protected override func saveToFile(data: String): Bool {
// Implement file writing logic
println("Write to file:\(data)")
        return true
    }
}
```  

### 2. Complex scenarios of multi-interface abstract classes
When abstract classes need to integrate multiple capabilities, multiple interfaces can be implemented:
```cj
abstract class NetworkDevice <: Controlable, StatusReportable {
public abstract func getIPAddress(): String // Implement StatusReportable
public func statusReport(): String { // The default implementation of the interface
return "Device status:\(isOn? "Running": "Close")"
    }
}
```  


## 4. Polymorphic Practical Practice: Architectural Design of Equipment Management System
### Scenario: Build a smart home device management platform, supports multiple device types (lights, air conditioners, sensors), and requires unified control and status reporting.

#### 1. Define interfaces and abstract classes
```cj
// Basic control interface
interface Controlable {
    func turnOn(): Unit
    func turnOff(): Unit
}

// Status reporting interface
interface StatusReportable {
    func getStatus(): String
}

// Abstract device class: integrates interfaces and provides general logic
abstract class SmartDevice <: Controlable, StatusReportable {
    protected var isOn = false
    public func turnOn() {
        isOn = true
onStateChange() // Hook function: subclass optional rewrite
    }
    public func turnOff() { isOn = false }
protected func onStateChange() {} // Empty implementation, subclasses can override
    public abstract func getStatus(): String
}
```  

#### 2. Implement specific equipment categories
```cj
// Smart light bulb
class SmartBulb <: SmartDevice {
    private let brightness: Int
    public init(brightness: Int) { self.brightness = brightness }
    public override func getStatus(): String {
return "Light Bulb Status:\(isOn? "On, Brightness\(brightness)" : "Off")"
    }
    protected override func onStateChange() {
println("Light Brightness:\(brightness)") // Rewrite the hook function
    }
}

// Environmental sensor (only status reporting)
class EnvironmentSensor <: SmartDevice {
    private let temperature: Float64
    public init(temperature: Float64) { self.temperature = temperature }
    public override func getStatus(): String {
return "Temperature:\(temperature)℃, device status:\(isOn? "Run": "Stop")"
    }
// No need to implement turnOn/turnOff, inherit from abstract class
}
```  

#### 3. Polymorphic management and dynamic scheduling
```cj
func manageDevices(devices: [SmartDevice]) {
    devices.forEach { device in
device.turnOn() // General logic that calls abstract class implementation
println(device.getStatus()) // Dynamic distribution subclass implementation
        device.turnOff()
    }
}

// Run example
let bulb = SmartBulb(brightness: 80)
let sensor = EnvironmentSensor(temperature: 24.5)
manageDevices(devices: [bulb, sensor])
```  

**Output result**:
```
Brightness of light bulb: 80
Light bulb status: On, brightness 80
Temperature: 24.5℃, Equipment status: Operation
```  


## 5. Design principles and trap avoidance

### 1. Dependency Inversion Principle (DIP)
High-level modules should rely on interfaces or abstract classes, not concrete classes.For example, the device management module relies on the `SmartDevice` abstract class, not the `SmartBulb` concrete class:
```cj
// Correct: Depend on abstract classes
func updateFirmware(device: SmartDevice) { /* ... */ }

// Error: Depend on specific classes
func updateFirmware(bulb: SmartBulb) { /* ... */ }
```  

### 2. Avoid over-designing of abstract classes
Abstract classes should focus on "core logic that must be implemented by subclasses" rather than taking care of all details.If the interface is sufficiently constrained, the interface is preferred.

### 3. Terminator processing of abstract class
Abstract classes containing resource management need to ensure that the subclass releases resources correctly. You can force the subclass declaration to clean up the logic through abstract functions:
```cj
abstract class ResourceHolder {
public abstract func release(): Unit // Force subclasses to implement resource release
~init() { release() } // The finalizer calls abstract function
}
```  


## 6. Summary: The dual driving force of abstraction and contract
In HarmonyOS Next, the coordination between abstract classes and interfaces reflects the design philosophy of "template method + interface contract":
- **Abstract class**Define algorithm skeletons and reduce duplicate code in subclasses;
- **Interface**Specification capability boundaries, supporting cross-module collaboration.
