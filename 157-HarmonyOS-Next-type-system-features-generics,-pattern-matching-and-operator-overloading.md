
# HarmonyOS Next type system features: generics, pattern matching and operator overloading

In HarmonyOS Next development, the type system is the core to ensure code robustness and maintainability.Cangjie Language realizes type abstraction and flexible expansion through features such as **Generics**, **Pattern Matching** and ** operator overloading**.This article will combine practical cases to analyze how these features can improve code reusability, security and readability.


## 1. Generic system: Type abstraction and code reuse
Generics allow the use of parameterized types to define functions, classes, and structures to implement logic independent of specific types and avoid repeated encoding.

### 1. Generic class: type-independent implementation of stack structure
```cj
class Stack<T> {
    private var elements: Array<T> = []

    func push(_ element: T) { elements.append(element) }
    func pop() -> T? { return elements.popLast() }
}

// Use Int type stack
let intStack = Stack<Int>()
intStack.push(10)
let top = intStack.pop() // top is Optional<Int>

// Use String type stack
let strStack = Stack<String>()
strStack.push("HarmonyOS")
```  

### 2. Type constraints: limit parameter types through the `where` clause
Ensure that generic types have specific capabilities (such as comparable, hashable) through protocol constraints.
```cj
func findMin<T: Comparable>(_ array: Array<T>) -> T? {
    guard !array.isEmpty else { return nil }
    return array.reduce { $0 < $1 ? $0 : $1 }
}

let numbers = [5, 3, 8, 2]
let minNum = findMin(numbers) // Correct: Int follows the Comparable protocol
// let strings = ["apple", "banana"] // Error: String not specified to follow Comparable (need to be explicitly declared)
```  

### 3. Type erasure and performance optimization
Generics will perform type erasing during the compilation period to generate optimized code for specific types.For example:
```cj
func testErasure() {
    let intList = Array<Int>()
    let strList = Array<String>()
print(type(of: intList)) // Output: Array<Int> (Type information is still retained at runtime)
}
```  


## 2. Pattern matching: flexible conditional judgment and type destruction
Pattern matching is implemented through the `when` expression, supporting enumeration value matching, type checking, deconstruction and assignment scenarios, and the code structure is simpler.

### 1. Enumeration value matching: State machine logic simplification
```cj
enum NetworkStatus {
    case connected, disconnected, loading
}

func handleStatus(_ status: NetworkStatus) {
    when (status) {
        case.connected:
println("Connected, data transfer allowed")
        case.disconnected:
println("Disconnect, try connection")
        case.loading:
println("Data loading, please wait")
    }
}

handleStatus(.loading) // Output: Data is loading, please wait
```  

### 2. Type Guard and Intelligent Conversion
Type checking and safe conversion are implemented through `is` and `as`, and the compiler automatically narrows the type range.
```cj
func printValue(_ value: Any) {
    when (value) {
        is Int:
let num = value as! Int // No forced unpacking is required, the compiler is known as Int
println("Integer:\(num)")
        is String:
println("String:\(value as! String)")
        else:
println("Unknown Type")
    }
}

printValue(42) // Output: integer: 42
printValue("Hello") // Output: String: Hello
```  

### 3. Tuple Deconstruction: Multi-value Pattern Matching
```cj
let point = (x: 10, y: 20)
when (point) {
    (x: 0, y: 0):
println("origin")
    (x: let a, y: let b) where a == b:
println("Diagonal point: \(a), \(b)")
(x: let a, y: _): // Ignore the y value
println("x coordinate:\(a)")
}
```  


## 3. Operator overloading: Custom type behavior extension
Operator overloading allows the behavior of defining standard operators (such as `+`, `*`) for custom types to improve code readability.

### 1. Numeric type operator: vector addition and number multiplication
```cj
struct Vector2D {
    var x: Float64, y: Float64
}

// Overload + operator implements vector addition
func +(lhs: Vector2D, rhs: Vector2D) -> Vector2D {
    return Vector2D(x: lhs.x + rhs.x, y: lhs.y + rhs.y)
}

// Overload the * operator to implement number multiplication
func *(lhs: Vector2D, scalar: Float64) -> Vector2D {
    return Vector2D(x: lhs.x * scalar, y: lhs.y * scalar)
}

let v1 = Vector2D(x: 1, y: 2)
let v2 = Vector2D(x: 3, y: 4)
let sum = v1 + v2          // (4, 6)
let scaled = v1 * 2.0      // (2, 4)
```  

### 2. Comparison operator: Custom sorting rules
```cj
struct Person {
    var age: Int, name: String
}

// Overload < operators implement sorting by age
func <(lhs: Person, rhs: Person) -> Bool {
    return lhs.age < rhs.age
}

let people = [Person(age: 25, name: "Alice"), Person(age: 30, name: "Bob")]
let sorted = people.sorted() // Sort by ascending order of age
```  

### 3. Compound operator: chain call optimization
```cj
struct StringBuilder {
    var content: String = ""
}

// Overload += operator to implement string stitching
func +=(lhs: inout StringBuilder, rhs: String) {
    lhs.content.append(rhs)
}

var builder = StringBuilder()
builder += "Hello, " += "HarmonyOS!"
println(builder.content) // Output: Hello, HarmonyOS!
```  


## 4. Mixed scenarios: collaborative application of type system characteristics
### 1. Generic + Pattern Matching: Collection Element Type Check
```cj
func processCollection<T>(_ collection: Array<T>) {
    for element in collection {
        when (element) {
            is Comparable:
println("Comparable Type:\(element)")
            is Hashable:
println("hashable type: \(element)")
            else:
println("Basic Type:\(element)")
        }
    }
}

processCollection([1, 2, 3]) // Output: Comparable type, hashable type
processCollection(["a", "b"]) // Same as above
processCollection([Vector2D(x: 1, y: 2)]) // Output: Basic type (requires manual implementation of the protocol)
```  

### 2. Operator overload + generics: matrix operation library design
```cj
struct Matrix<T: Numeric> {
    var rows: Int, columns: Int, data: Array<T>
}

// Overload the * operator to implement matrix multiplication
func *(lhs: Matrix<T>, rhs: Matrix<T>) -> Matrix<T> where T: Numeric {
// Dimensional checking and multiplication logic
    return Matrix<T>(rows: lhs.rows, columns: rhs.columns, data: [])
}

let intMatrix = Matrix<Int>(rows: 2, columns: 2, data: [1, 2, 3, 4])
let result = intMatrix * intMatrix // Call generic operators
```  


## Summarize
HarmonyOS Next's type system achieves the balance between "type safety" and "code reuse" through **generic abstraction**, **pattern matching flexibility** and ** operator customization:
- Generics are suitable for general implementations of data structures and algorithms;
- Pattern matching simplifies complex conditional logic and improves code readability;
- Operator overload allows custom types to be seamlessly integrated into the standard syntax system.
