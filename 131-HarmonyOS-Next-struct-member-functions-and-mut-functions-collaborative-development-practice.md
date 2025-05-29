
# HarmonyOS Next struct member functions and mut functions collaborative development practice

In HarmonyOS Next, the member function of `struct` is the core mechanism for manipulating instance data, and the `mut` function, as a special instance function, provides limited mutability for value types.This article is based on the document "0010 Creating a struct Example - Struct Type - Cangjie Programming Language Development Guide - Learning Cangjie Language.docx", and deeply analyzes the collaborative rules and practical scenarios between member functions and `mut` functions.


## 1. Classification and basic usage of member functions

### 1.1 Instance member function: operation instance status
Instance member functions access instance members through `this` and are divided into two categories: read-only functions and `mut` functions.

**Read-only function example**
```typescript  
struct Circle {  
  let radius: Float64  
  public func area(): Float64 {  
return 3.14159 * radius * radius // Read-only access instance members
  }  
}  
```  

**mut function example**
```typescript  
struct MutableCircle {  
  var radius: Float64  
  public mut func setRadius(newRadius: Float64) {  
radius = newRadius // Modify instance members to mut
  }  
}  
```  

### 1.2 Static member functions: type-level operations
Static member functions are called by type names and can only access static members, and cannot use `this`.

```typescript  
struct MathUtils {  
  static let PI = 3.14159  
  public static func calculateCircumference(radius: Float64) -> Float64 {  
return 2 * PI * radius // Access static members
  }  
}  
let circumference = MathUtils.calculateCircumference(radius: 5.0)  
```  


## 2. The core limitations and usage rules of mut function

### 2.1 Syntax requirements for mut function
- Mut keyword must be modified, otherwise the instance members cannot be modified.
- The `struct` instance declared by `let` prohibits calling the `mut` function.

**Error case**
```typescript  
struct Counter {  
  var count: Int64 = 0  
public func increment() { // Non-mut functions cannot modify instances
count += 1 // Error: Cannot modify value type members in non-mut functions
  }  
}  
```  

