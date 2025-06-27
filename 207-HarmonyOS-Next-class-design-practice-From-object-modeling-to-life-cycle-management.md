# HarmonyOS Next class design practice: From object modeling to life cycle management

> I still remember the first time I wrote the device class, the system crashed because of the wrong inheritance order. Debug only found out that the constructor did not call super().Today, I will share the pitfalls I have strolled over the years and summarized design experience to help everyone avoid detours.


## 1. The essence of class: "container" of data and behavior

### 1.1 Member-defined pit avoidance guide
```cj
// Base class of smart home equipment (correct demonstration)
open class SmartDevice {
public var deviceId: String // Unique ID of the device
private var _status: DeviceStatus = .offline // underline private variables
    
// Main constructor, parameter is declared directly as a member
    public SmartDevice(id: String) {
        self.deviceId = id
    }
    
// Status accessor (with verification logic)
    public func getStatus() -> DeviceStatus {
        _status
    }
    
    public func setStatus(status: DeviceStatus) {
        if status == .online && _status == .offline {
logStatusChange() // Status Change Log
        }
        _status = status
    }
}
```  

**Lesson of Blood and Tears**: All variables were set to public, causing external direct modification of the state to cause exceptions. Later, the verification logic was encapsulated with getter/setter, and the bug was reduced by 60%.


## 2. Life cycle: The journey of "birth to death" of objects

### 2.1 The order of execution of constructors
```cj
class Parent {
    public var parentProp: String
    
    public Parent(prop: String) {
        parentProp = prop
printInitMsg() // The subclass has not been initialized yet
    }
    
    public open func printInitMsg() {
        println("Parent initialized")
    }
}

class Child <: Parent {
    public var childProp: Int
    
    public Child(prop: String, childProp: Int) {
        self.childProp = childProp
super.init(prop: prop) // The parent class construct must be called first
    }
    
    public override func printInitMsg() {
        println("Child initialized with: \(childProp)")
    }
}

// When executing Child("test", 10), the output is:
// Parent initialized (the parent class is executed first, and childProp is 0 at this time)
// Correct way: Avoid calling subclass overrides in parent class constructs
```  

### 2.2 The correct way to open the finalizer
```cj
class NativeResource {
    private var ptr: UnsafeRawPointer?
    
    init(size: Int) {
ptr = malloc(size) // Allocate C memory
    }
    
    ~init() {
        if let p = ptr {
free(p) // Terminator releases resources
            ptr = nil
        }
    }
    
// Manual release method (more controllable than the terminator)
    public func release() {
        if let p = ptr {
            free(p)
            ptr = nil
        }
    }
}
```  

**Performance Tips**: The finalizer is the last guarantee. It is best to provide manual release methods to actively release resources when they do not rely on GC.


## 3. Inheritance mechanism: the "double-edged sword" of code reuse

### 3.1 Abstract class and template method pattern
```cj
// Device control abstract class (template method)
abstract class DeviceController {
    public func control(device: SmartDevice) {
preCheck() // General pre-check
doControl(device) // Abstract method, subclass implementation
postCheck() // General post-check
    }
    
protected func preCheck() { /* General logic such as permission verification */ }
    protected abstract func doControl(device: SmartDevice)
protected func postCheck() { /* general logic such as logging */ }
}

// Light bulb control implementation
class BulbController <: DeviceController {
    protected override func doControl(device: SmartDevice) {
        if let bulb = device as? SmartBulb {
            bulb.turnOn()
        }
    }
}
```  

### 3.2 Scenarios where combination is better than inheritance
```cj
// Error: Inheritance leads to functional bloating
class CameraDevice <: SmartDevice {
// Includes functions such as taking photos, recording, focusing, etc.
}

// Correct way: Combining functional interfaces
class CameraDevice <: SmartDevice {
private let captureHandler: CaptureHandler // Combined photo shooting function
private let focusHandler: FocusHandler // Combined focus function
    
    public func takePhoto() {
        captureHandler.shot()
        focusHandler.autoFocus()
    }
}
```  


## 4. Practical combat: The evolution of smart homes

### 4.1 First generation design (all problems)
```cj
// Original version: All devices share a class
class SmartDevice {
    var type: DeviceType
    var status: DeviceStatus
// Contains common and unique logic for all devices
}
```  

**question**:
- Class definition needs to be modified when adding new device types
- Unique functions are mixed, code is messy


### 4.2 Refactored architecture (clear and extensible)
```cj
// Base class
open class SmartDevice { /* General properties and methods */ }

// Interface definition unique capabilities
interface Cameraable { func takePhoto() }
interface Speakerable { func playSound() }

// Specific equipment class (combination interface)
class SmartCamera <: SmartDevice, Cameraable {
public func takePhoto() { /* Photo implementation */ }
}

class SmartSpeaker <: SmartDevice, Speakerable {
public func playSound() { /* play implementation */ }
}
```  

**Optimization effect**:
- No need to modify the base class when adding new device types
- Clear functions and responsibilities, and maintenance costs are reduced by 70%


## 5. Must know traps and best practices

1. **Initialization Sequence Trap**:
Do not call subclass overridden methods in the parent class construct, it may access uninitialized members.

2. **Terminator performance issues**:
Avoid time-consuming operations such as network requests in the finalizer, which may cause GC to pause

3. **Inheritance Depth Control**:
The inheritance level is controlled within 3 layers, if it exceeds it, it will be considered as a combination mode.
