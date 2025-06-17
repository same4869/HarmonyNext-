
# HarmonyOS Next Pattern Matching Basics: Constant Pattern and Wildcard Pattern

In HarmonyOS Next development, pattern matching is one of the core features of Cangjie language. It realizes data deconstruction and logical branch control through flexible pattern design.This article will focus on the ** constant mode** and ** wildcard mode**, analyze its syntax rules, application scenarios and linkage logic with enumeration types, and help developers master the conditional judgment skills of type safety.


## 1. Constant mode: the cornerstone of precise value matching
The constant mode is accurately matched through literal values ​​and is suitable for conditional judgment scenarios with known fixed values.

### 1. Supported literal types
| Type | Example | Match Logic |
|--------------|-------------------------------|---------------------------|  
| integer | `case 0`, `case 100` | equal values ​​means matching |
| Floating point number | `case 3.14`, `case 0.5f16` | Exact floating point value matching |
| Character/String | `case 'A'`, `case "hello"` | Character encoding or string content equal |
| Boolean value | `case true`, `case false` | Boolean logic matching |
| Unit | `case ()` | Unique value matching |

### 2. Multi-value matching and range logic
Implement the "OR" logic by connecting multiple constant patterns:
```cj
main() {
    let score = 85
    let grade = match (score) {
case 0..50 => "D" // Range matching (left close and right open, range mode needs to be explicitly defined)
case 60 | 70 => "C" // Multi-value matching
case 80 | 90 | 100 => "A" // Multi-value accurate matching
case _ => "Invalid" // Wildcard guarantee
    }
println(grade) // Output: "Invalid" (because 85 is not in the matching range)
}
```  

### 3. Constant pattern matching of enum types
Constant mode can directly match the enumeration constructor (no-reference scenario):
```cj
enum Direction { | Up | Down | Left | Right }

func handleDirection(dir: Direction) {
    match (dir) {
case Direction.Up => println("Move up")
case Down => println("move down") // Implicit type matching, equivalent to Direction.Down
case Left | Right => println("Horizontal Move")
    }
}

handleDirection(dir: .Right) // Output: "Move horizontally"
```  


## 2. Wildcard pattern: a flexible universal matching
Wildcard pattern (`_`) is used to match arbitrary values ​​and is a key tool for achieving logical integrity.

### 1. Must-choose practice as a default branch
In enumeration matching, if all constructors are not covered, the compiler will force the addition of wildcard branches:
```cj
enum RGBColor { | Red | Green | Blue }

func printColorName(color: RGBColor) {
    match (color) {
case Red => println("red")
case Green => println("green")
// case Blue => println("blue") // This branch is deliberately omitted
case _ => println("Unknown color") // Wildcard must be added to meet exhaustive requirements
    }
}

printColorName(color: .Blue) // Output: "Unknown color"
```  

### 2. Wildcard application in variable definition
In a deconstructed scenario, wildcards can ignore irrelevant data:
```cj
let (x, _) = (10, 20) // Get only x=10, ignore the second value
println(x) // Output: 10

for (_ in 1..5) { // Ignore the loop index and execute only the loop body
println("Iteration")
}
```  

### 3. Mixed with other modes
Wildcards can be used as part of complex patterns to simplify matching logic:
```cj
enum Command { | Ping | Pong(Int) | Error(String) }

func processCommand(cmd: Command) {
    match (cmd) {
case Ping => println("Ping received")
case Pong(_) => println("Pong received (parameter ignored)") // Match the Pong constructor but ignore the parameters
case Error(msg) => println("Error:\(msg)")
    }
}

processCommand(cmd: .Pong(123)) // Output: "Pong received (parameters ignored)"
```  


## 3. Exhaustion and type safety of pattern matching
The Cangjie compiler strictly checks the exhaustiveness of pattern matching to ensure that all possible values ​​are processed and avoid runtime vulnerabilities.

### 1. Enumeration type mandatory coverage requirements
For enumeration `RGBColor`, if all constructors are not matched and there are no wildcards, the compilation will report an error:
```cj
func incompleteMatch(color: RGBColor) {
    match (color) {
case Red => println("red") // Missing Green and Blue branches
// Compile error: "Not all constructors of RGBColor are covered"
    }
}
```  

### 2. Wildcard characters for numeric types
In numerical matching, wildcards are used to handle uncovered boundary values:
```cj
func validateNumber(n: Int) {
    match (n) {
case 1..100 => println("valid range")
case _ => println("out of range") // Guarantee all other values
    }
}
```  

### 3. Optimization of execution order of pattern matching
The matching rules follow the principle of "top to bottom, priority hitting" and need to place high-frequency conditions on the top:
```cj
enum Event { | Click | DoubleClick | LongPress }

func handleEvent(event: Event) {
    match (event) {
case DoubleClick => println("DoubleClick Processing") // High-frequency operation priority matching
case Click => println("Click Process")
case LongPress => println("Long press to process")
    }
}
```  


## 4. Mixed scenarios: Cooperation between constant mode and wildcard characters
In actual development, the accuracy of the constant pattern and the flexibility of wildcard characters are often combined to achieve concise logical expression.

### 1. Protocol instruction analysis
```cj
enum Protocol { | Get("get") | Post("post") | Other(String) }

func parseProtocol(cmd: String) {
    match (cmd) {
case Protocol.Get => println("processing GET request") // Constant string matching
case Protocol.Post => println("Processing POST request")
case Other(p) => println("Unknown Protocol:\(p)") // Wildcard captures the remaining value
    }
}

parseProtocol(cmd: "put") // Output: "Unknown Protocol: put"
```  

### 2. State machine default behavior
```cj
enum MachineState { | Running | Stopped | Paused(Int) }

func machineLogic(state: MachineState) {
    match (state) {
        case Running => start()
        case Stopped => stop()
        case Paused(time) => resume(time)
case _ => fatalError("illegal state") // In theory, unreachable, enhances robustness
    }
}
```  


## Summarize
Constant mode and wildcard mode are the basic tools for HarmonyOS Next type safety:
- **Constant mode**Use literals to achieve accurate value matching, suitable for enumeration states, fixed instructions and other scenarios;
- **Wildcard pattern** Ensure logic exhaustion is a necessary means to deal with default situations.
