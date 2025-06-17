
# HarmonyOS Next Advanced Tips for Pattern Matching in Deconstruction: Nesting, Combination and Pattern Guard

In HarmonyOS Next development, the power of pattern matching is not only the matching of basic values, but also its hierarchical deconstruction ability of complex data structures.Through nested modes, combined modes and Pattern Guard, developers can efficiently process multi-level data and achieve accurate conditional filtering.This article is based on Cangjie language document, advanced techniques for analyzing pattern matching and its application in actual scenarios.


## 1. Nesting mode: Hierarchical destruction of multi-layer data structures
Nested mode allows other modes to be included in the schema, suitable for parsing nested enums, tuples, or object data.

### 1. Destruction of enum nested enums
```cj
enum Outer {
    | Inner(InnerEnum)
}
enum InnerEnum {
    | Value(String)
    | Number(Int)
}

let data = Outer.Inner(InnerEnum.Value("hello"))

match (data) {
case Outer.Inner(InnerEnum.Value(str)) => // Double-layer enum nested matching
println("Internal string: \(str)") // Output: hello
    case Outer.Inner(InnerEnum.Number(n)) =>
println("Internal number: \(n)")
}
```  

### 2. Destruction of tuple nested enumerations
```cj
let nestedTuple = (1, Outer.Inner(InnerEnum.Number(42)))

match (nestedTuple) {
case (index, Outer.Inner(InnerEnum.Number(n))) => // Tuple + Enumeration nesting
println("Number at index \(index): \(n)") // Output: Number at index 1: 42
    default => ()
}
```  

### 3. The execution order of nested patterns
The nested pattern matches layer by layer from outside to inside, and if the outer layer fails, the entire branch will be skipped directly:
```cj
let value = ("error", 404)

match (value) {
case ("success", code) => println("Success code: \(code)") // The outer string does not match, just skip it
case ("error", code) where code >= 400 => println("Error code: \(code)") // Match successfully
}
```  


## 2. Combination mode: logical or with pattern collection
Connect multiple patterns through `|` to achieve "logical or" matching, suitable for scenarios where similar processing logic is merged.

### 1. Enumeration constructor combination matching
```cj
enum Action {
    | Click | DoubleClick | LongPress(Int)
}

func handleAction(action: Action) {
    match (action) {
case Click | DoubleClick => // Combination matching click class operation
println("handle click event")
        case LongPress(duration) =>
println("Long press\(duration) milliseconds")
    }
}
```  

### 2. Combination of numerical ranges and constants
```cj
let number = 15

match (number) {
case 0 | 1 | 2 => println("small number")
case 3..10 | 15 => // Combining match ranges with single values
println("medium number or 15") // Output: medium number or 15
case _ => println("big number")
}
```  

### 3. Limitations of combination modes
- Disable the definition of bound variables with the same name in combination mode:
  ```cj
// Counterexample: Repeat variable name n
case Add(n) | Sub(n) => println("operand: \(n)") // Compile error
  ```  
- The patterns in the combined mode must belong to the same type category (such as both are enumeration constructors or are numerical values).


## 3. Pattern Guard: Enhancement of Conditional Filtering
Pattern Guard adds additional conditions to the pattern through the `where` clause to achieve finer matching logic.

### 1. Basic syntax structure
```cj
match (value) {
case pattern where conditional expression => processing logic
}
```  

### 2. Conditional filtering of enumeration parameters
```cj
enum Temperature {
    | Celsius(Float) | Fahrenheit(Float)
}

let temp = Celsius(38.5)

match (temp) {
case Celsius(c) where c > 37.5 => // Match high temperature scenes
println("Abnormal body temperature:\(c)℃") // Output:Abnormal body temperature: 38.5℃
    case Celsius(c) =>
println("Normal body temperature:\(c)℃")
    case Fahrenheit(f) where f > 100 =>
println("High temperature:\(f)℉")
}
```  

### 3. Complex conditions combined with binding mode
```cj
let point = (x: 5, y: 5)

match (point) {
case (x, y) where x == y && x > 0 => // Use the binding variable x/y to participate in the conditional judgment
println("First quadrant diagonal point: (\(x), \(y))") // Output: First quadrant diagonal point: (5, 5)
    case (x, y) where x < 0 && y < 0 =>
println("third quadrant point")
    default => ()
}
```  

### 4. Combining mode guard and type mode
```cj
class Person {
    let age: Int
    init(age: Int) { self.age = age }
}

let person = Person(age: 25)

match (person) {
case p: Person where p.age >= 18 => // Type mode + age condition
println("adult")
    case p: Person =>
println("Minor")
}
```  


## 4. Practical scenario: Accurate analysis of protocol data
### Scenario: parse custom communication protocols
Protocol format: [Type Identification] [Length] [Data Content]`, where the type Identification is `0x01` (text) or `0x02` (value).

### 1. Enumeration definition matches pattern
```cj
enum ProtocolData {
    | Text(String)
    | Number(Int)
}

func parsePacket(bytes: [UInt8]) -> ProtocolData? {
    guard bytes.count >= 3 else { return None }

    match (bytes[0], bytes[1..3]) {
case (0x01, lengthBytes) where let length = bytesToInt(lengthBytes) => // Mode guard calculates length
            let dataBytes = bytes[3..3+length]
            return .Text(utf8ToString(dataBytes))
        case (0x02, lengthBytes) where let length = bytesToInt(lengthBytes) =>
            let dataBytes = bytes[3..3+length]
            return .Number(bytesToInt(dataBytes))
        default => return None
    }
}
```  

### 2. The key role of pattern guard
- Verify the validity of the length field (such as `length > 0`);
- Handling possible parsing through guards fails when converting a byte array to a numeric value or string.


## 5. Precautions and best practices
### 1. Avoid overly complex patterns
- When the pattern is nested more than three layers or the conditions are too complex, split into independent functions or types;
- Priority is given to using named parameters and clear indentation to improve readability.

### 2. The importance of pattern order
- Put specific patterns (such as enumeration constructors with conditions) before general mode;
- The combination mode and guarding conditions should be arranged from strict to loose.

### 3. Optimize with compiler prompts
The Cangjie compiler will prompt unused binding variables or unreachable pattern branches, which can simplify the code:
```cj
match (value) {
case (x, y) where x == y => println("equal") // If x/y is not used, the compiler prompts to delete the binding
    default => ()
}
```  


## Summarize
Advanced techniques for pattern matching (nesting, combinatorial, pattern guard) enable HarmonyOS Next developers to efficiently process complex data structures and implement precise conditional logic:
- **Nested pattern** is used to deconstruct multi-layer data, such as enum nesting or tuple nesting;
- **Combination mode**Combination similar processing logic to reduce redundant branches;
- **Mode Guard** Add extra conditions to achieve fine-grained matching control.
