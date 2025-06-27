# HarmonyOS enumeration performance optimization practice: double improvement of memory and matching efficiency

> As an old developer who has been enumerated performance pitted in embedded device development, the smart door lock was stuck due to unreasonable enumeration design, and later this optimization solution was summarized.Now share it with you so that the enumeration performance will no longer drag the project down.


## 1. The "split" rule of enumerating memory layout

### 1. No parameters enumeration: "Main Force" of Memory Saving
Each instance without parameters takes up only 1 byte, just like the tag in the toolbox:
```cj
enum DeviceState { | Idle | Working | Error } // Only 1 byte
```  
- The compiler automatically allocates the index (Idle=0, Working=1, Error=2)
- 1000 device status requires only 1KB of memory, saving 90% space than class instances

### 2. Enumeration of parameters: "Tailed in size" as needed
The enumeration memory with parameters depends on the maximum parameter type, and follows the "big principle":
```cj
enum SensorData {
| Temp(Float) // 4 bytes
| Humidity(UInt8) // 1 byte → It actually occupies 4 bytes (aligned)
}
```  
**Optimization Tips**:
- Replace `UInt32` with `UInt8` to store status code
- Split into parameterless + parameterless constructor to reduce redundancy:
  ```cj
  enum Cmd { | On | Off | SetLevel(UInt8) }
  ```  


## 2. The "efficiency password" for pattern matching

### 1. Matching order: "Fast Channel" with high frequency priority
Putting the common state in front is like putting the common tools on the top of the toolbox:
```cj
enum NetworkEvent {
    | DataReceived | Timeout | ConnectFailed
}

func handle(event: NetworkEvent) {
    match event {
case .DataReceived: processData() // High-frequency events are preferred
        case .Timeout: reconnect()
        case .ConnectFailed: logError()
    }
}
```  
**Measured data**: After high-frequency branches are advanced, the matching efficiency is increased by 30%

### 2. Combination mode: "merge skills" to reduce branches
Use `|` to merge similar patterns to avoid too many branches:
```cj
enum Key {
    | A | B | C | D | Func(Int)
}

func handleKey(key: Key) {
    match key {
        case .A | .B | .C: handleLetter()
        case .D: handleSpecial()
        case .Func(n) where n < 10: handleFunc(n)
        default: ignore()
    }
}
```  


## 3. The "Pipe Protection Guide" for Recursive Enumeration

### 1. Stack Overflow: "Collectroroute" of recursive depth
Recursive enumerations are like expression trees, and the stack will be burst after the depth:
```cj
enum Expr { | Num(Int) | Add(Expr, Expr) | Sub(Expr, Expr) }

func eval(expr: Expr) -> Int {
// Recursive depth = the number of nested layers of expression, more than 100 layers are prone to overflow
}
```  
**Solution**:
- Use iterative computing instead (maintaining stack structure)
- Enable tail recursive optimization (if the compiler supports it)

### 2. Tail recursion: a "weapon" for recursive optimization
```cj
@tailrec
func fact(n: Int, acc: Int = 1) -> Int {
    if n == 0 { return acc }
return fact(n-1, n*acc) // tail recursion, without increasing stack depth
}
```  


## 4. Practical combat: "Enumeration of slimming" for low-power devices

### 1. Sensor status enumeration design
Smart home sensor status enumeration, 100 instances require only 100 bytes:
```cj
enum SensorStat { | Normal | LowBat | Fault }
var stats: [SensorStat] = Array(repeating: .Normal, count: 100)
```  

### 2. Interrupt processing: "Life and Death Line" in the matching order
Embedded system interrupt processing, high-frequency interrupts are preferred:
```cj
enum Irq { | UART | Timer | ADC | GPIO }

func handleIrq(irq: Irq) {
    match irq {
case .UART: readBuf() // Communication interrupt is preferred
        case .Timer: updateTick()
        case .ADC: processADC()
        case .GPIO: handleIO()
    }
}
```  


## 5. Performance comparison and "pit avoidance list"

### 1. Memory usage comparison table
| Enumeration type | Constructor number | Single instance occupancy | Typical scenarios |
|----------------|----------|------------|------------------|  
| No parameter enumeration | 3 | 1 byte | State machine |
| Parameter Enumeration (Int) | 2 | 8 bytes | Command with numerical values ​​|
| Recursive Enumeration | 3 | Dynamic | Expression Analysis |

### 2. Optimization list (must do)
1. Enumeration without parameters is preferred, and the minimum data type is used for enumeration with parameters.
2. Pattern matching is sorted by frequency, with high frequency in front
3. Recursive enumeration over 50 layers and uses iterative instead
4. Combine similar patterns to reduce the number of branches
