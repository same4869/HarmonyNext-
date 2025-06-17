
# HarmonyOS Next full parsing of type conversion: safe adaptation practice from basic data to objects

In HarmonyOS Next development, type conversion is the core mechanism for implementing polymorphic programming and data interaction.Cangjie Language ensures the security and controllability of type conversion through a strict type system, combining the `is`, `as` operators and explicit conversion syntax.This article is based on the "Cangjie Programming Language Development Guide", combining document knowledge points to analyze type conversion rules and best practices in different scenarios.


## 1. Explicit conversion of basic data types
Cangjie language does not support implicit type conversion, and all basic type conversions need to be completed through explicit syntax to avoid runtime accidents.

### 1. Numerical type conversion: precise control and overflow processing
Use the `target type (expression)` syntax to support conversion between integers and floating-point numbers, and detect predictable overflows during the compilation period:
```cj
let intValue: Int32 = 255
let uintValue: UInt8 = UInt8(intValue) // Success: 255 is within the UInt8 range (0~255)
let overflowValue: Int8 = Int8(130) // Compilation error: 130 exceeds the Int8 range (-128~127)
```  

#### Conversion rules:
| Source Type | Target Type | Example | Results |
|--------------|----------------|---------------------------------------|-----------------------|  
| Integer → Unsigned | `UInt8(Int)` | `UInt8(-1)` | Runtime exception throwing |
| Float → Integer | `Int(Float)` | `Int(3.9)` | 3 (truncated instead of rounding) |
| Integer → Float | `Float(Int)` | `Float(10)` | 10.0 |

### 2. Rune and integer conversion: explicit processing of Unicode encoding
- **Rune to UInt32**: Get Unicode scalar value
  ```cj
  let symbol: Rune = '✨'
let code: UInt32 = UInt32(symbol) // 128293 (the specific value depends on the character encoding)
  ```  
- **Integer to Rune**: Make sure that the value is within the Unicode valid range (`0x0000`~`0xD7FF` or `0xE000`~`0x10FFFF`)
  ```cj
  let letterA: Int = 0x41 // 'A'
let char: Rune = Rune(letterA) // Success
let invalidCode: Int = 0x200000 // Out of range, throw exception during runtime
  ```  


## 2. Object type conversion: safe adaptation under polymorphic model
Object type conversion depends on subtype relationships, and dynamic type adaptation is achieved through `is` (type checking) and `as` (safe conversion) operators.

### 1. `is` operator: runtime type judgment
Returns a Boolean value to determine whether the object is a certain type or its subtype. It is often used in conditional branches:
```cj
open class Device {}
class Sensor <: Device {}

let device: Device = Sensor()
if device is Sensor {
println("Device is sensor type") // Output: The device is sensor type
}
println(device is Device) // true: The object itself is a Device type
```  

### 2. `as` operator: safe conversion and cast conversion
- **Safe conversion (`as?`)**: Returns the `Option` type, `None` when it fails
  ```cj
  let sensor: Device = Sensor()
  if let sensorImpl = sensor as? Sensor {
// Secure access to Sensor-specific members
      sensorImpl.readData()
  } else {
println("Conversion failed")
  }
  ```  
- **Captive (`as!`)**: Directly return to the target type, crashes when running (must ensure the correct type)
  ```cj
  let sensor: Device = Sensor()
let sensorImpl = sensor as! Sensor // cast, crash if the type is wrong
  ```  

### 3. Interface and class conversion rules
- **Class to Interface**: Class instances that implement interfaces can be implicitly converted to interface types (upward transformation)
  ```cj
  interface Communicable { func send(data: String) }
  class WifiModule <: Communicable {
public func send(data: String) { /* Implement send logic */ }
  }
let module: Communicable = WifiModule() // Legal, automatic upward transformation
  ```  
- **Interface to class**: It needs to be explicitly converted through `as` and succeeded only if the instance is actually type of this class
  ```cj
  let obj: Communicable = WifiModule()
  if let module = obj as? WifiModule {
// Access WifiModule-specific configuration interface
      module.setFrequency(2.4)
  }
  ```  


## 3. Subtype conversion rules for complex types

