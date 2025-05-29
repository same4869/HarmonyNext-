
# HarmonyOS Next Functional Programming and Practical Application of Closures in Collection Operations

> This article focuses on the specific practices of functional programming and closures in collection operations in HarmonyOS Next, and analyzes how to use closures to achieve efficient data processing logic through code examples to avoid involving unmentioned features.


## 1. Collection filtering and conversion: dynamic condition capture of closures
When processing collection data such as arrays and lists, closures can dynamically capture filtering conditions or conversion rules, separate business logic from data operations, and improve code reusability.

### 1.1 Dynamically filter collection elements
Encapsulate filtering logic through the closure factory function `createFilter`, allowing different filtering conditions to be passed in at runtime.
```typescript  
// Closure factory: Generate generic filtering functions
func createFilter<T>(predicate: (T) -> Bool): (Array<T>) -> Array<T> {  
  return { array in array.filter(predicate) }  
}  

// Business scenario: Filter long text in string array (length>5)
let texts = ["apple", "banana", "cherry", "date"]  
let longTextFilter = createFilter { $0.length > 5 }  
let result = longTextFilter(texts) // Output: ["banana", "cherry"]
```  
**Key Points**:
- The `predicate` closure parameter is responsible for the specific filtering logic, and the closure returned by `createFilter` is responsible for performing filtering;
- Support dynamic switching conditions (such as switching from length filtering to keyword filtering), without modifying the filter execution logic.

### 1.2 Type Conversion and Mapping
Use closures to implement type conversion of collection elements, and build processing pipelines in combination with the flow operator `|>`.
```typescript  
// String to integer array (ignoring invalid values)
let stringNumbers = ["1", "2", "three", "4"]  
let toInt = { (s: String) -> Int64? in Int64(s) } // Closure handling type conversion
let numbers = stringNumbers  
|> map(toInt) // Map as optional integer
|> filter { $0 != nil } // Filter empty values
|> map { $0! } // Unpacking optional value

// Output: [1, 2, 4]
```  
** Advantages**:
- Each step of transformation is completed by an independent closure, which is logically clear and reusable;
- `|>` operator makes data flow intuitive, easy to debug and expand.


## 2. Collection sorting and deduplication: the coordination between pure functions and closures
Pure functions ensure the determinism of the sorting rules, while closures are responsible for capturing dynamic sorting parameters, combining the two to achieve flexible set sorting.

### 2.1 Custom sorting rules
Passing sorting logic through closures supports running-time adjustment of sorting strategies (such as ascending, descending, and custom field sorting).
```typescript  
// Pure functions: general sorter (accepts comparison closures)
func sort<T>(array: Array<T>, comparator: (T, T) -> Bool): Array<T> {  
  return array.sorted(by: comparator)  
}  

// Business scenario: Sort by descending order of string length
let fruits = ["apple", "grape", "banana", "pear"]  
let sortByLength = sort(comparator: { $0.length > $1.length })  
let sortedFruits = sortByLength(fruits) // Output: ["banana", "grape", "apple", "pear"]
```  
**Design points**:
- The `comparator` closure defines the specific comparison logic, and the `sort` function focuses on sorting implementation;
- Supports complex sorting (such as multi-level conditions), just modify the comparison rules within the closure.

### 2.2 Closure encapsulation of deduplication logic
Use closures to capture the uniqueness judgment rules of collection elements to realize the generic deduplication function.
```typescript  
// Pure functions: deduplication based on custom equality judgment
func distinct<T>(array: Array<T>, isEqual: (T, T) -> Bool): Array<T> {  
  var uniqueItems = [T]()  
  for item in array {  
    if !uniqueItems.contains(where: { isEqual($0, item) }) {  
      uniqueItems.append(item)  
    }  
  }  
  return uniqueItems  
}  

// Scene: Deduplicate custom objects (judging equality by ID)
struct User {  
  var id: Int64  
  var name: String  
}  

let users = [User(id: 1, name: "Alice"), User(id: 2, name: "Bob"), User(id: 1, name: "Alice")]  
let distinctUsers = distinct(users, isEqual: { $0.id == $1.id }) // Output: [User(id:1), User(id:2)]
```  
**Key Logic**:
- The `isEqual` closure defines the object equality rules, decouples the deduplication logic and specific types;
- Suitable for complex types that cannot be used directly with the `Equatable` protocol.


