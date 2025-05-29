
# HarmonyOS Next Functional Programming and Closure Deep Integration: From Collection Operations to Architectural Design


## 1. Collection operation optimization: declarative expression of pure functions and closures
In data processing scenarios, functional programming disassembles complex data conversion logic into reusable operating units through the combination of pure functions and closures.For example, when deduplication, filtering, and type conversion of an array, closures can capture dynamic filtering conditions, while pure functions ensure determinism of data processing.

### 1.1 Array deduplication and conditional filtering
```typescript  
// Pure functions: implement generic array deduplication (judgment of dependency value type equality)
func distinct<T: Equatable>(array: Array<T>): Array<T> {  
  var seen = Set<T>()  
  return array.filter { seen.insert($0).inserted }  
}  

// Closure factory: Dynamically generate filtering functions (capture external conditions)
func createFilter<T>(predicate: (T) -> Bool): (Array<T>) -> Array<T> {  
  return { array in array.filter(predicate) }  
}  

// Business scenario: filter even numbers and remove heavy
let numbers = [1, 2, 2, 3, 4, 4, 4]  
let evenFilter = createFilter { $0 % 2 == 0 } // Closure captures even-number judgment logic
let result = evenFilter(numbers).distinct() // Output: [2, 4]
```  
**Key Points**:
- `distinct` is a pure function with no side effects and only depends on input arrays and generic constraints;
- `createFilter` realizes condition dynamics through closure encapsulation filtering logic and improves reusability.

### 1.2 Stream operators and closure chain processing
Using the `|>` operation string concatenation of multiple closures can be transformed into a clear pipeline model.For example, clean the string array and perform multi-level conversion:
```typescript  
let rawData = ["  apple  ", "BANANA", "orange", "  MANGO  "]  
let processed = rawData  
|> map { $0.trim() } // Closure 1: Remove the beginning and end spaces
|> map { $0.lowercased() } // Closure 2: Convert to lowercase
|> filter { $0.length > 5 } // Closure 3: Filter strings with length greater than 5
|> sort() // Closure 4: Sort Output

// Final result: ["banana", "mango"]
```  
** Advantages**:
- Each step of the transformation logic is responsible for independent closures and comply with the principle of single responsibility;
- Chain calls are highly readable, easy to debug and extend (such as inserting new processing steps).


## 2. Component state management: lightweight encapsulation of closures
In ArkUI development, closures can replace part of `@State` to implement component private state management, which is especially suitable for component scenarios with simple logic and independent life cycles.

### 2.1 Closure implementation of counter component
```typescript  
@Entry  
struct CounterComponent {  
// Closure encapsulation counter status (avoid @State contaminating component definition)
  private var counter: () -> Int64 = {  
    var count = 0  
    return { count += 1 }  
  }()  

  build() {  
    Column {  
      Text("Count: \(counter())")  
        .fontSize(24)  
      Button("Increment")  
.onClick(counter) // Directly call closure to update status
    }  
  }  
}  
```  
**characteristic**:
- The `count` variable in the closure forms a private state and cannot be directly accessed from the outside;
- The closure is used as an `onClick` callback and automatically updates the UI when triggered (responsive mechanism that relies on ArkUI).

### 2.2 State isolation of complex interactive components
For components that require multi-state collaboration (such as pagers), state linkage can be achieved through closure combination:
```typescript  
@Entry  
struct Pagination {  
  private var (currentPage, totalPages) = (1, 10)  
  private var updatePage: (Int64) -> Unit = { newPage in  
    currentPage = newPage  
    println("Page changed to \(newPage)")  
  }  

  build() {  
    Row {  
      Button("Previous")  
        .onClick { updatePage(currentPage > 1 ? currentPage - 1 : 1) }  
      Text("Page \(currentPage) of \(totalPages)")  
      Button("Next")  
        .onClick { updatePage(currentPage < totalPages ? currentPage + 1 : totalPages) }  
    }  
  }  
}  
```  
**Design points**:
- `updatePage` encapsulates paging logic, decouples UI interaction and state changes;
- Closure captures `currentPage` and `totalPages` to ensure state consistency.


