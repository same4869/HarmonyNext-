
# HarmonyOS Next type safety practice: Strong type checking and overflow control

In HarmonyOS Next development, type safety is the core of ensuring program stability.Cangjie Language avoids type-related risks from the compilation period to the runtime through mechanisms such as **Strong type check**, **numerical overflow detection** and **high-precision types (such as `Decimal`).This article will analyze best practices for type safety in combination with scenarios such as financial computing and embedded control.


## 1. Strong type checking: eliminate implicit conversion vulnerabilities
Cangjie language strictly prohibits non-secure implicit type conversion. All type conversions must be explicitly declared to avoid logical errors caused by type mismatch.

### 1. Type safety of conditional expressions
- **Counterexample (C language style, implicit conversion causes vulnerability)**
  ```c
  int a = 0;
if (a) { /* Execution logic */ } // Non-zero is true, it may be misjudged
  ```  
- **Positive example (Cangjie language, forced boolean type)**
  ```cj
  let a: Int = 0
if a != 0 { /* Explicit comparison to avoid misjudgment */ }
  ```  

### 2. Function parameter type matching
The compiler strictly checks the function parameter type and directly reports an error when it does not match.
```cj
func greet(name: String) { println("Hello, \(name)") }
greet(123) // Compilation error: Int cannot be implicitly converted to String
```  

### 3. Enumerated types of secure access
Enum values ​​must be explicitly matched to avoid runtime errors caused by unprocessed branches.
```cj
enum Color { red, green, blue }
func render(color: Color) {
    when (color) {
case.red: print("Rendering red")
case.green: print("Rendering green")
// When case.blue is not matched, the compiler forces the default branch to be added
default: fatalError("Unprocessed color")
    }
}
```  


## 2. Numerical overflow control: protection from compilation period to runtime
Overflow of numerical types may cause data errors or security vulnerabilities (such as integer back attacks), and Cangjie Language provides multiple protection mechanisms.

### 1. Compilation period overflow detection
Overflow checking is enabled by default, and expressions that exceed the type range will trigger a compilation error.
```cj
let a: Int8 = 127 + 1 // Compile error: The maximum value of Int8 is 127
// Solution: Use security operator &+
let b: Int8 = 127 &+ 1 // The runtime result is -128 (wrapped), and needs to be processed explicitly
```  

### 2. Runtime overflow processing
Catch overflow exceptions through the `safe` keyword, suitable for dynamic computing scenarios.
```cj
func calculateRiskFactor(a: Int32, b: Int32) -> Int32? {
    let result = a * b safe { error in
println("Multiple overflow: \(error)") // Handle overflow events
    }
    return result
}

let factor = calculateRiskFactor(2147483647, 2) // 2147483647*2=4294967294 (Int32 overflow)
if let value = factor { /* Use result */ } else { /* Overflow handling */ }
```  

### 3. Safe use of unsigned types
Unsigned types (such as `UInt`) are often used in the underlying protocol, and attention should be paid to boundary value processing.
```cj
let len: UInt16 = 0 // Legal minimum value
let maxLen: UInt16 = 65535 // Legal maximum value
let invalidLen: UInt16 = -1 // Compilation error: Unable to assign negative numbers to unsigned types
```  


## 3. High-precision type: financial computing and scientific modeling
For precision-sensitive scenarios (such as financial transactions, encryption algorithms), the `Decimal` type needs to be used instead of the floating-point type to avoid cumulative errors.

### 1. Accurate calculation of `Decimal`
```cj
import std.decimal.*

// Float64 cannot accurately represent 0.1)
let floatSum = 0.1 + 0.2 // The result is 0.3000000000000000004
println(floatSum) // Output: 0.3000000000000000004

// Decimal accurate calculation
let dec1: Decimal = 0.1
let dec2: Decimal = 0.2
let decSum = dec1 + dec2 // exact equal to 0.3
println(decSum) // Output: 0.3
```  

### 2. Best practices in currency calculation
```cj
struct Currency {
    var amount: Decimal
    var symbol: String

    func add(_ other: Currency) -> Currency? {
guard symbol == other.symbol else { return nil } // Currency consistency check
        return Currency(amount: amount + other.amount, symbol: symbol)
    }
}

let usd1 = Currency(amount: 100.50, symbol: "$")
let usd2 = Currency(amount: 200.75, symbol: "$")
let total = usd1.add(usd2) // The result is 301.25$, no accuracy loss
```  

### 3. Error control in scientific calculations
In scenarios such as encryption algorithms and physical simulations, the accuracy needs to be ensured by combining `Decimal` and generics.
```cj
func encrypt(data: String, key: Decimal) -> String {
// Use Decimal to perform key calculations to avoid decryption failure caused by floating point errors
    let encrypted = data.map { char in
        let offset = key.truncatingRemainder(dividingBy: 256)
        return String(UnicodeScalar(UInt8(char.asciiValue! + Int(offset.toUInt8()))))
    }
    return encrypted.joined()
}
```  


## 4. Custom type safety: protocol constraints and operator limitations
Add compile-time security constraints to custom types through protocol and operator overloading.

### 1. Protocol constraints: Ensure type capability
```cj
protocol Validatable {
    func validate() -> Bool
}

struct User: Validatable {
    var age: Int

    func validate() -> Bool {
return age >= 0 && age <= 150 // Age legality check
    }
}

func processUser<T: Validatable>(user: T) {
guard user.validate() else { fatalError("User data invalid") }
// Secure processing of user data
}
```  

### 2. Security design of operator overloading
Limit the operator parameter types of custom types to avoid illegal operations.
```cj
struct Distance {
    var value: Decimal
    var unit: String  // m, km, etc.
}

// Only the same unit of distance addition is allowed
func +(lhs: Distance, rhs: Distance) -> Distance? {
    guard lhs.unit == rhs.unit else { return nil }
    return Distance(value: lhs.value + rhs.value, unit: lhs.unit)
}

let meter1 = Distance(value: 100, unit: "m")
let meter2 = Distance(value: 200, unit: "m")
let total = meter1 + meter2 // Legal, the result is 300m
let km = Distance(value: 1, unit: "km")
let invalid = meter1 + km // There is no error during the compilation period, and nil is returned during runtime (need to be explicitly processed)
```  


## Summarize
HarmonyOS Next's type safety system builds a full-link guarantee from development to operation through strong type checks, overflow protection and high-precision types:
- Strongly typed rules eliminate implicit conversion vulnerabilities and improve code maintainability;
- Numerical overflow detection prevents program crashes due to boundary values;
- `Decimal` and other types meet the accuracy needs of finance and scientific computing.
