
# HarmonyOS Next Enumeration Recursive Definition and Expression Tree Modeling: From Theory to Practice

In HarmonyOS Next development, the recursive definition of enumeration is the core technology for building complex data structures.By allowing the enumeration constructor to refer to its own type, developers can easily model recursive data models such as expression trees and tree structures.This article combines the characteristics of Cangjie language to analyze the definition rules, pattern matching techniques and practical applications in expression evaluation.


## 1. Basic definition and rules of recursive enumeration
Recursive enumeration refers to the enum's constructor parameters that contain the enum's own type.This feature enables enumerations to represent data with hierarchical structures, such as mathematical expressions, file system directories, etc.

### 1. Basic syntax structure
```cj
enum enum name {
| Basic constructor (non-enumer type parameter)
| Recursive constructor (enumeration name, enumeration name) // The parameter is the enumerated type
}
```  

### 2. Expression tree example
Taking mathematical expressions as an example, define a recursive enum containing numerical values, additions and subtractions:
```cj
enum Expr {
| Num(Int64) // Basic constructor: numerical
| Add(Expr, Expr) // Recursive constructor: Addition expression (left operand, right operand)
| Sub(Expr, Expr) // Recursive constructor: subtraction expression (left operand, right operand)
}
```  
- **`Num(Int64)`**: Represents a single numerical value (such as `5`).
- **Add(Expr, Expr)`**: Represents additive expressions (such as `Add(Num(3), Num(4))` represents `3 + 4`).
- **`Sub(Expr, Expr)`**: represents subtraction expressions (such as `Sub(Num(10), Add(Num(2), Num(3))` means `10 - (2 + 3)`).

### 3. Compiler Limitations
Recursive enumerations need to ensure that the constructor contains at least one non-recursive constructor (base constructor) to avoid infinite recursion.The Cangjie compiler will automatically check the validity of recursive enumerations. If all constructors are recursive types, a compilation error will be triggered.


## 2. Pattern matching and traversal of recursive enumeration
### 1. Recursive pattern matching logic
When processing recursive enumerations through the `match` expression, the processing logic needs to be defined separately for the basic constructor and the recursive constructor.The basic constructor acts as a recursive termination condition, while the recursive constructor is responsible for handling the hierarchy.

**Example: Calculate expression value**
```cj
func evaluate(expr: Expr): Int64 {
    match (expr) {
case Num(n) => n // Basic constructor: directly return the numeric value
case Add(lhs, rhs) => evaluate(lhs) + evaluate(rhs) // Recursively process left and right operands
case Sub(lhs, rhs) => evaluate(lhs) - evaluate(rhs) // Recursively process left and right operands
    }
}
```  

### 2. Expression tree construction example
```cj
// Build expression: 10 - (3 + 2)
let expr = Sub(
    Num(10),
    Add(Num(3), Num(2))
)

let result = evaluate(expr: expr) // The calculation result is 5
println("Expression result: \(result)") // Output: 5
```  

### 3. Tips for traversing recursive enumerations
For more complex recursive structures (such as expressions containing multi-layer nested), traversal can be achieved through ** pattern matching combined with loops** or ** tail recursive optimization:
```cj
// Tail recursive optimization version evaluation function
func evaluateTailRecursive(expr: Expr, acc: Int64 = 0): Int64 {
    while true {
        match (expr) {
            case Num(n) => return acc + n
            case Add(lhs, rhs) => expr = lhs; acc += evaluateTailRecursive(rhs, 0)
            case Sub(lhs, rhs) => expr = lhs; acc -= evaluateTailRecursive(rhs, 0)
        }
    }
}
```  


## 3. Practical scenario: file system directory modeling
Recursive enumerations are not only suitable for mathematical expressions, but also for modeling directory structures in file systems, where directories can contain subdirectories and files.

### 1. Recursive enum definition
```cj
enum FileSystemItem {
| File(name: String, size: Int64) // File: Name, Size
| Directory(name: String, items: [FileSystemItem]) // Directory: Name, subitem list
}
```  

### 2. Example of building directory structure
```cj
// Create a file system structure:
// root/
// ├─ file1.txt (1024B)
// └─ subdir/
//    └─ file2.txt (512B)
let file1 = File(name: "file1.txt", size: 1024)
let file2 = File(name: "file2.txt", size: 512)
let subdir = Directory(name: "subdir", items: [file2])
let root = Directory(name: "root", items: [file1, subdir])
```  

### 3. Recursively calculate the total directory size
```cj
func calculateSize(item: FileSystemItem): Int64 {
    match (item) {
case File(_, size) => size // The file returns the size directly
case Directory(_, items) => items.map(calculateSize).reduce(0, +) // Recursively calculate the sum of the child's sizes
    }
}

let totalSize = calculateSize(item: root) // The calculation result is 1536 (1024 + 512)
println("Total directory size: \(totalSize)B")
```  


## 4. Performance considerations and optimization of recursive enumeration
### 1. Stack Overflow Risk
If the depth of the recursive enumeration exceeds the system stack limit, it will cause a runtime stack overflow error.For example, an expression tree with a depth of 1000 may trigger a stack overflow.

### 2. Optimization strategy
#### (1) Iterative substitution recursion
By manually maintaining the stack structure, convert recursive traversal into iterative traversal:
```cj
func evaluateIterative(expr: Expr): Int64 {
    var stack = [expr]
    var result = 0

    while !stack.isEmpty {
        let current = stack.pop()!
        match (current) {
            case Num(n) => result += n
            case Add(lhs, rhs) => stack.append(rhs); stack.append(lhs)
case Sub(lhs, rhs) => stack.append(rhs); stack.append(Expr.Sub(lhs, Num(0))) // Adjust symbols
        }
    }

    return result
}
```  

#### (2) Tail recursive optimization
If the compiler supports tail recursive optimization, the recursive function can be rewritten into tail recursive form to avoid increasing stack depth:
```cj
@tailrec
func evaluateTailRecursive(expr: Expr, acc: Int64 = 0): Int64 {
    match (expr) {
        case Num(n) => acc + n
        case Add(lhs, rhs) => evaluateTailRecursive(lhs, acc + evaluateTailRecursive(rhs))
        case Sub(lhs, rhs) => evaluateTailRecursive(lhs, acc - evaluateTailRecursive(rhs))
    }
}
```  

### 3. Compiler optimization support
The Cangjie compiler optimizes the tail recursive function and converts it into an iterative form to avoid stack overflow.Developers can explicitly mark tail recursive functions through `@tailrec` annotation (requires compiler support).


## 5. Summary
Recursive enumeration is a powerful tool for processing hierarchical data in HarmonyOS Next, and its core advantages are:
1. **Simple data modeling**: Easily define complex models such as expression trees and directory structures through recursive references of enumerated constructors;
2. **Type-safe traversal**: Combined with pattern matching, ensure that all possible enumeration constructors are processed during the compilation period;
3. **Flexible optimization strategy**: Balance code simplicity and performance requirements through iterative or tail recursive optimization.
