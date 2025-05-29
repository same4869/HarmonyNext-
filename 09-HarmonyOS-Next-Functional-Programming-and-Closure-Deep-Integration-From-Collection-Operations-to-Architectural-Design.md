
# HarmonyOS Next Functional Programming and Closure Deep Integration: From Collection Operations to Architectural Design

> This article aims to deeply explore the technical details of Huawei HarmonyOS Next system, and summarize the integrated application of functional programming and closures based on actual development practices.Combined with the contents of documents such as "0002-Closure-Function-Cangjie Programming Language Development Guide-Learning Cangjie Language.docx", focus on the collection operation, state management and architectural design scenarios to avoid unmentioned features.


## 1. The core paradigm of functional programming: the coordination between pure functions and closures

In Cangjie language, functional programming implements declarative expression of data processing through a combination of pure functions (no side effects, same input and same output) and closures.In this process, closures assume the dual role of state capture and logical encapsulation, especially in collection operations.

### 1.1 Closure encapsulation of pure functions
Encapsulate the data conversion logic into a closure to ensure the purity and reusability of the function.

**Example: Array Deduplication and Filtering**
```typescript  
// Pure function: filter non-unique values
func distinct<T: Equatable>(array: Array<T>): Array<T> {  
  var seen = Set<T>()  
  return array.filter { seen.insert($0).inserted }  
}  

// Closure capture filtering conditions
func createFilter<T>(predicate: (T) -> Bool): (Array<T>) -> Array<T> {  
  return { array in array.filter(predicate) }  
}  

// Use scenario: filter even numbers and de-repeat
let numbers = [1, 2, 2, 3, 4, 4, 4]  
let evenFilter = createFilter { $0 % 2 == 0 }  
let result = evenFilter(numbers).distinct() // Output: [2, 4]
```  

### 1.2 The "memory effect" of closure conflicts with pure functions
If a closure captures a mutable variable (`var`), it will cause the function to be impure.Pure function characteristics need to be ensured through `let` or class instance.

**Counterexample: Closure capture `var` destroys purity**
```typescript  
var globalCounter = 0  
func impureClosure() -> () -> Int64 {  
  var count = 0  
return { count += 1 } // Impurity function, relying on mutable state
}  

**Recommended: Use class encapsulation status**
```typescript  
class Counter {  
  private var count = 0  
  func increment(): Int64 { return count++ }  
}  

let counter = Counter()  
let pureIncrement = { counter.increment() } // Pure function, state is managed by class
```  


## 2. Functional practice of collection operations: the combination of closures and stream operators

### 2.1 Stream operator (|>) and closure chain call
Through the `|>` operation character concatenating multiple closures in a string, the data processing pipeline is realized and the code readability is improved.

**Example: string array cleaning and conversion**
```typescript  
let rawData = ["  apple  ", "BANANA", "orange", "  MANGO  "]  
let processed = rawData  
|> map { $0.trim() } // Remove the beginning and end spaces
|> map { $0.lowercased() } // Convert to lowercase
|> filter { $0.length > 5 } // Filter strings with lengths greater than 5
|> sort() // Sort

// Output: ["banana", "mango"]
```  

### 2.2 Custom operators and closure combinations
By combining single parameter functions with the `~>` operator, functional combination of complex logic is realized.

**Example: Data Verification and Conversion Pipeline**
```typescript  
func validateEmail(email: String): Result<String, Error> {  
// Verification logic, return Result type
}  

func encodeEmail(email: String): String {  
// Encoding logic
}  

let pipeline = validateEmail ~> encodeEmail // Combination verification and encoding functions
let result = pipeline("user@example.com") // equivalent to encodeEmail(validateEmail(...))
```  


## 3. Closure application in state management: from component to global state

### 3.1 Component-level state closure
In ArkUI, the private state of the component is encapsulated by closure to avoid overuse of `@State`.

**Example: Closure implementation of counter component**
```typescript  
@Entry  
struct CounterComponent {  
  private counterClosure: () -> Int64 = {  
    var count = 0  
    return { count += 1 }  
  }()  