## 3. Set reduction and aggregation: state accumulation of closures
Reduce operations accumulate collection elements into a single result through closures, which are responsible for state update logic in this process.

### 3.1 Numerical Aggregation Calculation
Use closures to define the accumulation logic to implement summing, product and other operations.
```typescript  
// Calculate the sum of squared elements of the array
let numbers = [1, 2, 3, 4]  
let sumOfSquares = numbers.reduce(0) { acc, num in  
acc + num * num // Closed square value
} // Output: 30 (1+4+9+16)
```  
**Simplicity reflects**:
- The closure parameter `acc` is the cumulative state, and `num` is the current element, and the logic is straightforward;
- Can be easily extended to other aggregation logic (such as finding maximum, average).

### 3.2 Complex object aggregation
Grouping, statistics and other operations on custom object collections, and the closure is responsible for extracting feature values.
```typescript  
// Statistics the total amount of the order (the order list contains discount information)
struct Order {  
  var quantity: Int64  
  var price: Float64  
  var discount: Float64  
}  

let orders = [Order(quantity: 2, price: 10.0, discount: 0.1), Order(quantity: 1, price: 15.0, discount: 0.2)]  
let totalAmount = orders.reduce(0.0) { acc, order in  
  let itemPrice = order.price * (1 - order.discount) * Float64(order.quantity)  
return acc + itemPrice // closure calculates the amount of a single order and accumulates it
} // Output: (2*10*0.9)+(1*15*0.8)=18+12=30.0
```  
**Advantage Analysis**:
- The closure can contain complex business logic (such as discount calculations) to maintain the universality of reduction operations;
- Avoid explicit loop traversal, the code is more in line with the functional programming paradigm.


## 4. Performance optimization and precautions
### 4.1 Avoid unnecessary operations in closures
Remove the invariant calculations from the closure to reduce duplicate processing in the loop.
```typescript  
// Counterexample: Repeated calculation of threshold values ​​within closure
let threshold = 100  
let data = [1, 2, 3, ..., 1000]  
let filtered = data.filter { $0 * 2 > threshold } // Each time the closure is called, the threshold value is calculated

// Optimization: Calculate the threshold multiple in advance
let doubleThreshold = threshold * 2  
let filtered = data.filter { $0 > doubleThreshold } // Only comparison operations are performed in the closure
```  

### 4.2 Preferential use of built-in higher-order functions
The collection types of Cangjie language (such as `Array`) have built-in higher-order functions such as `filter`, `map`, `reduce`, etc., and their performance has been optimized and should be used first rather than manually implemented.
```typescript  
// Recommended: Use built-in filter instead of custom loops
let evenNumbers = numbers.filter { $0 % 2 == 0 }  

// Not recommended: Manually implement filtering logic
let evenNumbers = [Int64]()  
for num in numbers { if num % 2 == 0 { evenNumbers.append(num) } }  
```  


## 5. Summary: The core value of functional closures in collection operations
Through the integration of functional programming and closures, developers can implement it in Hongmeng applications:
- **Declarative data processing**: Clearly express the data conversion process through closure chain;
- **Logical multiplexing and decoupling**: Closure encapsulate independent business rules, supporting dynamic replacement;
- **Performance and readability balance**: Use built-in high-order functions and closure combinations to avoid redundant code.

In actual development, we recommend following the principle of "single responsibility for closures". Each closure focuses on completing a data processing step, forming a complete processing pipeline through a combination of stream operators or functions to ensure that the code is concise and efficient.
