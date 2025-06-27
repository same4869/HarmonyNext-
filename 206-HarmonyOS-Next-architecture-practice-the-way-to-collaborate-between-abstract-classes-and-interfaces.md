# HarmonyOS Next architecture practice: the way to collaborate between abstract classes and interfaces

> I still remember when I first designed the device driver framework, I was facing the chaotic code adapted by multiple devices, and I didn’t realize it until I refactored it with abstract classes and interfaces.This architectural solution has withstood the test of more than 10 device types in smart home projects. Today, we share the core design ideas.


## 1. The collaborative philosophy of abstraction and interface

### 1.1 Core difference comparison (practical perspective)
| ** Features** | ** Abstract Class** | ** Interface** |
|----------------|---------------------------|---------------------------|  
| **Positioning** | Algorithm Skeleton (with partial implementation) | Capability Contract (Pure Behavior Definition) |
| **User scenarios** | Data processing process standardization | Cross-module capability abstraction |
| **Typical Cases** | Basic Implementation of Log Framework | Communication Protocol Definition |

**Golden Rules of Collaboration**:
- Interface definition "What can be done", abstract class implementation "How to do partly"
- Subclasses inherit abstract classes and implement interfaces, and the dual advantages of combination and reuse


## 2. Template method and contract combination practice

### 2.1 Hierarchical design of log system
```cj
// Define log interface (contract)
interface LogContract {
    func log(msg: String)
    func logError(msg: String)
}

// Abstract classes implement public logic
abstract class BaseLogger <: LogContract {
// Template method: Unified log format
    public func log(msg: String) {
        let time = getFormattedTime()
appendLog("[\(time)] \(msg)") // Abstract method is implemented by subclasses
    }
    
    public func logError(msg: String) {
log(msg: "[ERROR] \(msg)") // Reuse normal log logic
    }
    
    protected abstract func appendLog(formattedMsg: String)
private func getFormattedTime() -> String { /* General time formatting */ }
}

// Specific implementation class (file log)
class FileLogger <: BaseLogger {
    private var fileHandler: FileHandler
    
    protected override func appendLog(formattedMsg: String) {
        fileHandler.write(formattedMsg)
    }
}
```  

**Key Advantages**:
- Interface unified log behavior, abstract class encapsulation time formatting and other public logic
- Subclasses only need to implement differentiated storage logic, and the code volume is reduced by 40%


## 3. Multi-interface integration: device driver framework design

### 3.1 Resilient architecture for cross-device control
```cj
// Define the device control interface
interface Controlable {
    func powerOn()
    func powerOff()
}

// Define the status reporting interface
interface Reportable {
    func getStatus() -> String
}

// Dual ability of abstract class integration
abstract class DeviceDriver <: Controlable, Reportable {
// Startup template method
    public func powerOn() {
checkPermission() // General permission check
doPowerOn() // Abstract: Subclass implements specific boot logic
logStatus() // General status logging
    }
    
public func getStatus() -> String { /* General status format */ }
    protected abstract func doPowerOn()
private func checkPermission() { /* General permission logic */ }
}

// WiFi module driver implementation
class WiFiDriver <: DeviceDriver {
    protected override func doPowerOn() {
// WiFi chip initialization logic
println("WiFi module is started")
    }
}
```  

### 3.2 Interface conflict handling practice
```cj
interface A { func action() }
interface B { func action() }

// Unified conflict handling of abstract classes
abstract class ConflictHandler <: A, B {
    public func action() {
// Unified preprocessing logic
handleAction() // Abstract method is implemented by subclasses
    }
    protected abstract func handleAction()
}
```  


## 4. Blood and tears experience in architecture optimization

### 4.1 Drive the Evolution of Framework
**First Edition Question**:
- Direct implementation of the interface leads to repeated codes
- Multiple logic needs to be modified when adding a new device type

**Refactoring Solution**:
1. Abstract class encapsulates common processes (permission checking, logging)
2. Interface definition core capabilities (control, reporting)
3. Subclasses only implement device-specific hardware operations

**Optimization effect**:
- The development time of new equipment has been shortened from 2 days to 4 hours
- Reduce code maintenance costs by 60%


### 4.2 Three principles of abstract design
1. **Single Responsibilities**: Each abstract class focuses on 1 core process (such as logs, device control)
2. **Hook is preferred**: Use abstract methods to expose extension points, rather than to cover the entire process after inheritance.
3. **Terminator Design**:
```cj
abstract class ResourceDriver {
    public abstract func release()
~init() { release() } // Ensure resource release
}
```  


## 5. Advanced applications: Plug-in architecture practice

### 5.1 Plug-in interface and abstract class combination
```cj
// Basic plug-in interface
interface Plugin {
    func init(params: Any) -> Bool
    func execute() -> Any
}

// Plugin abstract class (implementing public logic)
abstract class BasePlugin <: Plugin {
    public func init(params: Any) -> Bool {
// General initialization check
        return doInit(params)
    }
    
    protected abstract func doInit(params: Any) -> Bool
    public abstract func execute() -> Any
}

// Network plug-in implementation
class NetworkPlugin <: BasePlugin {
    protected override func doInit(params: Any) -> Bool {
// Network plug-in specific initialization
    }
    
public func execute() -> Any { /* Network request logic */ }
}
```  

**Plugin Advantages**:
- Supports dynamic loading of plug-ins at runtime
- New features do not need to modify the main frame code


## 6. Pit avoidance guide: From stepping on a pit to filling a pit

1. **Interface expansion trap**:
Interfaces with more than 5 methods are considered split into multiple dedicated interfaces

2. **Abstract class overdesign**:
The abstract method is controlled within 3, otherwise it will be split into multi-layer abstract classes.

3. **Type conversion risk**:
Reduce casting with type erase or generic constraints
