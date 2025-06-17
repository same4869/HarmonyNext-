
# HarmonyOS Next Enumeration Type Basics: Definition and Parameterless Constructor Application

In HarmonyOS Next development, enum types (`enum`) are an important tool for building type-safe systems.The enumeration of Cangjie language not only supports traditional value enumeration, but also integrates the algebraic data type characteristics of functional programming, which can flexibly model states, protocols and hierarchies.This article will analyze the core usage of enumeration types from three aspects: basic definition, instantiation method and scope rules.


## 1. Enumerate type basic definition
Enumeration types define types by listing all possible values ​​(called **Constructors**), and are suitable for scenarios such as state machines, protocol fields, color modes, etc.

### 1. Basic syntax structure
```cj
enum enum name {
| Constructor 1 | Constructor 2 | Constructor 3
}
```  
- **Keyword**: Start with `enum`, followed by an enum name (camel name, such as `RGBColor`).
- **Constructor**: The value separated by `|` in the enumeration body, the `|` before the first constructor is optional.

**Example: Define RGB color enumeration**
```cj
enum RGBColor {
| Red | Green | Blue // Three parameterless constructors represent red, green, and blue respectively
}
```  

### 2. Applicable scenarios for parameterless constructors
- **Status Identification**: For example, the network request status `enum NetworkState { | Idle | Loading | Success | Error }`.
- **Type ID**: For example, file type `enum FileType { | Text | Image | Video }`.
- **Simple enumeration value**: Scenarios where no additional data is required.


## 2. Instantiation of enum types
When creating an enumeration instance (enumeration value), it needs to be initialized through the constructor.Cangjie provides two instantiation methods to adapt to scenarios with different scopes.

### 1. Explicitly specify the type name (recommended)
Syntax: `Enum name.Constructor`
```cj
let redColor = RGBColor.Red // Use type names explicitly to avoid naming conflicts
let greenColor = RGBColor.Green
```  
** Advantages**: Clearly identify the source of enumeration, especially suitable for complex scenarios where multiple enumerations coexist.

### 2. Implicitly omit type names (used with caution)
When the constructor name is unique in the current scope, the type name can be omitted:
```cj
enum Direction { | Up | Down | Left | Right }

let moveUp = Up // equivalent to Direction.Up
let moveDown = Down // equivalent to Direction.Down
```  
**Risk**: If there is a global variable/function with the same name, a naming conflict will be triggered.

### 3. Named conflict cases and solutions
```cj
let Red = 1 // Global variable Red
func Green() { /* ... */ } // Global function Green

enum RGBColor {
| Red | Green(UInt8) | Blue(UInt8) // Enumeration constructor Red/Green
}

// The following is the error usage (compiler error)
let r1 = Red // priority match global variable Red=1
let g1 = Green(100) // Preferentially match global function Green

// Correct usage: explicitly specify the enum type name
let r2 = RGBColor.Red // Match the enumeration constructor Red
let g2 = RGBColor.Green(100) // Match enumeration constructor Green(UInt8)
```  


## 3. Scope rules and best practices
The enumeration type needs to be defined in the top-level scope of the source file and cannot be nested inside functions or structures.Its constructor scope follows the following rules:

### 1. Global visibility of top-level enumerations
```cj
// File 1: color_enum.cj
enum RGBColor {
    | Red | Green | Blue
}

// File 2: main.cj
import color_enum.RGBColor

main() {
let c = RGBColor.Red // Cross-file access enumeration constructor
}
```  

### 2. Avoid conflicts with system type naming
If the enum name conflicts with the system type (such as `String`, `Array`) or keyword, you need to add a prefix:
```cj
enum UIString { // Avoid conflicts with system type String
    | Title | Subtitle | ButtonText
}
```  

### 3. Semantic naming of enumerator constructors
- **Counterexample**: `enum Status { A | B | C }` (semantic fuzziness).
- **Positive example**: `enum OrderStatus { | Pending | Shipped | Delivered }` (clearly express the meaning of state).


## 4. The linkage between enumeration and pattern matching
Enumeration types are often combined with `match` expression to implement branch logic.The following is a matching example of an enumeration without parameters:
```cj
enum TrafficLight { | Red | Yellow | Green }

func getLightAction(light: TrafficLight) {
    match (light) {
case Red => println("Stop")
case Yellow => println("Prepare")
case Green => println("pass")
    }
}

getLightAction(light: TrafficLight.Green) // Output: Pass
```  

**Compiler Features**: If the enumeration constructor is not completely covered, a compilation error will be triggered to ensure logical integrity.


## Summarize
HarmonyOS Next's enumeration type realizes concise state modeling through parameterless constructors, and cooperates with domain rules and pattern matching, becoming the core component of type safety design.Developers need to pay attention to:
1. Preferred to instantiating enums with explicit type names to avoid naming conflicts;
2. The enumeration definition must be located in the top-level scope to ensure global visibility;
3. Combining the `match` expression to implement exhaustive branch logic to improve code robustness.
