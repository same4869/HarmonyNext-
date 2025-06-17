
# HarmonyOS Next type conversion security and controllability practice: full-link guarantee from compilation period to runtime

In HarmonyOS Next development, the security and controllability of type conversion are the cornerstones for building robust systems.Cangjie Language ensures the dual reliability of type conversion during the compile period and runtime through **explicit conversion rules**, **runtime type checks** and ** strict subtype constraints.This article combines the "Cangjie Programming Language Development Guide" to analyze the core mechanisms and practical points of type conversion from basic data to object types.


## 1. Basic data type: precise control of explicit conversion
Cangjie Language** completely prohibits implicit type conversion, requiring developers to complete data type conversion through explicit syntax to avoid potential risks caused by automatic conversion.

### 1. Numerical type: double verification between compilation period and runtime
#### (1) Explicit conversion syntax and rules
Use the `target type (expression)` syntax, for example:
```cj
let intValue: Int32 = 255
let uint8Value: UInt8 = UInt8(intValue) // Legal: 255 is within the UInt8 range (0~255)
let overflowValue: Int8 = Int8(130) // Compilation error: 130 exceeds the Int8 range (-128~127)
```  

#### (2) Conversion rules and risk scenarios
| Conversion direction | Sample code | Results description | Security mechanism |
|------------------|-------------------------|-----------------------------------|--------------------------------|  
| Integer → Unsigned integer | `UInt8(-1)` | Exceeding exception at runtime | Negative number exceeds the range of unsigned type |
| Float number → Integer | `Int(3.9)` | Result is 3 (truncated instead of rounding) | Clear truncated semantics to avoid implicit rounding |
| Integer → Floatpoint | `Float64(1024)` | The result is 1024.0 | Precision lossless conversion |
| Rune → UInt32 | `UInt32('π')` | Get Unicode scalar value (such as 960) | Direct map character encoding |
| Integer → Rune | `Rune(0x200000)` | Runtime exception throwing | Exceeding Unicode valid range (0xD7FF~0xE000) |

### 2. Avoid fuzzy transformation: clarify business logic boundaries
In scenarios involving unit conversion or precision sensitive (such as sensor data parsing), explicit conversion can avoid implicit errors:
```cj
// The sensor returns the UInt32 temperature value and needs to be converted to Celsius temperature (range -40~85℃)
let rawTemp: UInt32 = 300 // Assume that the original value is 300 (actually meaning is 30.0℃)
if rawTemp > 850 { // Check the range first, then convert
throw Error("Temperature value exceeds safety range")
}
let celsius: Int8 = Int8(rawTemp / 10) // explicitly convert and process business logic
```  


## 2. Object type conversion: security guard at runtime
Object type conversion depends on subtype relationships, and the `is` and `as` operators realize the ** type check** and ** safe conversion** to ensure the correctness of types in polymorphic scenarios.

### 1. `is` operator: pre-checking of type existence
Before performing a conversion, use `is` to determine whether the object is a target type or its subtype to avoid invalid conversion:
```cj
open class Device { /* Device base class */ }
class Sensor <: Device { /* Sensor subclass */ }

func processDevice(device: Device) {
if device is Sensor { // Check whether it is a sensor type first
let sensor = device as! Sensor // Combined with is to ensure the safety of cast conversion
sensor.readEnvironmentData() // Call subclass-specific methods
    } else {
device.basicOperation() // Handle base class logic
    }
}
```  

### 2. `as` operator: the trade-off between safe conversion and cast conversion
#### (1) Safe conversion (`as?`): Returns the `Option` type
Use optional values ​​to handle conversion failure scenarios to avoid program crashes:
```cj
let device: Device = getRandomDevice() // It may return any Device subclass
if let sensor = device as? Sensor {
// Secure access to Sensor properties and methods
println("Sensor Model: \(sensor.model)")
} else if let actuator = device as? Actuator {
// Process the executor logic
} else {
println("Unknown device type")
}
```  

#### (2) Cases (`as!`): a last resort to careful use
Use only when ensuring type correctness, otherwise crashes at runtime:
```cj
// Scenario where explicitly knows that device is a Camera instance (such as factory function returns)
let camera = device as! Camera 
camera.startPreview() // Assuming device is indeed Camera type, it will crash
```  

### 3. Interface and class conversion rules: Strict compliance with subtype relationships
- **Class-to-interface**: Class instances that implement interfaces can be implicitly converted to interface types (upward transformation), without explicit operations:
  ```cj
  interface Communicable { func send(data: String) }
  class WifiModule <: Communicable {
public func send(data: String) { /* Implement send logic */ }
  }
let module: Communicable = WifiModule() // Legal, automatic upward transformation
  ```  
