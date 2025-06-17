
# HarmonyOS Next Collaborative Practice of Abstract Classes and Interfaces: Building Elastic Polymorphic Architecture

In HarmonyOS Next development, the coordinated use of abstract classes and interfaces is the core means to implement code reuse and behavioral abstraction.Abstract classes restrict subclass behavior by defining abstract members, while interfaces regulate type capabilities in the form of contracts.The combination of the two can build a system architecture with clear hierarchy and easy to expand. This article combines the "Cangjie Programming Language Development Guide" to analyze its collaboration model and practical points.


## 1. Core differences and complementarity between abstract classes and interfaces
| ** Features** | ** Abstract Class** | ** Interface** |
|------------------|-------------------------------------|-------------------------------------|  
| **Define Purpose** | Provides abstract templates for partial implementations | Define pure behavior contracts (no implementation) |
| **Inheritance Limit** | Single Inheritance (`class <: Abstract Class`) | Multiple Implementations (`class <: Interface 1 & Interface 2`) |
| **Member type** | Can contain abstract/non-abstract functions, variables | Abstract functions only, static functions (can be implemented by default) |
| **Typical Scenario** | Algorithm Skeleton (such as data processing flow) | Capability Abstraction (such as communication, storage interface) |

**Cooperation logic**:
- Abstract class is a partial implementation carrier of the interface, providing public logic for subclasses;
- Interfaces define common capabilities across domains, abstract classes implement interfaces and constrain subclass behavior.


## 2. Abstract class implementation interface: sinking design of default behavior
Abstract classes can implement interfaces and provide default implementations. Subclasses only need to cover the difference part and reduce duplicate code.

### 1. Interface definition and abstract class implementation
```cj
// Define log interface
interface Loggable {
    func log(message: String)
}

// Abstract class implements interface and provides a general log format
abstract class AbstractLogger <: Loggable {
    public func log(message: String) {
let timestamp = getCurrentTime() // General logic: get the timestamp
printLogWithFormat(timestamp: timestamp, message: message) // Abstract function, subclass implements specific format
    }
    protected abstract func printLogWithFormat(timestamp: String, message: String)
}

// Subclasses implement specific log formats (such as JSON format)
class JSONLogger <: AbstractLogger {
    protected override func printLogWithFormat(timestamp: String, message: String) {
        println("{\"time\": \"\(timestamp)\", \"msg\": \"\(message)\"}")
    }
}
```  

### 2. Hook function and template method pattern
Abstract classes define process skeletons through non-abstract functions, and subclasses implement differentiation steps by overwriting abstract functions:
```cj
abstract class DataProcessor {
public func process(data: String) { // Template method
let cleanedData = clean(data) // hook function, subclass implementation
let processedData = processCore(cleanedData) // Abstract function, subclass implementation
save(processedData) // General saving logic
    }
protected func clean(data: String) -> String { // Optional hook function, providing default implementation
        data.trimmingCharacters(in: .whitespaces)
    }
    protected abstract func processCore(data: String) -> String
private func save(data: String) { /* general saving logic */ }
}
```  


## 3. Multi-interface abstraction: Integrating cross-domain capabilities
Abstract classes can implement multiple interfaces at the same time, providing compounding capabilities for subclasses.

### 1. Multi-interface declaration and implementation
```cj
interface Communicable { func send(data: String) }
interface Loggable { func log(message: String) }

// Abstract class integrates communication and logging capabilities
abstract class NetworkComponent <: Communicable, Loggable {
    public func send(data: String) {
log(message: "Send data:\(data)") // Call the log interface
doSend(data) // Abstract function, subclass implements specific sending logic
    }
    protected abstract func doSend(data: String)
public func log(message: String) { /* The default implementation of the log interface */ }
}

// Subclass implements network components (such as HTTP clients)
class HTTPClient <: NetworkComponent {
    protected override func doSend(data: String) {
// Implement HTTP sending logic
    }
}
```  

### 2. Interface conflict handling
When multiple interfaces have members of the same name, abstract classes can be implemented uniformly:
```cj
interface A { func action() }
interface B { func action() }

abstract class ConflictHandler <: A, B {
public func action() { // Unified implementation of the same name function
handleAction() // Abstract function, subclasses implement concrete logic
    }
    protected abstract func handleAction()
}
```  


## 4. Practical scenario: Layered design of device driver framework
### Scenario: Build a cross-device driver framework to support unified control and status reporting of different hardware

#### 1. Define basic interfaces and abstract classes
```cj
// Device control interface
interface Controllable {
    func turnOn()
    func turnOff()
}

// Status reporting interface
interface Reportable {
    func getStatus(): String
}

// Abstract device class: implements interface and provides general logic
abstract class AbstractDevice <: Controllable, Reportable {
    public func turnOn() {
preCheck() // General pre-check
doTurnOn() // Abstract function, subclass implementation
logStatus("Opened")
    }
public func turnOff() { /* general closing logic */ }
public func getStatus(): String { /* Default status information */ }
    protected abstract func doTurnOn()
private func preCheck() { /* general check logic */ }
private func logStatus(message: String) { /* General logging */ }
}
```  

#### 2. Specific device driver implementation
```cj
// Sensor driver
class SensorDriver <: AbstractDevice {
    protected override func doTurnOn() {
// Initialize the sensor hardware
println("Sensor is enabled")
    }
    public override func getStatus(): String {
"Sensor Status: Normal"
    }
}

// Actuator driver
class ActuatorDriver <: AbstractDevice {
    protected override func doTurnOn() {
// Start the actuator motor
println("Executor started")
    }
}
```  

#### 3. Framework layer polymorphic call
```cj
func operateDevice(device: AbstractDevice) {
    device.turnOn()
    println(device.getStatus())
    device.turnOff()
}

// Use example
let sensor: SensorDriver = SensorDriver()
operateDevice(device: sensor) // Call the general process and subclass concrete implementation of abstract classes
```  


## 5. Design principles and trap avoidance

### 1. Priority interface abstraction, delayed implementation of sinking
- Ability to define through interfaces, try not to include abstract classes, and maintain the purity of the interface;
- Abstract classes only implement public logic across subclasses, avoiding the inclusion of domain-specific code.

### 2. Design of the finalizer for abstract classes
If abstract classes involve resource management, the cleanup logic needs to be implemented through abstract functions:
```cj
abstract class ResourceHolder {
public abstract func release() // abstract release function
~init() { release() } // The finalizer calls abstract function
}
```  

### 3. Avoid over-expansion of abstract classes
Control the responsibility boundaries of abstract classes. If there are more than 3 abstract functions, consider splitting them into multiple abstract classes or interfaces.


## 6. Summary: The synergistic value of abstraction and contract
The collaboration between abstract classes and interfaces in HarmonyOS Next reflects the design philosophy of "template method + capability contract":
- **Code reuse**: Abstract classes provide common processes and interface definition capabilities standards;
- **Scalability**: Subclasses quickly integrate compound capabilities by inheriting abstract classes and implementing interfaces;
- **Type Safety**: The compiler forces the abstract member implementation to avoid logical vulnerabilities.