### 2.2 The special semantics of this
In the mut` function, `this` allows modifying instance members, but prohibits being captured by closures or used as expressions.

```typescript  
struct Foo {  
  var value: Int64 = 0  
  public mut func updateValue() {  
let closure = { this.value = 1 } // Error: This is not captured
value = 2 // Legal modification
  }  
}  
```  

### 2.3 Compatibility with interfaces
The `mut` function declared in the interface, the `mut` modifier must be retained when implementing the `struct`.

```typescript  
interface Updatable {  
  mut func update(value: Int64)  
}  
struct UpdatableStruct : Updatable {  
public mut func update(value: Int64) { /*...*/ } // Mut must be added
}  
```  


## 3. Collaborative development scenarios: from data operation to architectural design

### 3.1 Separation of data verification and status change
By checking the data by read-only function, the `mut` function performs changes to ensure the atomicity of the operation.

```typescript  
struct Account {  
  var balance: Float64  
// Read-only function: Check whether the balance is sufficient
  public func canWithdraw(amount: Float64) -> Bool {  
    return balance >= amount  
  }  
// mut function: execute deduction
  public mut func withdraw(amount: Float64) {  
    if canWithdraw(amount: amount) {  
      balance -= amount  
    }  
  }  
}  
var account = Account(balance: 1000.0)  
account.withdraw(amount: 200.0) // Legal operation, the balance becomes 800.0
```  

### 3.2 Batch operation and performance optimization
In scenarios where instances need to be modified multiple times, the `mut` function merge operation is used to reduce copy generation.

```typescript  
struct Matrix {  
  var data: [[Float64]]  
// mut function: matrix transposition
  public mut func transpose() {  
    data = data[0].indices.map { col in  
      data.map { $0[col] }  
    }  
  }  
// mut function: element scaling
  public mut func scale(factor: Float64) {  
    data = data.map { $0.map { $0 * factor } }  
  }  
}  
var matrix = Matrix(data: [[1, 2], [3, 4]])  
matrix.transpose().scale(factor: 2.0) // Chained call, modified in place
```  

### 3.3 State management of responsive components
In ArkUI, a responsive update of component state is implemented in combination with `@State` and `mut` functions.

```typescript  
@Entry  
struct CounterView {  
  @State private counter = CounterStruct()  
  build() {  
    Column {  
      Text("Count: \(counter.value)")  
      Button("Increment")  
        .onClick {  
counter.increment() // Call mut function to update the status
        }  
    }  
  }  
}  
struct CounterStruct {  
  var value: Int64 = 0  
  public mut func increment() {  
value += 1 // Modify triggers UI re-rendering
  }  
}  
```  


## 4. Common Errors and Best Practices

### 4.1 Non-mut functions call mut functions
Non-mut functions prohibit direct call to mut functions, and logic needs to be modified or reconstructed through instances.

**Counterexample**
```typescript  
struct DataProcessor {  
  var data: String  
  public func process() {  
cleanData() // Error: Non-mut functions call mut functions
  }  
  public mut func cleanData() {  
    data = data.trim()  
  }  
}  
```  

**Solution**
```typescript  
struct DataProcessor {  
  var data: String  
  public mut func process() {  
cleanData() // The mut function can call other mut functions
  }  
  public mut func cleanData() {  
    data = data.trim()  
  }  
}  
```  

### 4.2 Side effects of overuse of mut function
Avoid performing time-consuming operations or generating external dependencies in the mut function, and keep the function pure.

**Counterexample**
```typescript  
struct FileWriter {  
  public mut func write(data: String) {  
FileSystem.writeToDisk(path: "data.txt", data: data) // Time-consuming I/O operation
  }  
}  
```  

**Recommended practices**
```typescript  
struct FileWriter {  
  public func prepareData(data: String) -> String {  
// Data preprocessing (read-only operation)
    return data.compress()  
  }  
  public mut func write(preparedData: String) {  
FileSystem.writeToDisk(path: "data.txt", data: preparedData) // Focus on writing
  }  
}  
```  

### 4.3 Naming specifications for member functions
- Read-only functions are named with prefixes such as `get/has/is` (such as `getArea/hasPermission`).
- The `mut` function is named after verbs such as `set/update/modify` (such as `setSize/updateStatus`).

```typescript  
struct Sensor {  
public func getTemperature() -> Float64 { /*...*/ } // Read-only function
public mut func calibrate(offset: Float64) { /*...*/ } // mut function
}  
```  


## 5. Performance optimization and design principles

### 5.1 Avoid unnecessary copy generation
Use the `inout` modifier in function parameters to avoid the overhead of copying `struct` instances.

```typescript  
func processLargeStruct(inout data: LargeStruct) {  
data.updateValue() // Directly operate the original value to reduce copying
}  
var data = LargeStruct()  
processLargeStruct(inout: &data)  
```  

### 5.2 Compilation period optimization strategy
Encapsulate the unchanged logic into a static member function or a `const` modified `struct`, and use the compilation period to improve performance.

```typescript  
const struct FixedMath {  
  public static func multiply(a: Int64, b: Int64) -> Int64 {  
return a * b // Compilation period can be calculated
  }  
}  
```  

### 5.3 Separation of interface and implementation
Through the interface abstracting member functions, `struct` and `class` are implemented separately to improve code maintainability.

```typescript  
interface DataHandler {  
  func process(data: String) -> String  
  mut func reset()  
}  
struct StructHandler : DataHandler {  
  public func process(data: String) -> String { /*...*/ }  
  public mut func reset() { /*...*/ }  
}  
class ClassHandler : DataHandler {  
  public func process(data: String) -> String { /*...*/ }  
public func reset() { /*...*/ } // The class does not require mut modification
}  
```  


## Conclusion
The coordinated use of `struct` member functions and `mut` function reflects HarmonyOS Next's "safe and variable" design philosophy in value type operations.In development, the following principles must be followed:
1. **Separation of responsibilities**: Read-only logic is separated from mutable operations, improving code traceability through access control of member functions;
2. **Minimum mutable**: Use the `mut` function only when necessary, and implement immutable design by returning new instances first;
3. **Performance sensitivity**: For struct` instances of high-frequency operations, use the `inout` parameter or batch `mut` function to reduce overhead.

By rationally using these mechanisms, developers can build an efficient and secure data operation system in Hongmeng applications, especially in real-time data processing, embedded device control and other scenarios, to give full play to the performance advantages of value types.
