
# HarmonyOS Next basic data types detailed explanation: In-depth analysis from boolean to integers

In HarmonyOS Next development, data types are the cornerstone of building programs.Cangjie Language provides a rich and rigorous basic data type system, which not only follows international standards (such as the IEEE 754 floating point specification), but also optimizes for scenarios such as the Internet of Things and high-performance computing.This article will expand from five dimensions: boolean type, integer type, floating point type, character type and special type, combining sample code and application scenarios to help developers deeply understand the characteristics and best practices of data types.


## 1. Boolean type: the cornerstone of logical operations
The Boolean type (`Bool`) is the core of logical judgment, and the value is `true` (true) or `false` (false), which is used for conditional judgment, loop control and other scenarios.Unlike C language, Cangjie language strictly prohibits implicit conversion of non-Bolean types to Boolean values ​​to avoid the logical vulnerability of "non-zero or true".

### 1. Basic usage
```cj
let isReady: Bool = true
let hasError: Bool = false

// Conditional judgment
if isReady {
    println("System is ready")
} else {
    println("System is initializing")
}

// Logical operations
let isSafe = isReady && !hasError // with operation
let isAlert = isReady || hasError // or operation
```

### 2. Type Safety Design
- **Implicit conversion is prohibited**: `Int` and other types are not allowed to directly assign values ​​to `Bool`, and explicit judgment is required (such as `let isPositive = num > 0`).
- **TriState Logic Extension**: If you need to deal with "unknown state", you can define the enum `enum TriState { true, false, unknown }` to adapt to complex business scenarios.


## 2. Integer type: precisely control the numerical range
Integer types are divided into two categories: signed (`Int`) and unsigned (`UInt`), covering 8-bit to 64-bit and platform-related types (`IntNative`/`UIntNative`), to meet the numerical accuracy and storage needs of different scenarios.

### 1. Type range and selection suggestions
| Type | Representation Range | Typical Scenario |
|---------|-------------------------|------------------------------|
| `Int8` | -128 ~ 127 | Sensor data (such as temperature value) |
| `UInt8` | 0 ~ 255 | Communication protocol bytes (such as HTTP status code) |
| `Int32` | -2147483648 ~ 2147483647 | Normal integer calculation (such as user ID) |
| `Int64` | -9223372036854775808 ~ 9223372036854775807 | Big data calculation (such as financial transaction amount) |
| `IntNative` | Platform related (such as `Int64` for 64-bit system) | Underlying pointer operation |

### 2. Bit operation and practical skills
Integer types support bitwise and (`&`), or (`|`), XOR (`^`), left shift (`<<`), right shift (`>>`), etc., and are suitable for scenarios such as underlying protocol analysis and graphics rendering.

**Example: RGB color component extraction**
```cj
let pixel: UInt32 = 0xFF00FF00 // ARGB format (assuming the highest 8 bits are Alpha)
let red = (pixel >> 16) & 0xFF // Extract red component (0x00)
let green = (pixel >> 8) & 0xFF // Extract green component (0xFF)
let blue = pixel & 0xFF // Extract blue component (0x00)
```

### 3. Overflow Detection and Safety Programming
The Cangjie compiler enables integer overflow detection by default, and an error will be reported when it exceeds the type range.For scenarios where overflow needs to be handled explicitly, security operators such as `&+`, `&-`, and `&*` can be used.

```cj
let a: Int8 = 127
let b: Int8 = a &+ 1 // Safe addition, the result is -128 (overflow wrap)
// let c: Int8 = a + 1 // Compile error: Overflowing the Int8 range
```


## 3. Floating point type: the core of scientific computing
The floating point type is based on the IEEE 754 standard, including `Float16` (half-precision), `Float32` (single precision), and `Float64` (double precision). It is suitable for scenes with high requirements for decimal accuracy, such as scientific computing, graphics rendering, etc.

