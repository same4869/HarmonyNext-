
# HarmonyOS Next Enumeration and Pattern Matching Best Practices: A Clean Code Way

In HarmonyOS Next development, the rational use of enum types (`enum`) and pattern matching (`match`) is the key to writing neat and robust code.By following algebraic data types design principles and best practices for pattern matching, code readability, maintainability and type safety can be significantly improved.This article combines document knowledge points to summarize the core best practices of enumeration and pattern matching.


## 1. The single responsibility principle of enumeration design
### 1. Avoid mixing irrelevant states
Each enum should focus on a single concept or business scenario to avoid carrying too many irrelevant states.
**Counterexample** (overmix):
```cj
enum DataStore {
| File(String) // File storage
| Database(Int) // Database Storage (ID)
| Network(String) // Network address
| Cache(Bool) // Cache status (whether it is enabled)
}
```  

**Positive example** (Split independent enumeration):
```cj
enum StorageType { | File(String) | Database(Int) }
enum NetworkType { | Address(String) }
enum CacheState { | Enabled | Disabled }
```  

### 2. Semantic naming of constructor parameters
Add named tags to parameters of parameter constructors to improve code self-interpretation.
```cj
enum coordinates {
|Two-dimensional (x: Double, y: Double)
|Three-dimensional (x: Double, y: Double, z: Double)
}

let point = coordinates.2D (x: 3.0, y: 4.0) // Clear the meaning of the parameters
```  


## 2. Clear hierarchical strategy for pattern matching
### 1. Sort branches by matching frequency
Place the high-frequency state or specific conditions on the top of the matching branch to reduce unnecessary judgment overhead.
```cj
enum UserAction {
    | Click | DoubleClick | LongPress(Int)
}

func handleAction(action: UserAction) {
    match (action) {
case .Click => handleClick() // High frequency operation is preferred
        case .DoubleClick => handleDoubleClick()
        case .LongPress(duration) => handleLongPress(duration)
    }
}
```  

### 2. Use wildcards to handle default situations
In enumeration matching, always use the wildcard `_` to overwrite the unexpected state to avoid runtime errors.
```cj
enum HttpMethod { | GET | POST | PUT | DELETE }

func handleMethod(method: HttpMethod) {
    match (method) {
        case .GET => fetchData()
        case .POST => submitData()
        case .PUT => updateData()
case _ => error("Unsupported request method") // Provide a guarantee to handle possible new methods in the future
    }
}
```  

### 3. Avoid nested matching and disassemble complex logic
Nested matches over two layers should be split into independent functions, keeping each `match` branch concise.
**Counterexample** (Deep nesting):
```cj
enum JsonValue { | Object(Array<JsonValue>) | Array(Array<JsonValue>) | String(String) }

func parseJson(value: JsonValue) {
    match (value) {
        case .Object(items) =>
            for item in items {
                match (item) {
                    case .String(s) => processString(s)
                    case .Array(arr) =>
                        for elem in arr {
match (elem) { /* third layer match */ }
                        }
                }
            }
    }
}
```  

**Positive example** (disassembly function):
```cj
func parseObject(items: Array<JsonValue>) {
    items.forEach(parseItem)
}

func parseItem(item: JsonValue) {
    match (item) {
        case .String(s) => processString(s)
        case .Array(arr) => parseArray(arr)
// Other situations
    }
}

func parseArray(arr: Array<JsonValue>) {
    arr.forEach(parseItem)
}
```  


## 3. Type-safe error handling mechanism
### 1. Replace magic values ​​and boolean flags with enums
Avoid using fuzzy types such as `Int` or `Bool` by explicitly defining state or error types by enumeration.
**Counterexample**(magic value):
```cj
let status = 2 // 0=success, 1=failure, 2=processing (the meaning is unclear)
```  

**Positive example** (enumeration substitution):
```cj
enum OperationStatus { | Success | Failed | InProgress }
let status = OperationStatus.InProgress
```  

### 2. Combined with the Result type processing can fail
Use `Result<T, E>` to encapsulate possible failure operations, and process successful and error paths through pattern matching.
```cj
enum FileError { | NotFound | PermissionDenied }

func readFile(path: String) -> Result<String, FileError> {
    if !fileExists(path) {
        return .Err(.NotFound)
    } else if !canRead(path) {
        return .Err(.PermissionDenied)
    } else {
        return .Ok(readFileContent(path))
    }
}

// The result of the call
match (readFile("/config.txt")) {
    case .Ok(content) => processContent(content)
    case .Err(error) => showError(error)
}
```  


## 4. Performance optimization of enumeration and pattern matching
### 1. No parameters enumeration takes precedence over parameter enumeration
The parameterless enumeration has a smaller memory footprint (only 1 byte), suitable for pure state identification scenarios.
```cj
enum ConnectionMode { | Wifi | Bluetooth | Usb } // No parameters enum, efficient and lightweight
```  

### 2. Use the compiler's exhaustive check
Relying on the compiler to force overwrite all enumerators to avoid logical vulnerabilities.
```cj
enum Color { | Red | Green | Blue }

func printColorName(color: Color) {
    match (color) {
case .Red => print("red")
case .Green => print("green")
// Compilation error: Unhandled.Blue, force developer to supplement logic
    }
}
```  

### 3. Avoid using binding mode in `|`
`|`The definition of variables with the same name is prohibited in the connection mode to prevent ambiguity and compilation errors.
```cj
enum Command { | Add(Int) | Sub(Int) }

func processCommand(cmd: Command) {
    match (cmd) {
// Counterexample: Repeat variable name n
// case Add(n) | Sub(n) => println("operand: \(n)")
        
// Affirmative example: Use wildcards or tear down branches
case Add(n) => println("Add number: \(n)")
case Sub(n) => println("Subtraction:\(n)")
    }
}
```  


## 5. Practical combat: a comprehensive case of clean code
### Scenario: User permission system
#### 1. Enumeration definition (single responsibility)
```cj
// Permission type enumeration
enum Permission {
    | Read | Write | Delete | Admin
}

// Enumeration of permission check results
enum PermissionResult {
    | Granted(Permission)
    | Denied(Permission, Reason)
}

// Reject reasons enumeration
enum Reason { | NoRole | Expired | ManualBlock }
```  

#### 2. Pattern matching logic (clear layering)
```cj
func handlePermissionResult(result: PermissionResult) {
    match (result) {
        case .Granted(permission) =>
println("Authorized:\(permission)")
            executeAction(permission)
        
        case .Denied(permission, reason) =>
println("Permission Denied: \(permission) - Reason: \(reason)")
match (reason) { // Second layer matching, logical concentration
                case .NoRole => promptAssignRole(permission)
                case .Expired => showRenewalPrompt()
                case .ManualBlock => contactAdmin()
            }
    }
}
```  

#### 3. Type-safe extension (adapting to the standard library)
```cj
// Convert PermissionResult to Result type
func toResult(result: PermissionResult) -> Result<Permission, (Permission, Reason)> {
    match (result) {
        case .Granted(p) => .Ok(p)
        case .Denied(p, r) => .Err((p, r))
    }
}
```  


## Summarize
The best practices for enumeration and pattern matching in HarmonyOS Next can be summarized as:
1. **Enum design**: Follow a single responsibility, constructor parameters are semantic, and the use of parameterless enumeration is preferred;
2. **Pattern matching**: Sort branches by frequency, avoid nesting, and force exhaustive checks;
3. **Error handling**: Use enumerations to replace fuzzy types, and combine `Result` to achieve type-safe failure handling;
4. **Performance and readability**: Use compiler optimization to keep the matching logic concise and disassemble complex scenarios.
