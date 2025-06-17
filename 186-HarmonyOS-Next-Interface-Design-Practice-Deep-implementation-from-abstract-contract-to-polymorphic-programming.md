
# HarmonyOS Next Interface Design Practice: Deep implementation from abstract contract to polymorphic programming

In HarmonyOS Next development, Interface is the core tool for building scalable and loosely coupled systems.As an abstract contract for type behavior, the interface not only defines a set of constraint rules, but also realizes the design principle of "abstract-oriented programming" through a polymorphic mechanism.This article combines actual development scenarios to analyze the core features and implementation practices of the interface, helping developers master the full process design from basic definition to complex architecture.


## 1. The nature of an interface: the standardized definition of behavior contracts
Interfaces are abstractions of type capabilities, which strip away specific implementation details and retain only the declaration of behavior.In HarmonyOS Next, the interface is defined through the `interface` keyword, and its members (functions, static functions) are all declared abstractly, requiring that the implementation type must provide a specific implementation.

### 1. Basic interface definition and implementation
Taking the device control scenario as an example, define the start-stop behavior of the `Controlable` interface to constrain the device:
```cj
// Define interface: Device control contract
interface Controlable {
func turnOn(): Unit // Turn on
func turnOff(): Unit // Shutdown
static func deviceName(): String // Static function: get the device name
}

// Implementation class: Smart bulb
class SmartBulb <: Controlable {
    private var isOn = false

// Implement interface members
    public func turnOn() {
        isOn = true
println("\(Self.deviceName()) enabled")
    }

    public func turnOff() {
        isOn = false
println("\(Self.deviceName()) Closed")
    }

    public static func deviceName(): String {
"Smart Light Bulb"
    }
}
```

### 2. Access control and scope of interfaces
- **`sealed` interface**: Restricts only implementations within the current package, such as the system-level interface `sealed interface SystemDriver` to prevent illegal implementations from outside.
- **Default implementation of static members**: The static functions of the interface can provide default implementations to reduce the duplicate code of subclasses:
  ```cj
  interface Loggable {
static func logLevel(): LogLevel { .Info } // Default log level
      func log(message: String)
  }
  ```


## 2. Collaboration between interfaces and classes: the core paradigm of polymorphic programming
The value of interfaces is reflected through a polymorphic mechanism, that is, "same interface, different implementations".In HarmonyOS Next, the class implements an interface through the `<:` keyword declaration, forming a subtype relationship, and supporting dynamic distribution.

### 1. Dynamic dispatch mechanism for polymorphic calls
Define the `HomeAppliance` interface, implement the `Refrigerator` and `AirConditioner` subclasses, and operate different devices through the unified interface:
```cj
interface HomeAppliance <: Controlable {
func adjustSetting(value: Int) // Adjust settings
}

class Refrigerator <: HomeAppliance {
    public func adjustSetting(value: Int) {
println("Set the refrigerator temperature to \(value)℃")
    }
// Implement Controlable members...
}

class AirConditioner <: HomeAppliance {
    public func adjustSetting(value: Int) {
println("Set the air conditioner temperature to \(value)℃")
    }
// Implement Controlable members...
}

// Polymorphic call: interface as function parameter
func operateAppliance(appliance: HomeAppliance, setting: Int) {
    appliance.turnOn()
    appliance.adjustSetting(setting)
    appliance.turnOff()
}

// Dynamically determine the specific implementation during runtime
let fridge = Refrigerator()
operateAppliance(appliance: fridge, setting: 4) // Output smart light bulb related logs
```

### 2. Interface and inheritance selection strategy
| Dimensions | Interface | Abstract Class |
|--------------|----------------------------------|-----------------------------------|  
| **Essence** | Behavior contract (declared only) | Partially implemented abstract types (can include specific methods) |
| **Inheritance Limit** | Multiple interfaces can be implemented (no inheritance restrictions) | Single inheritance (`class <: abstract class`) |
| **Applicable scenarios** | Capability abstraction (such as network protocols, data formats) | Template methods (such as algorithm skeleton) |

**Best Practice**: Prioritize the use of interfaces to implement capability abstraction, and use abstract classes only when sharing implementation details are needed.For example, the `JSONParser` and `XMLParser` implement the `DataParser` interface, while the `AbstractParser` abstract class provides a default implementation of the parsing process.


## 3. Advanced applications of interfaces: from basic components to complex architectures

### 1. Constraints of interfaces in generic programming
Through generic constraints, it is mandatory that types must implement specific interfaces to improve code reusability.For example, define a general logging function, requiring the type to implement the `Loggable` interface:
```cj
func logAllItems<T: Loggable>(items: [T]) {
    items.forEach { item in
println("[\(T.logLevel())] \(item.log(message: "Operation Record"))")
    }
}

// Example of usage: Smart device list log output
let devices: [Loggable] = [SmartBulb(), Refrigerator()]
logAllItems(items: devices)
```

### 2. Interface and type conversion: Safe runtime adaptation
Using the `is` and `as` operators, we can determine whether the object supports a specific interface at runtime and safely convert the type:
```cj
func handleDevice(device: Controlable) {
    if device is HomeAppliance {
let appliance = device as? HomeAppliance // Safely convert to HomeAppliance type
appliance?.adjustSetting(value: 24) // Call extension function only when supported
    }
device.turnOn() // The required interface function is executed normally
}
```

### 3. Practice of Interface Isolation Principle (ISP)
Avoid the interface being too bloated, split the large interface into multiple small interfaces, and reduce the dependency burden of implementing classes.For example, split the `Device` interface into `Controlable` and `StatusReportable`:
```cj
interface Controlable { /* Start and stop interface */ }
interface StatusReportable { func getStatus(): String }

// Only some interface types need to be implemented
class SimpleSensor <: StatusReportable {
public func getStatus() -> String { "Sensor status is normal" }
// No need to implement the Controlable interface
}
```


## 4. Practical Traps and Optimization Strategies

### 1. Visibility control of interface members
Interface members default `public`, and the implementation class must use the same or more relaxed access modifier.For example:
```cj
interface PrivateInterface {
func privateFunc(): Unit // Implicit public, the implementation class must be declared as public
}

class Implementation <: PrivateInterface {
// Compilation error: The default internal modifier is not loose enough
    func privateFunc() {} 
}
```

### 2. Version compatibility of static members
Modifying static members of the interface may cause binary incompatibility.It is recommended to implement extensions by adding static functions instead of modifying existing functions:
```cj
interface NetworkClient {
static func defaultTimeout(): Int // Existing static functions
static func newDefaultTimeout(): Int { 30 } // Add new extension function to preserve the original logic
}
```

### 3. Resource management of terminal and interface
If the class implementing the interface involves resource release (such as file handles, network connections), it needs to be managed through the terminator (`~init`) in conjunction with interface lifecycle:
```cj
class FileHandler <: FileIO {
    private var fd: CInt = -1

    ~init() {
if fd != -1 { close(fd) } // Ensure resource release
    }
}
```


## 5. Summary: Interface-driven architecture upgrade
In HarmonyOS Next, interfaces are the cornerstone of building elastic architectures:
- **Decoupling component dependency**: Implement details through interface isolation, such as separating device drivers from business logic;
- **Improving testability**: Use interfaces to simulate dependencies (such as using `MockNetworkClient` instead of real implementation);
- **Support hot plug**: Dynamically load modules that implement the same interface without modifying the core code.