  build() {  
    Column {  
      Text("Count: \(counterClosure())")  
      Button("Increment").onClick(counterClosure)  
    }  
  }  
}  
```  

### 3.2 Global state management: combining closures and singleton mode
Use the singleton feature of closure to achieve lazy initialization of global state.

```typescript  
let globalState: () -> GlobalState = {  
  var state = GlobalState()  
  return { state }  
}()  

//Usage scenario: Global status access
func getGlobalData() {  
  let state = globalState()  
// Operate state data
}  
```  


## 4. Architectural design: the layered practice of functional thinking

### 4.1 Domain logic layer: closure encapsulation business rules
Abstract business logic into closures, isolate external dependencies, and improve testability.

**Example: Order price calculation rules**
```typescript  
struct Order {  
  var amount: Float64  
  var discount: Float64  
}  

// Counterfeit discount calculation rules
let calculateFinalPrice: (Order) -> Float64 = { order in  
  order.amount * (1 - order.discount)  
}  

// Can be easily replaced with other calculation rules
let holidayDiscount: (Order) -> Float64 = { order in  
calculateFinalPrice(order) * 0.95 // Overlay holiday discount
}  
```  

### 4.2 Infrastructure layer: Closures adapt to external services
Dependency inversion is achieved through closure and third-party library calls.

```typescript  
// Closure abstract network request
func fetchData<T>(url: String, parser: (Data) -> T): Future<T> {  
  return networkClient.request(url).map(parser)  
}  

//Usage scenario: adapt to different API response formats
let fetchUser = fetchData<User>("https://api/user", parseUserJSON)  
let fetchProduct = fetchData<Product>("https://api/product", parseProductJSON)  
```  


## 5. Performance optimization and trap avoidance

### 5.1 Avoid high-frequency calculations in closures
Move the unchanged computational logic outside the closure to reduce runtime overhead.

**Pre-optimization**
```typescript  
func processData(data: Data) {  
  let processor = { data in  
let hash = calculateHash(data) // High frequency call, repeated calculation
// Other processing
  }  
  processor(data)  
}  

**Optimized**
```typescript  
func processData(data: Data) {  
let hash = calculateHash(data) // Calculate in advance
  let processor = { _ in  
// Use pre-calculated hash
  }  
  processor(data)  
}  
```  

### 5.2 Closures and Memory Management
- Avoid closures holding large object references for a long time, using weak references (if Cangjie supports them) or local scope restrictions;
- Closures in collection operations should prioritize the use of value type parameters to reduce the memory overhead caused by reference types.

**Example: Weak references avoid memory leaks**
```typescript  
class ViewModel {  
  private weak var view: View?  
  func loadData() {  
    networkRequest { [weak self] data in  
Self?.view?.update(data) // Weak references avoid circular references
    }  
  }  
}  
```  


## 6. Boundaries and best practices of functional closures

### 6.1 Summary of applicable scenarios
- **Simple data conversion**: set filtering, mapping, reduction and other operations;
- **Event-driven logic**: UI event callbacks, asynchronous operation processing;
- **Lightweight state management**: Component private state, temporary computing cache.

### 6.2 Not applicable
- **Complex business logic**: Closure nestings over 3 layers should be split into classes or modules;
- **Shared variable state**: Global state change logic is recommended to use a state management framework (such as Redux) instead of closures;
- **High Performance Computing**: Closures in high-frequency loops may introduce additional overhead, giving priority to native loops.


## Conclusion: The "moderate use" philosophy of functional closures

The integration of functional programming and closures is an efficient tool developed by HarmonyOS Next, but it must follow the principle of "moderate use":
- **Small and beautiful**: Use closures to deal with single responsibility logic to avoid excessive complexity;
- **Pure functions are preferred**: Use immutable data and pure functions as much as possible to reduce side effects;
- **Architecture Layer**: Use closures in the domain layer and tool layer, and maintain restraint at the interface layer and infrastructure layer.

By combining functional thinking with the characteristics of the Hongmeng framework, developers can build more flexible and maintainable application architectures, especially unlocking greater potential in cross-device collaboration and lightweight application scenarios.