## 3. Architectural layering practice: the application of closures in the domain and infrastructure layer
Functional closures act as a adhesive for architectural hierarchy, creating clear boundaries between domain logic and external dependencies.

### 3.1 Domain logic layer: closure abstraction of business rules
Encapsulate business computing rules into closures for easy testing and dynamic switching.For example, the price calculation of e-commerce orders:
```typescript  
struct Order {  
  var originalPrice: Float64  
  var discountRate: Float64  
}  

// Basic price calculation (pure function)
let calculateBasePrice: (Order) -> Float64 = { $0.originalPrice * (1 - $0.discountRate) }  

// Closure combination: superimposed holiday discounts (relying on basic calculations)
let holidayPromotion: (Order) -> Float64 = { order in  
calculateBasePrice(order) * 0.95 // Call pure functions in the closure to keep the logic clear
}  

// Dynamic selection of calculation rules during runtime
func processOrder(order: Order, strategy: (Order) -> Float64) {  
  let finalPrice = strategy(order)  
  println("Final Price: \(finalPrice)")  
}  

// Example of usage: Ordinary orders and holiday orders are processed separately
processOrder(order: normalOrder, strategy: calculateBasePrice)  
processOrder(order: holidayOrder, strategy: holidayPromotion)  
```  
** Advantages**:
- Business rules are separated from calling logic, and support runtime policy switching;
- Closures can be passed as parameters, comply with the principle of dependency inversion.

### 3.2 Infrastructure layer: closure adaptation for external services
By wrapping third-party library calls through closures, avoiding components directly relying on specific implementations.For example, the abstraction of network requests:
```typescript  
// Closure encapsulate network requests (return to Future type)
func fetchData<T>(url: String, decoder: (Data) -> T): Future<T> {  
  return NetworkClient.request(url)  
.map { data in decoder(data) } // Closure processing data decoding
    .catch { error in handleNetworkError(error) }  
}  

// Domain layer call (relying on abstract closures rather than concrete implementations)
func loadUserProfile(userId: String) {  
  fetchData(url: "https://api/user/\(userId)", decoder: User.decode) { user in  
updateUI(with: user) // The closure processing request successfully callback
  }  
}  
```  
**实践价值**：  
- Easy to simulate external services for unit testing;
- When replacing the network library, you only need to modify the closure implementation, and it does not affect the upper layer logic.


## 4. Performance optimization and precautions
### 4.1 Avoid repeated calculations in closures
Calculate invariants in advance to reduce runtime overhead in closures:
```typescript  
// Counterexample: Repeat calculation of hash value in closure
func processImages(images: [Image]) {  
  images.forEach { image in  
let hash = calculateHash(image.data) // Recalculate each loop
    saveToCache(hash: hash, image: image)  
  }  
}  

// Optimization: Calculate in advance and pass to closure
func processImages(images: [Image]) {  
  let hashes = images.map { calculateHash($0.data) }  
  images.zip(hashes).forEach { image, hash in  
saveToCache(hash: hash, image: image) // The closure uses pre-calculated results directly
  }  
}  
```  

### 4.2 Memory Management and Weak References
When closure captures class instances, use weak references to avoid circular references (assuming Cangjie supports the `weak` keyword):
```typescript  
class ViewModel {  
  private weak var view: UIView?  

  func loadData() {  
    networkRequest { [weak self] data in  
Self?.view?.render(data) // Weak reference ensures that the view can be released correctly
    }  
  }  
}  
```  


## 5. Summary: Applicable boundaries of functional closures
The integration of functional programming and closures is effective in the following scenarios:
- **Lightweight logic encapsulation**: such as data conversion, event callbacks, simple state management;
- **Declarative process control**: Implement data processing pipelines through flow operators and closure chains;
- **Dependence abstraction and testing**: Detailed implementation through closure isolation between architectural layers.
