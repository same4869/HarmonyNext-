
# HarmonyOS Next Property: Advanced Tips for Encapsulating Data Access

In HarmonyOS Next development, Property is the core mechanism for implementing data encapsulation and behavior abstraction.Through the properties of `getter` and `setter`, developers can flexibly control the reading and modification of data without exposing internal implementations.This article combines the "Cangjie Programming Language Development Guide" to analyze advanced application scenarios and best practices for attributes.


## 1. The essence of attributes: the abstract layer of data access
The attribute is declared through the `prop` keyword, decoupling the data access logic from the storage.Unlike member variables, attributes do not directly store values, but control read and write through custom logic.

### 1. Basic syntax and read and write control
```cj
class TemperatureSensor {
    private var _temp: Float64 = 25.0
    private let minTemp: Float64 = -20.0
    private let maxTemp: Float64 = 80.0

// Read-only attribute: exposed temperature value, restricted modification
    public prop temperature: Float64 {
        get() { _temp }
    }

// Read and write properties: Verify the temperature range
    public mut prop targetTemperature: Float64 {
        get() { _temp }
        set(value) {
            if value >= minTemp && value <= maxTemp {
                _temp = value
            } else {
throw Error("Temperature out of range:\(value)")
            }
        }
    }
}
```  

### 2. Implicit Closure Property
For simple logic, the `get` keyword can be omitted and the expression can be directly returned:
```cj
class Circle {
    private let radius: Float64
public prop area: Float64 = 3.14 * radius * radius // Implicit getter
    public init(radius: Float64) { self.radius = radius }
}
```  


## 2. Advanced features and design patterns of attributes

### 1. Static properties: type-level data abstraction
Static properties belong to the class itself, not instances, and are modified by `static`:
```cj
class AppConfig {
    public static prop appVersion: String {
        get() { "1.2.3" }
    }
    public static mut prop debugMode: Bool {
        get() { false }
set { /* Write logic */ }
    }
}

// Use example
println(AppConfig.appVersion) // Output: 1.2.3
AppConfig.debugMode = true
```  

### 2. Property Observer
Listen to the change of property values ​​through the `didSet` and `willSet` hook functions:
```cj
class User {
    public mut prop email: String {
        didSet {
if email != oldValue { // oldValue is the old value
sendNotification("The email has been changed to:\(email)")
            }
        }
    }
}
```  

### 3. Abstract properties in interfaces
The interface can declare abstract properties and force the implementation class to provide read and write logic:
```cj
interface Observable {
mut prop data: String // Abstract read and write properties
prop version: Int // Abstract read-only attributes
}

class DataModel <: Observable {
    private var _data: String = ""
    private var _version: Int = 0

    public mut prop data: String {
        get() { _data }
        set { _data = value; _version += 1 }
    }

    public prop version: Int { get() { _version } }
}
```  


## 3. Coordinated application of attributes and other characteristics

### 1. Attributes and Access Modifiers
Attributes can control visibility through access modifiers (`public`/`private`, etc.):
```cj
class SecureStorage {
    private mut prop encryptionKey: String {
        get() { loadKey() }
        set { saveKey(newValue) }
    }
    public func getDecryptedData() -> String {
// Use private attributes internally
        let key = encryptionKey
// Decryption logic
    }
}
```  

### 2. Attribute overlay and polymorphism
Subclasses can override the parent class attributes, and need to keep the type consistent and use `override` to modify:
```cj
open class Base {
    public open mut prop value: Int = 0
}
class Derived <: Base {
    public override mut prop value: Int {
get() { super.value * 2 } // Zoom twice when reading
set { super.value = newValue / 2 } // Shrink twice when writing
    }
}
```  

### 3. Attribute and type conversion
Attributes can play a role in type conversion, such as dynamic access to interface properties:
```cj
interface Measurable {
    prop value: Float64
}
class Thermometer <: Measurable {
    public prop value: Float64 = 25.0
}

let device: Any = Thermometer()
if let measurable = device as? Measurable {
println("Measured value: \(measurable.value)") // Dynamic access to properties
}
```  


## 4. Practical scenario: Dynamic management of equipment parameters

### Scenario: Design the parameter configuration module of the intelligent device, requiring automatic verification of parameter values, historical record tracking and network synchronization.

#### 1. Parameter base class: define attribute interface
```cj
abstract class DeviceParam<T> {
public abstract mut prop value: T // Abstract read and write properties
    public prop history: [T] = []
    protected func logChange(oldValue: T, newValue: T) {
        history.append(newValue)
syncToCloud(oldValue, newValue) // Abstract function, subclass implementation
    }
    protected abstract func syncToCloud(oldValue: T, newValue: T)
}
```  

#### 2. Specific parameters implementation: Temperature parameters
```cj
class TemperatureParam <: DeviceParam<Float64> {
    private var _value: Float64 = 25.0
    public override mut prop value: Float64 {
        get() { _value }
        set {
if newValue >= -40.0 && newValue <= 125.0 { // Temperature range verification
                let oldValue = _value
                _value = newValue
                logChange(oldValue: oldValue, newValue: newValue)
            } else {
throw Error("Temperature parameter is invalid: \(newValue)")
            }
        }
    }

    protected override func syncToCloud(oldValue: Float64, newValue: Float64) {
// Implement network synchronization logic
println("Synchronous temperature change: \(oldValue) → \(newValue)")
    }
}
```  

#### 3. Parameter management and polymorphic operations
```cj
let tempParam = TemperatureParam()
tempParam.value = 28.5 // Trigger verification, logging and synchronization
println("History: \(tempParam.history)") // Output: [28.5]

func updateParam(param: DeviceParam<Float64>, newValue: Float64) {
param.value = newValue // Polymorphic call, automatically adapts to specific parameter logic
}
```  


## 5. Common traps and optimization strategies

### 1. Avoid recursive calls of properties
Avoid calling itself directly or indirectly in `getter`/`setter` to prevent dead loops:
```cj
class Counter {
    private var _count: Int = 0
    public mut prop count: Int {
get() { count + 1 } // Recursively call getter, causing stack overflow
        set { _count = newValue }
    }
}
```  

### 2. Prefer attributes over public variables
Public variables destroy encapsulation, and properties can flexibly add verification logic:
```cj
// Counterexample: Directly expose public variables
class BadDesign {
public var volume: Int = 0 // Unlimited modification
}

// Formal example: limit the volume range through attributes
class GoodDesign {
    public mut prop volume: Int {
        set { volume = max(0, min(100, newValue)) }
    }
}
```  

### 3. Thread safety of static properties
In a multi-threaded environment, thread safety needs to be ensured for static attribute access, which can be achieved through mutex locks:
```cj
class ThreadSafeConfig {
    private static var _instance: ThreadSafeConfig?
    private static var lock = Mutex()
    public static prop instance: ThreadSafeConfig {
        get() {
            lock.lock()
            defer { lock.unlock() }
            return _instance ?? createNewInstance()
        }
    }
}
```  


## 6. Summary: The design philosophy of attributes
The attribute mechanism of HarmonyOS Next reflects the design idea of ​​"data is interface":
- **Encapsulation**: Hide internal storage details and provide a unified access portal through `getter`/`setter`;
- **Flexibility**: Supports complex logic such as verification, logging, synchronization, etc., to adapt to changes in business rules;
- **Polymorphism**: Combining interface and inheritance, realizing dynamic distribution of attribute behavior.
