
# HarmonyOS Next pattern nesting combination: complex data structure matching

In HarmonyOS Next development, the nesting combination ability of pattern matching is crucial in the face of nested complex data structures (such as enumeration wrapping tuples, tuple nesting enumerations, etc.).Cangjie Language supports the use of enumeration patterns, tuple patterns and other patterns in the `match` expression to achieve accurate deconstruction of multi-layer data.This article combines document knowledge points to analyze the grammar rules, application scenarios and best practices of nested patterns.


## 1. Nested Match between Tuples and Enumerations
### 1. The enumeration constructor contains tuples
When the enumerated constructor carries tuple parameters, fields can be extracted through nested tuple patterns:
```cj
enum UserInfo {
| Profile((String, Int)) // Tuple parameters: (name, age)
    | Settings(Bool)
}

let info = UserInfo.Profile(("Alice", 30))

match (info) {
case UserInfo.Profile((name, age)) => // First match the enumeration, then deconstruct the tuple
println("User:\(name), Age\(age)") // Output: User: Alice, Age 30
    case UserInfo.Settings(theme) =>
println("Theme Settings:\(theme)")
}
```  

### 2. Tuple elements are enum types
When an enumeration value is included in a tuple, it can be matched layer by layer:
```cj
let data = (status: NetworkStatus.Loading, retryCount: 3)
enum NetworkStatus { | Idle | Loading | Failed(String) }

match (data) {
case (NetworkStatus.Loading, count) => // Match the enum value and extract the second element of the tuple
println("Loading, remaining retry times: \(count)")
    case (NetworkStatus.Failed(msg), _) =>
println("Reason for failure: \(msg)")
    case _ => ()
}
```  


## 2. Destruction of multi-layer enumeration nesting
### 1. Pattern matching of recursive enumerations
Recursive enumeration is often used to build tree-like structures, and recursive hierarchies need to be processed through nested patterns:
```cj
enum FileSystem {
    | File(String)
| Directory(String, Array<FileSystem>) // Directory contains subfiles/directories
}

let root = Directory("root", [
    File("file1.txt"),
    Directory("subdir", [File("file2.txt")])
])

func traverse(file: FileSystem, depth: Int = 0) {
    match (file) {
        case File(name) =>
            println(" ".repeat(depth) + "- \(name)")
        case Directory(name, children) =>
            println(" ".repeat(depth) + "+ \(name)")
            for child in children {
traverse(file: child, depth: depth + 1) // Recursively traverse child nodes
            }
    }
}

traverse(file: root)
/* Output:
+ root
  - file1.txt
  + subdir
    - file2.txt
*/
```  

### 2. Enumeration nested enum matching
When the enumeration constructor refers to other enum types, a layer by layer match is required:
```cj
enum Protocol {
    | HTTP(Method, String)
    | FTP(Mode)
}
enum Method { | GET | POST }
enum Mode { | Active | Passive }

let request = Protocol.HTTP(GET, "/api/data")

match (request) {
case HTTP(GET, path) => // Directly match nested enumeration Method
println("GET request path:\(path)")
    case HTTP(POST, path) =>
println("POST request path: \(path)")
    case FTP(mode) =>
println("FTP mode:\(mode)")
}
```  


## 3. Complex combination of mixed modes
### 1. Mix type mode and enumeration mode
When matching `Any` type data, combine the type pattern and the enumeration pattern to determine the data type:
```cj
let value: Any = Directory("docs", [File("readme.md")])

match (value) {
case file: FileSystem => // First determine whether it is FileSystem in the type mode
traverse(file: file) // Call recursive function to traverse
case _ => println("non-file system type")
}
```  

### 2. Nested mode with conditions
Add extra conditions to nested patterns via the `where` clause:
```cj
enum MathExpr {
    | Number(Double)
    | Operation(String, MathExpr, MathExpr)
}

let expr = Operation("+", Number(3.14), Number(2.71))

match (expr) {
case Operation("+", left, right) where let sum = left + right => // Nested mode + conditional calculation
println("Addition result: \(sum)") // Output: 5.85
    case Operation("-", left, right) =>
println("Subtraction result: \(left - right)")
    case Number(n) =>
println("Value:\(n)")
}
```  


## 4. Common traps and best practices
### 1. Avoid over-necking and degrading readability
When the nesting level exceeds three layers, it is recommended to disassemble it into a standalone function or type:
```cj
// Counterexample: Three-layer nesting is difficult to maintain
match (nestedEnum) {
    case A(B(C(D(value)))) => println(value)
}

// Positive example: step by step deconstruction
if let A(b) <- nestedEnum, let B(c) <- b, let C(d) <- c, let D(value) <- d {
    println(value)
}
```  

### 2. Preferential matching of specific patterns
Place more specific nested patterns on top of the matching branches to avoid logic being overwritten by common patterns:
```cj
enum Shape {
    | Circle(radius: Double)
    | Rectangle(width: Double, height: Double)
| Square(size: Double) // Square is a special case of Rectangle
}

let shape = Square(size: 5.0)

match (shape) {
case Square(size) => println("Square area: \(size * size)") // Preferential match for Square
case Rectangle(width, height) => println("Rectangle area:\(width * height)")
case Circle(radius) => println("Circle area:\(3.14 * radius * radius)")
}
```  

### 3. Ignore irrelevant fields using wildcards
In nested mode, if certain fields are not processed, the wildcard `_` can be ignored:
```cj
let log = (level: "ERROR", message: "UnexpectedEOF", location: (line: 10, column: 5))

match (log) {
case ("ERROR", msg, (line, _)) => // Ignore the column field
println("Error line\(line):\(msg)")
    case _ => ()
}
```  


## Summarize
Pattern nesting combination is the core technology of HarmonyOS Next to process complex data structures. Through multi-layer deconstruction of enumeration, tuples, and type patterns, data hierarchical relationships can be clearly expressed.Developers need to master:
1. Enumerations and nested matching orders of tuples;
2. Termination conditions and recursive traversal logic of recursive enumeration;
3. Coordination between conditional judgment and field extraction in mixed mode.