### 1. Accuracy comparison and selection suggestions
| Type | Accuracy (decimal) | Number of significant digits | Memory usage | Typical scenarios |
|----------|----------------|--------------|----------|------------------------|
| `Float16` | About 3 decimal places | 5-6 digits | 2 bytes | IoT sensor data |
| `Float32` | About 6 decimal places | 7-8 bits | 4 bytes | 3D graphics coordinate calculation |
| `Float64` | About 15 decimal places | 15-17 digits | 8 bytes | Financial computing, encryption algorithms |

**Example: Pi calculation error with different accuracy**
```cj
let pi16: Float16 = 3.1415926f16 // Stored as 3.140625 (Error about 0.00097)
let pi32: Float32 = 3.1415926f32 // Stored as 3.1415926535 (Error about 1e-8)
let pi64: Float64 = 3.141592653589793f64 // High-precision approximation
```

### 2. Hexadecimal floating point literal
Supports hexadecimal floating-point representation through the `0x` prefix, which is suitable for scenarios such as underlying hardware register configuration, encryption key generation, etc.
```cj
let value = 0x1.1p0 // Hexadecimal 1.1 (binary 1.000110011...) multiplied by 2^0, equal to decimal 1.0625
```

### 3. Guide to avoid pitfalls in financial calculations
There is accuracy error in floating point types, and financial scenarios require the use of the `Decimal` type (decimal fixed precision).
```cj
import std.decimal.*

let amount1: Decimal = 0.1
let amount2: Decimal = 0.2
let sum = amount1 + amount2 // Exactly equal to 0.3, no floating point error
```


## 4. Characters and special types: the key to Unicode and control flow
### 1. `Rune` type: Unicode fully compatible
`Rune` is used to represent any Unicode character (including Emoji and uncommon characters). The underlying layer corresponds to the Int32 type and supports UTF-8 encoding conversion.
```cj
let chinese = r'\u{4f60}' // Character "you", Unicode code point 0x4F60
let emoji = r'\u{1F603}' // Smiley Emoji, need to be a proxy to store
println(String(chinese) + "Okay, world!" + String(emoji))
```

### 2. `Unit` and `Nothing` types
- **`Unit`**: indicates that there is no valid return value, similar to `void` in C language, but is an explicit type (the unique value is `()`).
  ```cj
  func printGreeting(): Unit {
      println("Hello, HarmonyOS Next!")
  }
  ```
- **`Nothing`**: means never return (such as `break`, `throw`), used to control flow interruptions.
  ```cj
  while true {
      if condition {
break // Return type is Nothing, terminates the loop
      }
  }
  ```


## 5. Type conversion: the balance between safety and efficiency
### 1. Explicit conversion rules
- **Numerical conversion**: Follow the principle of "width to narrow, narrow to narrow, and narrow to wide can be expanded".
  ```cj
  let num: Int32 = 1000
let byte: UInt8 = num.toUInt8() // truncated to 232 (1000 % 256)
  ```
- **Convert characters and numeric values**: `Rune` is binary equivalent to `UInt32`, and can be converted directly.
  ```cj
let rune: Rune = r'\u{4e2d}' // Character "in"
  let code: UInt32 = rune.toUInt32()  // 0x4E2D
  ```

### 2. Custom type conversion
Custom type conversion logic (such as complex to floating point) is implemented through operator overloading.
```cj
struct Complex {
    var real: Float64
    var imaginary: Float64
}

func toFloat(complex: Complex) -> Float64 {
    return sqrt(complex.real * complex.real + complex.imaginary * complex.imaginary)
}
```


## Summarize
HarmonyOS Next's data type system takes "type safety" and "performance optimization" as its core design concepts, which not only meets daily business development needs, but also provides accurate control capabilities for scenarios such as high-performance computing and Internet of Things edge devices.Developers need to choose the appropriate type according to the scenario (such as `Decimal` for financial computing and `Float16` for sensor data), and master the skills of type conversion, overflow detection, etc. to ensure the stability and efficiency of the program.
