
# HarmonyOS Next type conversion deep analysis: safe adaptation from basic data to objects

In HarmonyOS Next development, type conversion is a key link in realizing polymorphic programming and data interaction.Cangjie Language ensures the security and controllability of type conversion through a strict type system, combining the `is` and `as` operators and explicit conversion syntax.This article is based on the "Cangjie Programming Language Development Guide" and analyzes the type conversion rules and best practices in different scenarios.


## 1. Basic data type conversion: explicit operations and overflow processing
Cangjie language does not support implicit type conversion, and all basic data type conversions need to be performed explicitly to avoid runtime accidents.

### 1. Numerical type conversion
Use the `target type (expression)` syntax to support conversion between integers and floating-point numbers:
```cj
let intValue: Int32 = 100
let uintValue: UInt32 = UInt32(intValue) // 100
let floatValue: Float32 = Float32(intValue) // 100.0

// Overflow processing: Overflow errors that can be detected during the compilation period
let overflow: Int8 = Int8(130) // Compilation error: 130 exceeds the Int8 range (-128~127)
```  

### 2. Conversion between Rune and integers
- **Rune to UInt32**: Get Unicode scalar value
  ```cj
  let char: Rune = 'π'
  let code: UInt32 = UInt32(char) // 960
  ```  
- **Integer to Rune**: Make sure the value is within the valid range of Unicode
  ```cj
  let validCode: Int = 0x41 // 'A'
let char: Rune = Rune(validCode) // Success
let invalidCode: Int = 0x200000 // Out of range, throw exception during runtime
  ```  


## 2. Object type conversion: safe adaptation under polymorphic model
Object type conversion depends on subtype relationships, and is implemented through the `is` (type check) and `as` (safe conversion) operators.

### 1. `is` operator: runtime type judgment
Returns a Boolean value to determine whether the object is of a certain type or its subtype:
```cj
open class Animal {}
class Dog <: Animal {}

let pet: Animal = Dog()
println(pet is Dog) // true: Dog is a subclass of Animal
println(pet is Animal) // true: judging one's own type
```  

### 2. `as` operator: safe conversion and cast conversion
- **Safe conversion**: Returns the `Option` type, `None` when it fails
  ```cj
  let animal: Animal = Dog()
if let dog = animal as? Dog { // Safe conversion
println("Conversion is successful, it is a Dog instance")
  } else {
println("Conversion failed")
  }
  ```  
- **Captive**: Use `as!`, if it fails, it crashes at runtime (must make sure the type is correct)
  ```cj
let dog: Dog = animal as! Dog // cast, if animal is not Dog instance, it will crash
  ```  

### 3. Interface and class conversion rules
- **Class to Interface**: Class instances that implement interfaces can be implicitly converted to interface types (upward transformation)
  ```cj
  interface Flyable {}
  class Bird <: Flyable {}
  let bird: Bird = Bird()
let flyable: Flyable = bird // Legal, Bird implements the Flyable interface
  ```  
- **Interface to class**: It needs to be explicitly converted through `as` and succeeded only if the instance is actually type of this class
  ```cj
  let obj: Flyable = Bird()
if let bird = obj as? Bird { // Conversion is successful
// Access Bird-specific members
  }
  ```  


## 3. Type conversion between cross-package and generic scenes
### 1. Limitations of cross-packet type conversion
If the interface or class is defined in other packages, you need to pay attention to the impact of the `sealed` modifier:
```cj
// Define sealed interface in package A
package A
sealed interface InternalService {}

// Try to implement it in package B
package B
import A.*
class ServiceImpl <: InternalService {} // Compilation error: sealed interface is only implemented in package A
```  

### 2. Type constraints in generic functions
Restrict the effectiveness of type conversion by generic constraints, for example, only types that implement specific interfaces can participate in conversion:
```cj
func processData<T: Loggable>(data: T) {
if data is Serializable { // Require T to implement both Loggable and Serializable
        let serializable = data as? Serializable
// Handle serialization logic
    }
}
```  

### 3. Subtype conversion of tuples and function types
- **Tuple Type**: When each element type is a subtype, the tuple is a subtype
  ```cj
  let point: (Int, Int) = (1, 2)
let superPoint: (Number, Number) = point // Assume Int is a subtype of Number (Sample Scenario)
  ```  
- **Function type**: When the parameter type is parent type, the return type is child type, the function is child type
  ```cj
  func superFunc(x: Number) -> Animal { /* ... */ }
  func subFunc(x: Int) -> Dog { /* ... */ }
let funcVar: (Number) -> Animal = subFunc // Legal, subtype functions can be assigned to parent-type function variables
  ```  


## 4. Typical traps and evasion strategies for type conversion

### 1. Runtime errors caused by type erasing
Generic containers may lose specific type information, resulting in the `as` conversion failure:
```cj
let list: Array<Any> = [Dog()]
let dog = list[0] as? Dog // Successful, runtime type is Dog
let wrongType = list[0] as? Cat // Failed, return None
```  

### 2. Avoid overuse of casts
Cases (`as!`) destroy type safety and should be avoided by design:
```cj
// Counterexample: Relying on casts, there is a risk of crash
let obj: Any = "text"
let num = obj as! Int // crashes during runtime

// Positive example: check the type first and then convert it
if let str = obj as? String {
// Handle string logic
}
```  

### 3. Integrity check of interface implementation
If the class does not fully implement the interface, the type conversion may fail implicitly:
```cj
interface TwoFunctions {
    func f1()
    func f2()
}
class PartialImpl <: TwoFunctions {
public func f1() {} // f2 is not implemented, compilation error
}
```  


## 5. Practical scenario: Type conversion design of equipment adaptation layer
### Scenario: Build a cross-device adaptation layer and uniformly process data formats of devices of different brands

#### 1. Define unified interface and specific device classes
```cj
// Unified data interface
interface DeviceData {
    func toJSON(): String
}

// Data format of device A (class)
class DeviceAData <: DeviceData {
    private let value: Int
    public func toJSON(): String {
        "{\"value\": \(value)}"
    }
}

// Data format (structure) of device B
struct DeviceBData <: DeviceData {
    let code: String
    public func toJSON(): String {
        "{\"code\": \"\(code)\"}"
    }
}
```  

#### 2. Type conversion and polymorphic processing of adapter layer
```cj
func processDeviceData(data: Any) {
if let deviceData = data as? DeviceData { // Convert to unified interface
        let json = deviceData.toJSON()
        sendToCloud(json)
    } else {
println("Unsupported data type")
    }
}

// Call example
let dataA = DeviceAData(value: 100)
let dataB = DeviceBData(code: "DEV_B")
processDeviceData(data: dataA) // Successfully converted and processed
processDeviceData(data: "invalid") // Output unsupported data types
```  

#### 3. Generic Optimization: Constrain input types
```cj
func safeProcessData<T: DeviceData>(data: T) {
let json = data.toJSON() // Directly call the interface method without conversion
// Other processing logic
}
```  


## 6. Summary: The safe way to type conversion
The type conversion system of HarmonyOS Next embodies the design concept of "explicit priority, safe and controllable":
- **Basic type**: Avoid implicit errors through explicit conversion, and overflow processing ensures stability;
- **Object type**: Relying on `is`/`as` to achieve safe polymorphic conversion, prohibiting unsafe implicit conversion;
- **Architecture Design**: Reduce the dependence of runtime type conversion through interfaces and generic constraints and improve code maintainability.
