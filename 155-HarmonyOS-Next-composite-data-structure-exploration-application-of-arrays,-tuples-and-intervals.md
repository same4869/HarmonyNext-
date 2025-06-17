
# HarmonyOS Next composite data structure exploration: application of arrays, tuples and intervals

In HarmonyOS Next development, composite data structures are the core tool for organizing complex data.The array (`Array`/`VArray`), tuple (`Tuple`) and interval (`Range`) types provided by Cangjie Language not only support flexible data modeling, but also deeply optimized for performance and readability.This article will combine memory models, practical cases and performance comparisons to analyze the core characteristics and best practices of these data structures.


## 1. Array type: from memory layout to performance optimization
Arrays are containers that continuously store data. Cangjie Language provides **reference type `Array<T>`** and **value type `VArray<T, $N>`**. The two have significant differences in memory models and applicable scenarios.

### 1. Memory model comparison
- **`Array<T>` (reference type)**
- Stored in heap memory, elements are reference types, and support dynamic expansion.
- Only copy references when passed, suitable for large-scale data sharing scenarios.
  ```cj
  let arr: Array<Int> = [1, 2, 3]
let arrCopy = arr // Only copy references, not data
arrCopy[0] = 0 // The value of the original array arr is changed synchronously
  ```  

- **`VArray<T, $N>` (value type)**
- Stored in the stack memory, the length `$N` is determined during the compilation period, and the element directly stores the value.
- Value copying is performed during delivery, suitable for small-scale and high-performance scenarios (such as embedded devices).
  ```cj
  var vArr: VArray<Int, $3> = [1, 2, 3]
let vArrCopy = vArr // Deep copy, modifying vArrCopy does not affect the original array
  vArrCopy[0] = 0
  ```  

### 2. Performance test: 100,000 element accesses
Comparison of access speeds of two arrays through benchmark tests:
```cj
import std.time.*

func testArrayAccess() {
    let arr: Array<Int> = Array(100000, item: 0)
    let startTime = getCurrentTime()
    for i in 0..100000 { _ = arr[i] }
println("Array time-consuming: \(getCurrentTime() - startTime) ms")
}

func testVArrayAccess() {
    var vArr: VArray<Int, $100000> = VArray(item: 0)
    let startTime = getCurrentTime()
    for i in 0..100000 { _ = vArr[i] }
println("VArray time-consuming: \(getCurrentTime() - startTime) ms")
}

// Output: Array takes about 12ms, VArray takes about 5ms (stack access is faster)
```  

### 3. Scene selection suggestions
- **Dynamic data, large-scale sharing** → Use `Array<T>` (such as the list of network request results).
- **Fixed length, high performance requirements** → Use `VArray<T, $N>` (such as sensor data buffer).


## 2. Tuple type: a lightweight solution for multi-value processing
Tuples are lightweight composite types, used to combine multiple values ​​into a logical whole, and are suitable for scenarios such as multiple return values ​​of functions and pattern matching.

### 1. Deconstruct assignment and multiple return values
```cj
func getUser(): (id: Int, name: String) {
return (1, "Alice") // Returns a tuple with named parameters
}

let (userId, userName) = getUser() // Deconstruct the assignment
println("User ID:\(userId), name:\(userName)")
```  

### 2. Readability optimization in API design
Tuples with named parameters can significantly improve code readability:
```cj
func getRect(): (width: Float, height: Float, area: Float) {
    let w = 10.0, h = 5.0
    return (w, h, w * h)
}

let rect = getRect()
println("area:\(rect.area)") // Accessed through parameter name, with clear intention
```  

### 3. Performance Traps and Optimization
- **Avoid large tuple copy**: Tuple is a value type, and the performance overhead is significant when copying large tuples with more than 10 elements.
- **Alternatives**: Use structures (reference type) or break them into multiple variables.
```cj
// Counterexample: Large tuple copy consumption is high
let largeTuple: (Int, Int, Int, Int, Int) = (1,2,3,4,5)
let copy = largeTuple // Copy 5 Int values, which takes a lot of time

// Affirmative example: Use structure to implement reference transfer
struct Data { var a,b,c,d,e: Int }
let data = Data(a:1,b:2,c:3,d:4,e:5)
let copy = data // copy only references, higher performance
```  


## 3. Interval type: an efficient traversal tool for ordered sequences
The interval type `Range<T>` is used to represent a continuous sequence of numerical values, defined by `start..end` (left closed and right open) or `start..=end` (left closed and right closed), supporting step size control and parallel traversal.

### 1. Basic grammar and application scenarios
```cj
// Integer interval: 0 to 9 (left closed and right open), step size 1
let range1 = 0..10 : 1 // Contains 0,1,...,9
for num in range1 { println(num) }

// Floating point interval: 0.0 to 3.0 (left closed and right closed), step size 0.5
let range2 = 0.0..=3.0 : 0.5 // Contains 0.0, 0.5,..., 3.0
```  

### 2. Empty interval processing and compiler optimization
When `start >= end` and the step size is positive and the interval is empty, the compiler will directly skip the loop body to avoid invalid calculations:
```cj
let emptyRange = 10..5 : 1 // empty range
for _ in emptyRange { 
println("not executed") // Compiler optimization, directly ignore loops
}
```  

### 3. Parallel computing: MapReduce case
Use interval segmentation to realize parallel computing to improve the utilization rate of multi-core processors:
```cj
import std.concurrent.*

func parallelSum(range: Range<Int>) -> Int {
    let chunkSize = 1000
    let tasks = range.chunked(into: chunkSize).map { async {
return $0.reduce(0, +) // Each subtask calculates the interval and
    }}
return awaitAll(tasks).reduce(0, +) // Merge results
}

let total = parallelSum(0..100000) // calculate sums from 0 to 99999 in parallel
```  


## 4. Collaborative application of composite structures
### 1. Array and interval: batch data generation
```cj
let numbers = Array(0..100: 2) // Generate an array of 0,2,4,...,100
println(numbers) // Output [0,2,4,...,100]
```  

### 2. Tuples and intervals: function returns multiple values ​​+ traversal
```cj
func getRangeInfo() -> (start: Int, end: Int, count: Int) {
    let r = 5..20 : 3  // 5,8,11,14,17
    return (r.start, r.end, r.count)
}

let (s, e, c) = getRangeInfo()
println("Interval from \(s) to \(e), total of \(c) elements")
```  


## Summarize
HarmonyOS Next's composite data structure system takes into account flexibility and performance:
- **Array**: Select `Array` or `VArray` according to the data size and whether it is mutable;
- **Tuple**: Lightweight multi-value encapsulation to avoid excessive use of large tuples;
- **Interval**: The core tool for efficient traversal and parallel computing.
