# HarmonyOS Next type conversion practice: a guide to safe conversion from basic data to objects

> In distributed device development, type conversion is like a translator in different languages.The on-board system collapsed due to coercive conversion. Later, this safety conversion system was summarized. Now I will share it with you to avoid pitfalls.


## 1. Basic type conversion: the safety bottom line of explicit operation

### 1. Numerical type conversion rules
- Must be explicitly converted: `target type (value)`
- Overflow protection: Compilation period checks limit value exceeded
```cj
let a: Int32 = 200
let b: Int8 = Int8(a) // Compile error: 200 out of Int8 range
let c: UInt32 = UInt32(a) // Correct: 200 within the UInt32 range
```  

### 2. Rune and numerical value transfer
- Rune→UInt32: Get Unicode code points
- UInt32→Rune: Make sure the value is within the range of 0x0-0x10FFFF
```cj
let rune: Rune = 'medium'
let code: UInt32 = UInt32(rune)  // 20013
let invalid: Rune = Rune(0x200000) // Runtime exception
```  


## 2. Object conversion: a security bridge in a polymorphic world

### 1. Type Check Three Musketeers
- `is`: judge type (return to Bool)
- `as?`: Safe conversion (return to None if failed)
- `as!`: Cases (failed crash)

```cj
open class Animal {}
class Dog <: Animal {}

let pet: Animal = Dog()
if pet is Dog {
let dog = pet as? Dog // Safe conversion
    dog.bark()
}
```  

### 2. Transformation logic between interface and class
- Class → Interface: Implicit Upward Transformation (Polymorphic Basics)
- Interface → Class: Explicit downward transformation (need to type matching)

```cj
interface Flyable {}
class Bird <: Flyable {}

let bird: Bird = Bird()
let flyable: Flyable = bird // Legal, interface transformation
let backToBird = flyable as? Bird // Convert successfully
```  


## 3. Cross-scene conversion traps and countermeasures

### 1. Type erase trap
Generic containers lose specific type information:
```cj
let list: Array<Any> = [Dog()]
let dog = list[0] as? Dog // Success
let cat = list[0] as? Cat // Failed, return None
```  

### 2. Cases abuse
Counterexample (danger):
```cj
let obj: Any = "text"
let num = obj as! Int // crashes during runtime
```  
Regular example (safety):
```cj
if let str = obj as? String {
    processString(str)
}
```  


## 4. Practical combat: Type conversion design of equipment adaptation layer

### 1. Unified interface definition
```cj
interface DeviceData {
    func toJSON(): String
}

class DeviceAData <: DeviceData {
    private let value: Int
    public func toJSON() -> String {
        "{\"value\": \(value)}"
    }
}
```  

### 2. Adaptation layer conversion logic
```cj
func processData(data: Any) {
    if let deviceData = data as? DeviceData {
        let json = deviceData.toJSON()
        sendToCloud(json)
    } else {
print("Unsupported Type")
    }
}
```  


## 5. The golden rule of safe conversion

1. **Basic Type**: Always explicit conversion, using compile-time overflow check
2. **Object conversion**: Priority for `as?` safe conversion, avoid `as!` cast
3. **Architecture Design**: Reduce runtime conversion requirements through interface abstraction