### 1. Tuple type: subtype constraints of element type
Tuple subtypes require that each element type be a child type of the corresponding parent type:
```cj
let intPoint: (Int, Int) = (1, 2)
let numberPoint: (Number, Number) = intPoint // Assume Int is a subtype of Number (sample scenario)
// Legal: Int is a Number subtype, and the entire tuple is a subtype

let mixedPoint: (Int, String) = (1, "x")
let errorPoint: (Number, Number) = mixedPoint // Compile error: String non-Number subtype
```  

### 2. Function type: Covariance/inversion of parameters and return values
Function type `(S) -> R` is a subtype of `(T) -> U`, which must meet:
- Parameter type `T <: S` (inverter)
- Return type `R <: U` (covariance)
```cj
func superFunc(arg: Device) -> String { "Device" }
func subFunc(arg: Sensor) -> Sensor { Sensor() }

// Legal: The parameter Sensor is a Device subtype, and the return Sensor is Any subtype
let funcVar: (Device) -> Any = subFunc 
```  

### 3. Generic Type: Constrained Subtype Relationship
Generic functions can limit the validity of type conversions through the `where` clause:
```cj
func printDeviceInfo<T: Device>(device: T) where T <: Communicable {
device.send(data: "INFO") // Ensure T implements the Communicable interface
println("Device type: \(typeNameOf(T.self))")
}

// Call example: Pass in the Sensor class that implements Communicable
let sensor: Sensor = Sensor()
printDeviceInfo(device: sensor)
```  


## 4. Typical traps and evasion strategies for type conversion

### 1. Runtime errors caused by type erasing
Generic containers may lose specific type information, causing the `as` conversion to fail:
```cj
let values: Array<Any> = [1, "text", Sensor()]
let number = values[0] as? Int // Successful, runtime type is Int
let sensor = values[2] as? Sensor // Successful, runtime type is Sensor
let str = values[1] as? Int // Failed, runtime type is String
```  

### 2. Avoid overuse of casts
Cases (`as!`) destroy type safety and should be avoided by design:
```cj
// Counterexample: Relying on casts, there is a risk of crash
let obj: Any = FileHandle()
let handle = obj as! NetworkHandle // If obj is not a NetworkHandle type, it crashes

// Positive example: check the type first and then convert it
if let handle = obj as? NetworkHandle {
// Use handle safely
} else {
error("Unsupported handle type")
}
```  

### 3. Integrity check of interface implementation
If the class does not fully implement the interface, the type conversion may fail implicitly:
```cj
interface TwoActions {
    func action1()
    func action2()
}
class PartialImplementation <: TwoActions {
public func action1() {} // action2 is not implemented, compilation error
}
```  


## 5. Practical scenario: Type conversion design of equipment adaptation layer
### Scenario: Build a cross-device data processing layer to uniformly parse data in different formats

#### 1. Define unified interface and specific data classes
```cj
// Unified data interface
interface DataModel {
    func toJSON(): String
}

// Data format of device A (class)
class DeviceAData <: DataModel {
    private let value: Int
    public func toJSON(): String {
        "{\"value\": \(value)}"
    }
}

// Data format (structure) of device B
struct DeviceBData <: DataModel {
    let code: String
    public func toJSON(): String {
        "{\"code\": \"\(code)\"}"
    }
}
```  

#### 2. Type conversion and polymorphic processing of adapter layer
```cj
func processData(data: Any) {
if let model = data as? DataModel { // Convert to unified interface
        let json = model.toJSON()
        uploadToCloud(json)
    } else {
println("Unsupported data type")
    }
}

// Call example
let dataA = DeviceAData(value: 100)
let dataB = DeviceBData(code: "DEV_B")
processData(data: dataA) // Convert successfully and processed
processData(data: "raw_data") // Output: Unsupported data types
```  

#### 3. Generic Optimization: Constrain input types
```cj
func safeProcessData<T: DataModel>(data: T) {
let json = data.toJSON() // Directly call the interface method without conversion
// Other processing logic
}
```  


## 6. Summary: The safe way to type conversion
The type conversion system of HarmonyOS Next follows the design concept of "explicit priority, safe and controllable":
- **Basic type**: Avoid implicit errors through explicit conversion, and overflow processing ensures stability;
- **Object type**: Depend on `is`/`as` to implement safe polymorphic conversion, prohibiting unsafe implicit conversion;
- **Architecture Design**: Reduce the dependence of runtime type conversion through interfaces and generic constraints and improve code maintainability.