- **Interface to class**: It needs to be explicitly converted through `as` and succeeds only if the actual type of the instance matches:
  ```cj
  let communicable: Communicable = WifiModule()
  if let wifiModule = communicable as? WifiModule {
wifiModule.setChannel(6) // Access subclass-specific configuration
  }
  ```  


## 3. Subtype constraints of complex types: static verification during compilation period
### 1. Tuple type: covariant rules for element types
Tuple subtypes require that each element type is a child type of the corresponding parent type, and the compiler performs static checks when assigning:
```cj
let intPoint: (Int, Int) = (1, 2)
let numberPoint: (Number, Number) = intPoint // Assume Int is a Number subtype (sample scenario)
// Legal: The whole tuple is a subtype, and the element types all satisfy the subtype relationship

let mixedPoint: (Int, String) = (1, "x")
let errorPoint: (Number, Number) = mixedPoint // Compile error: String non-Number subtype
```  

### 2. Function type: inverter/covariation of parameters and return values
Function type `(S) -> R` is a subtype of `(T) -> U`, which must meet:
- Parameter type `T <: S` (inverter, parameter type is more specific)
- Return type `R <: U` (covariant, return type is more abstract)
```cj
func superFunc(arg: Device) -> String { "Device" } // Parent type parameter, child type returns value
func subFunc(arg: Sensor) -> Any { "Sensor" } // Subtype parameter, parent type returns value

let funcVar: (Device) -> String = subFunc // Legal: parameter Sensor<:Device, return Any<:String
```  

### 3. Generic type: Constrained by the `where` clause
Use the `where` clause in a generic function to force the type to satisfy multiple interfaces or inheritance relationships:
```cj
func printDeviceInfo<T: Device>(device: T) where T <: Communicable & Configurable {
device.send(data: "INFO") // Ensure T implements the Communicable interface
device.configure(settings: defaultConfig) // Ensure T implements the Configurable interface
println("Device type: \(typeNameOf(T.self))")
}
```  


## 4. Typical traps and defensive programming strategies
### 1. Runtime errors caused by type erasing
Generic containers (such as `Array<Any>`) will lose specific type information and need to be run-time verification through `is` or `as?`:
```cj
let data: Any = getFromCache() // May be Int, String or custom type
if let number = data as? Int {
    processNumber(number)
} else if let str = data as? String {
    processString(str)
} else if let custom = data as? CustomModel {
    processCustom(custom)
} else {
throw Error("Unsupported data type") // Defensive bottom-up processing
}
```  

### 2. Circular dependency and conversion failure
Round references may cause objects to not be recycled correctly, which in turn raises a type conversion exception.Breaking the loop with `weak` weak reference:
```cj
class Node {
var parent: Node? // Strong reference of parent node
weak var child: Node? // Weak reference of child nodes to avoid loops
}
```  

### 3. The interface implements incomplete compile period checking
If the class does not fully implement the interface, the compiler will force an error to avoid crashes during runtime due to missing methods:
```cj
interface TwoFunctions {
    func f1()
    func f2()
}
class PartialImpl <: TwoFunctions {
public func f1() {} // F2 is not implemented, compilation error: interface members are not fully implemented
}
```  


## 5. Practical scenario: Type safety design of equipment adaptation layer
### Scenario: Cross-device data analysis module
Define the unified interface `DataParser`, which supports parsing data in different formats (JSON/XML/binary), and implements polymorphic processing through type conversion:
```cj
// Unified parsing interface
interface DataParser {
    func parse(data: String) -> Any
}

// JSON parser
class JSONParser <: DataParser {
    public func parse(data: String) -> Any {
// JSON parsing logic
    }
}

// XML parser
class XMLParser <: DataParser {
    public func parse(data: String) -> Any {
// XML parsing logic
    }
}

// Adaptation layer functions: safe conversion and polymorphic calls
func processData(data: String, parser: Any) {
if let parser = parser as? DataParser { // Convert to unified interface
        let result = parser.parse(data: data)
        handleResult(result)
    } else {
println("Unsupported parser type")
    }
}

// Use example
let jsonParser = JSONParser()
processData(data: "{...}", parser: jsonParser) // Safely call JSON parsing logic
```  


## 6. Summary: Full-link guarantee for type safety
The type conversion system of HarmonyOS Next ensures security and controllability through the following mechanisms:
1. **Compilation period verification**: Prohibit implicit conversion, forcing interfaces to achieve integrity, and generic constraints;
2. **Runtime Protection**: The `is`/`as` operator avoids invalid conversion and `Option` type processing failure scenarios;
3. **Architecture Design**: Prioritize the use of interface abstraction and generic constraints to reduce type conversion dependencies.
