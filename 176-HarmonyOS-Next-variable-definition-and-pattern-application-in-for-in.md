
# HarmonyOS Next variable definition and pattern application in for-in

In HarmonyOS Next development, pattern matching is not limited to `match` expression, but can also be directly used in the ** variable definition ** and ** for-in` loops.Secure destruction of complex data structures can be achieved by placing the pattern to the left of the equal sign or after the `for` keyword.This article combines document knowledge points to analyze how to use the Irrrefutable Pattern to achieve efficient data extraction and collection traversal.


## 1. Pattern destruction in variable definition
When a variable is defined, the pattern is located to the left of the equal sign, which is used to extract specific fields from the value or deconstruct complex types.Only support **No refutation mode** to ensure that the assignment is successful.

### 1. Tuple Deconstruction: Extracting Multi-field Data
```cj
// Basic tuple destruction
let (x, y) = (10, 20) // Deconstruct into two variables x=10, y=20
println("Coordinates: (\(x), \(y))") // Output: Coordinates: (10, 20)

// Named tuple deconstruction (by field name matching)
let point = (x: 3.0, y: 4.0)
let (x: _, y: coordinateY) = point // Ignore the x field and extract y as coordinateY
println("Y coordinate: \(coordinateY)") // Output: Y coordinate: 4.0
```  

### 2. Enumeration deconstruction: Extract constructor parameters
```cj
enum Temperature { | Celsius(Float) | Fahrenheit(Float) }
let temp = Celsius(25.5)

// Deconstruct the enumeration constructor parameters
let Celsius(degree) = temp // Directly extract degree=25.5
println("Celsius temperature:\(degree)℃")

// Simplified deconstruction of single constructor enumeration
enum Unit { | Meter(Double) }
let Meter(length) = Unit.Meter(10.5) // equivalent to let length = 10.5
```  

### 3. Mixed mode: Deconstructing tuples and enumerations in combination
```cj
enum Data { | Value((Int, String)) }
let data = Data.Value((42, "Answer"))

// Deconstruct the enumeration first, then deconstruct the tuple
let Data.Value((number, str)) = data // Extract number=42, str="Answer"
println("value: \(number), string: \(str)")
```  


## 2. Pattern matching in for-in loop
The `for-in` loop supports the use of patterns between `for` and `in` to implement deconstruction and traversal of collection elements.The same requires that the pattern is **No refutation mode** to ensure that each iteration can be matched successfully.

### 1. Deconstruction traversal of tuple collections
```cj
let points = [(1, 2), (3, 4), (5, 6)]
for ((x, y) in points) { // Tuple pattern deconstructs each element
println("Point(\(x), \(y))")
}
/* Output:
Points (1, 2)
Points (3, 4)
Points (5, 6)
*/
```  

### 2. Deconstruction traversal of enumerated collections
```cj
enum Command { | Ping | Pong(Int) }
let commands = [Ping, Pong(1), Pong(2)]

for cmd in commands {
    match (cmd) {
case Ping => println("Ping received")
case Pong(n) => println("Pong:\(n)")
    }
}
/* Output:
Received Ping
Received Pong: 1
Received Pong: 2
*/
```  

### 3. Hierarchical destruction of nested structures
```cj
let nestedTuples = [( (1, "a"), (2, "b") ), ( (3, "c"), (4, "d") )]
for ( (num1, str1), (num2, str2) in nestedTuples ) { // Double-layer tuple pattern
println("First layer: \(num1), \(str1); second layer: \(num2), \(str2)")
}
```  


## 3. The irrefutable requirement of the model
Only **Non-refutable mode** is allowed in variable definitions and `for-in` loops, for the following reasons:
1. **Security**: Avoid program crashes due to matching failure during runtime;
2. **Compiler restrictions**: The compiler must ensure that the pattern must match during the compilation period, otherwise an error will be reported.

### 1. Prohibited scenarios in refutation mode
```cj
// Counterexample: Constant mode is a refutation mode, which is prohibited from being used in variable definitions
let 1 = x // Compile error: Cannot bind to a refutable pattern in variable declaration

// Counterexample: Partial enumeration constructor matching (refutable)
enum E { | A | B }
let A = E.B // Compile error: Pattern matches only some possible values ​​of type 'E'
```  

### 2. Example of legal non-refutable mode
| Pattern type | Example | Reasons for a must-match |
|----------------|-------------------------------|---------------------------------|  
| Binding pattern | `let x = 10` | Match any value, bind to variable x |
| Full tuple pattern | `let (a, b) = (1, 2)` | The number of tuple elements is exactly the same as the pattern |
| Single constructor enum | `let A(n) = Enum.A(5)` | Enum contains only A constructor |
| Wildcard pattern | `let _ = "hello"` | Match any value, ignore specific content |


## 4. Practical scenarios: data analysis and collection processing
### 1. Configuration file destruction (tuple pattern)
```cj
// Assume that the configuration file returns a tuple (key, value)
let config = ("timeout", 30)

// Deconstruct into variable names and values
let (key, value) = config  
println("Configuration item: \(key)=\(value)") // Output: Configuration item: timeout=30
```  

### 2. Sensor data traversal (enumeration mode)
```cj
enum SensorData {
    | Temperature(Float)
    | Humidity(Float)
}

let readings = [Temperature(25.5), Humidity(60.0)]

for case let SensorData.Temperature(temp) in readings { // Process only temperature data
println("Temperature:\(temp)℃")
}
```  

### 3. Batch processing of nested enums
```cj
enum NestedEnum {
    | Item(String, Int)
    | List(Array<NestedEnum>)
}

let list = NestedEnum.List([Item("a", 1), Item("b", 2)])

// Recursively traverse nested lists
func process(item: NestedEnum) {
    switch item {
        case let Item(str, num):
            println("\(str): \(num)")
        case let List(items):
            for item in items {
                process(item: item)
            }
    }
}

process(item: list)
/* Output:
a: 1
b: 2
*/
```  


## Summarize
Applying pattern matching in variable definition and `for-in` loop is a key technology for HarmonyOS Next to implement concise data deconstruction.Developers need to master:
1. Use only non-refutable mode to ensure deconstruction security;
2. Use tuple pattern and enumeration pattern to extract fields in complex structures;
3. Filter or convert elements through pattern matching during collection traversal.
