
# Refutability of HarmonyOS Next mode: refutable and unrefutable modes

In HarmonyOS Next development, understanding the **Refutability of patterns is the key to mastering type safety matching.Cangjie language divides patterns into **Refutable Pattern** and **Irrefutable Pattern**. The essential difference between the two lies in whether it is possible to match failure.This article combines document knowledge points to analyze the definitions, application scenarios and compiler behaviors of the two types of patterns.


## 1. Refutation mode: risk mode that may match failure
**Refutable mode**In some cases, the value to be matched may not be matched, and logical processing is required to avoid runtime errors.This type of pattern requires developers to explicitly handle matching failures.

### 1. Common types of refutation patterns
| Pattern type | Example | Match failure scenario |
|----------------|-------------------------------|---------------------------------------|  
| Constant mode | `case 1` | Failed if the value to be matched is not 1 |
| Type pattern | `case a: Dog` | Failed to match an instance of a non-Dog type |
| Partial Enumeration Pattern | `case Add(n)` (the enumeration has multiple constructors) | Failed when the value to be matched is another constructor (such as Sub) |
| Tuple pattern | `case (1, 2)` | Failed if the value or quantity of tuple element does not match |

### 2. Processing requirements for matching failures
When using rebutable mode in the `match` expression, you must ensure that all possible situations are overwritten, otherwise the compiler will report an error.
```cj
enum Command { | A | B(Int) }

func process(cmd: Command) {
    match (cmd) {
case A => println("process A")
case B(n) => println("process B, parameter: \(n)")
// No additional processing is required, since the enumeration has only two constructors, it has been completely covered
    }
}

// Counterexample: Refutable mode that does not cover all constructors
enum Color { | Red | Green | Blue }
func printColor(c: Color) {
    match (c) {
case Red => println("red") // Missing Green and Blue branches, compile errors
    }
}
```  

### 3. Combined with `if-let` to process refutation mode
For possible failed matches (such as parsing Option type), you can handle them in advance via `if-let`:
```cj
let maybeNum: Option<Int> = None
if (let Some(n) <- maybeNum) { // Some(n) is a refutation mode, fails when matching None
println("Value:\(n)")
} else {
println("valueless") // Explicit processing failure scenario
}
```  


## 2. Unrefutable mode: a safe mode that must be successful
**Unrefutable mode**There must be successful under the premise of type matching, and there is no need for additional processing of failures. It is suitable for variable definitions, `for-in` loops and other scenarios.

### 1. Common types of non-refutable patterns
| Pattern type | Example | Reasons for a must-match |
|----------------|-------------------------------|---------------------------------|  
| Wildcard pattern | `case _` | Match any value |
| Bind Mode | `case x` | Capture any value and bind to a variable |
| Single constructor enumeration | `case A(n)` (Enum only has A constructor) | Enum value can only be A constructor |
| Full element tuple pattern | `case (x, y)` | The number of tuple elements is fixed and the pattern is unlimited |

### 2. Application in variable definition
The non-refutable mode allows direct use of variable deconstruction without conditional judgment:
```cj
// Tuple deconstruction (not refuted pattern)
let (x, y) = (10, 20) // It must be successful, x=10, y=20

// Enumeration deconstruction (single constructor, unrefutable)
enum UnitEnum { | Value(Int) }
let Value(n) = UnitEnum.Value(5) // Get n=5 directly
```  

### 3. Safe traversal in `for-in` loop
The `for-in` loop requires that the mode is irrefutable to ensure that the loop is executed normally:
```cj
let list = [1, 2, 3]
for (n in list) { // The binding pattern n is irrefutable, matching each element
    println(n)
}

// Enumerate collection traversal (single constructor)
enum SingleEnum { | Item(String) }
let items = [SingleEnum.Item("a"), SingleEnum.Item("b")]
for (Item(s) in items) { // Non-refutable mode, directly obtain s
    println(s)
}
```  


## 3. Compiler behavior of pattern classification
The Cangjie compiler judges the integrity of the matching logic through the refutation of the pattern. The core rules are as follows:

### 1. Mandatory coverage requirements for refutation modes
- If the `match` expression uses a refutation mode and does not cover all possible situations, the compiler reports an error.
- **Example**: Enumeration mode does not cover all constructors
  ```cj
  enum E { | A | B | C }
  func f(e: E) {
      match (e) {
case A => () // Missing B and C branches, compile error: "Non-exhaustive patterns"
      }
  }
  ```  

### 2. Loose check of non-refutable mode
- The non-refutable pattern does not need to cover all cases, as it must match.
- **Example**: Wildcard pattern as unique branch
  ```cj
  func g(x: Int) {
      match (x) {
case _ => () // Non-refutable mode, no other branches are needed
      }
  }
  ```  

### 3. Matching order of mixed patterns
When refutable and non-refutable mode coexist, refutable mode needs to be placed ahead:
```cj
enum Mix { | A(Int) | B }
func h(m: Mix) {
    match (m) {
case A(n) => println(n) // Refute the pattern, first match the specific situation
case _ => println("Other") // Unrefutable mode guarantees
    }
}
```  


## 4. Practical scenario: Correct application of pattern refutation
### 1. Safe parsing nullable values ​​(refutable mode)
```cj
let optionalStr: ?String = "Hello"
match (optionalStr) {
case Some(s) => println("value: \(s)") // Some(s) is a refutation pattern, fails when matching None
case None => println("No string") // Explicit processing failure
}
```  

### 2. Forced deconstruction of non-null values ​​(not refuted mode)
```cj
let nonOptional = "World"
let Some(s) = nonOptional // is equivalent to let s = nonOptional, irrefutable
println(s) // Output: "World"
```  

### 3. Safe traversal of recursive enumerations (not refuted mode)
```cj
enum List {
| Nil // Basic case, irrefutable
| Cons(Int, List) // Recursive case, refute
}

func traverse(list: List) {
    match (list) {
case Nil => println("empty list") // Non-refutable mode, terminate recursion
case Cons(n, rest) => { // Refuted mode, need to ensure recursive termination
            println(n)
            traverse(list: rest)
        }
    }
}

traverse(list: Cons(1, Cons(2, Nil))) // Output: 1 2
```  


## Summarize
The refutation of the pattern is an important guarantee for HarmonyOS Next type safety:
- **Refutation mode**The matching failure needs to be explicitly handled, suitable for enumeration of multiple constructors, type checking and other scenarios;
- **No refutation mode** Ensures safe deconstruction and is suitable for unconditional scenarios such as variable definition and loop traversal.
