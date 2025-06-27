# HarmonyOS Next Pattern Matching Core: Precise Control of Constants and Wildcards

Pattern matching is a powerful tool for Cangjie language to process complex logic, where constant patterns and wildcard patterns form the basis for type safety matching.This article will analyze the grammatical rules and application scenarios of these two modes through practical cases, helping developers master the core skills of accurate value matching and flexible bottom-up protection.


## 1. Constant mode: Implementation of accurate value matching

### 1. Supported literal matching types
| Type | Match Example | Core Features |
|------------|-----------------------|---------------------------|  
| Integer | `case 0`, `case 100` | Exact numerical equality match |
| String | `case "ok"`, `case 'A'`| Content equality match |
| Boolean value | `case true` | Logical value matching |
| Enumeration constructor | `case Direction.Up` | Enumeration instance precision matching |

### 2. Multi-value and range matching syntax
Connect multiple values ​​through `|` and define the range with `..` (left closed and right open):
```cj
let score = 85
let grade = match score {
case 90..100 => "A" // Range matching 90-99
case 80 | 85 | 90 => "B" // Multi-value accurate matching
    case 60..80 => "C"       // 60-79
case _ => "D" // Wildcard character bottom
}
// grade result is "B"
```  

### 3. Constant matching of enum types
The parameterless enumeration constructor can directly match and supports implicit type derivation:
```cj
enum Direction { | Up | Down | Left | Right }

func move(dir: Direction) {
    match dir {
case Up => println("up")
case Down => println("down")
case Left | Right => println("Horizontal Move")
    }
}

move(dir: .Right) // Output "horizontal movement"
```  


## 2. Wildcard mode: a universal solution with flexible bottom-up

### 1. Enumeration matching is a must-have guarantee
The compiler forces enumeration matching to cover all cases, and wildcards handle constructors that do not explicitly match:
```cj
enum Color { | Red | Green | Blue }

func showColor(c: Color) {
    match c {
case Red => print("red")
case Green => print("green")
case _ => print("blue") // Must be added, otherwise the compilation error will be reported
    }
}
```  

### 2. Ignore irrelevant values ​​in deconstruction
Wildcards ignore unwanted variables when deconstructing:
```cj
let (x, _) = (10, 20) // Get only x=10
println(x) // Output 10

for (_ in 0..5) { // Ignore the loop index
println("Iteration")
}
```  

### 3. Partial matching with parameter enumeration
Match the constructor but ignore the parameters, simplify the logic:
```cj
enum Command { | Ping | Pong(Int) | Error(String) }

func process(cmd: Command) {
    match cmd {
case Ping => print("Ping received")
case Pong(_) => print("Pong received") // Ignore parameters
case Error(msg) => print("Error:\(msg)")
    }
}

process(cmd: .Pong(123)) // Output "Pong received"
```  


## 3. Exhaustion check of type safety

### 1. Enumeration match mandatory override
When all enumeration constructors are not overwritten and there are no wildcards, the compiler reports an error:
```cj
enum State { | Idle | Working | Error }

func update(state: State) {
    match state {
case Idle => print("idle")
case Working => print("work")
// Compilation error: Error status not handled
    }
}
```  

### 2. Boundary processing of numerical matching
Wildcards deal with undefined ranges of values:
```cj
func check(n: Int) {
    match n {
case 1..100 => print("valid")
case _ => print("Invalid") // Process all other values
    }
}
```  

### 3. Matching order optimization
High-frequency conditions are preferred to improve execution efficiency:
```cj
enum Event { | Click | DoubleClick | LongPress }

func handle(e: Event) {
    match e {
case DoubleClick => print("DoubleClick") // High frequency operation is preferred
case Click => print("click")
case LongPress => print("Long Press")
    }
}
```  


## 4. Practical scenarios: Mode combination application

### 1. Protocol instruction analysis
Constant pattern matching fixed instructions, wildcard processing extended instructions:
```cj
enum Protocol { | Get("get") | Post("post") | Other(String) }

func parse(cmd: String) {
    match cmd {
case Protocol.Get => print("processing GET")
case Protocol.Post => print("process POST")
case Other(p) => print("Unknown protocol:\(p)")
    }
}

parse(cmd: "put") // Output "Unknown Protocol:put"
```  

### 2. State machine default behavior
Wildcard enhances the robustness of state machines:
```cj
enum Machine { | Run | Stop | Pause(Int) }

func control(m: Machine) {
    match m {
        case Run => start()
        case Stop => end()
        case Pause(t) => wait(t)
case _ => error() // Theories are unreachable, enhancing robustness
    }
}
```  


## Summarize
Constant mode and wildcard mode form the basic ability of pattern matching:
- Constant mode achieves accurate value matching through literals, suitable for enumeration states, protocol instructions and other scenarios
- Wildcard pattern ensures logical integrity and is a must-have tool for handling default situations and type safety
- Exhaustible checking mechanism of the compiler to avoid runtime logic vulnerabilities from the source

Mastering the coordinated use of these two modes can keep the code simple while maintaining both type safety and maintainability.
