
# HarmonyOS Next closures and variable capture in-depth analysis: scope rules and practical constraints

> This article aims to deeply explore the technical details of Huawei HarmonyOS Next system and summarize them based on actual development practices.It is mainly used as a carrier of technology sharing and communication, and it is inevitable to miss mistakes. All colleagues are welcome to put forward valuable opinions and questions in order to make common progress.This article is original content, and any form of reprinting must indicate the source and original author.


## 1. The essence of closure: "Spatial-time capsule" that captures variables and scope

In the Cangjie language of HarmonyOS Next, a closure is an entity composed of a function and the variables it captures.When a function or Lambda expression refers to variables outside the scope, the closure "remembers" these variables, which are accessible even if they are out of the scope.This feature is crucial in scenarios such as state management and callback functions, but it requires strict adherence to variable capture rules.


### 1.1 "Legal Boundaries" of Variable Capture
Closures can only capture variables of the following types, and other types will trigger compilation errors:
- **Function parameter default value**: Access local variables outside the function (non-function parameter).
- **Function/Lambda In-body**: Access local variables (including parent functions or global scopes) of outer scope.
- **Class/Structure Non-Member Function**: Access instance member variables through `this` (need to be in non-member functions).

**Legal capture example**
```typescript
func outer() {
let outerVar = 10 // external local variable
  func inner() {
println(outerVar) // Legal: Capture external local variables
  }
  inner()
}
```

### 1.2 Uncaught "Notification Zone"
The following scenarios do not constitute variable capture, and are parsed as normal variables during access:
- **Local variables within the function**: Variables defined in the closure cannot be reverse captured.
- **Function parameter**: The parameter is regarded as a variable within the function and does not belong to the capture category.
- **Global/static member variable**: Direct access, no triggering of capture logic (considered as global scope).

**Counterexample: Illegal capture scenario**
```typescript
var globalVar = 0 // Global variable
func f() {
let param: Int64 = 10 // Function parameters
let closure = { => param + globalVar } // No param (formal parameters), directly access globalVar (global variable)
}
```


## 2. "Compilation period verification" of variable capture: visibility and initialization

### 2.1 Visibility Rules: Variables must be "defined first and then captured"
When closure is defined, the captured variable must be declared within the scope, otherwise an error will be reported in the compiler.

**Example: Undefined variable capture error**
```typescript
func errorExample() {
  func closure() {
println(undefinedVar) // Error: undefinedVar is not defined
  }
let y = 20 // y is declared after closure is defined, and cannot be captured
  closure()
}
```

### 2.2 Initialization rules: variables must be "assigned first and then used"
The captured variable must be initialized when the closure is defined, avoiding the use of unassigned "dangling references".

**Example: Uninitialized variable capture error**
```typescript
func initError() {
var uninitVar: Int64 // Not initialized
  func closure() {
println(uninitVar) // Error: uninitVar is not initialized
  }
uninitVar = 10 // After initialization, an error still reported
  closure()
}
```


## 3. Capture differences between reference type and value type

### 3.1 Reference type (class): "Pointer semantics" of shared state
When a closure captures a `class` instance, the instance reference is stored, and the modifications to instance members inside and outside the closure will take effect synchronously.

**Example: Reference type capture and state sharing**
```typescript
class Counter {
  public var count = 0
}

func createCounter(): () -> Unit {
let counter = Counter() // closure captures counter reference
  return () -> Unit {
counter.count += 1 // Modify instance members
    println("Count: \(counter.count)")
  }
}

let counter1 = createCounter()
counter1() // Output: Count: 1
counter1() // Output: Count: 2
```

### 3.2 Value type (struct): "isolation" of copy semantics
When a closure captures a `struct` instance, a copy of the value is created, and modifications within the closure will not affect the original variable.

**Example: Value type capture and state isolation**
```typescript
struct Point {
  var x: Int64, y: Int64
}

func createPointClosure(point: Point): () -> Point {
var copiedPoint = point // Closure captures copy value
  return () -> Point {
copiedPoint.x += 1 // Modify the copy value
    return copiedPoint
  }
}

let original = Point(x: 0, y: 0)
let closure = createPointClosure(original)
println(closure()) // Output: Point(x: 1, y: 0)
println(original.x) // Output: 0 (the original value has not changed)
```


## 4. "Escape Limit" of Var: "Yester" of Closure

### 4.1 Core rules for escape restrictions
When the closure captures a mutable variable declared by `var`, the closure ** is prohibited as a first-class citizen** (cannot be assigned to a variable, passed as a parameter/return value), and only allows direct calls.

**Example: Limits of variable capture**
```typescript
func restrictedClosure() {
  var temp = 10
  func closure() {
temp += 1 // Legal: Capture variables
  }
  
// Error: Closure cannot be assigned to variables
  // let c = closure  
// Error: Closure cannot be used as return value
  // return closure  
// Correct: Call directly
  closure() 
}
```

### 4.2 Transitive Capture: "Chain Limitation" of the Ripple Effect
If function A calls function B that captures the `var` variable, and the variable captured by B is not within the scope of A, then A will also be regarded as capturing `var` and is subject to escape restrictions.

**Example: Limits caused by transitive capture**
```typescript
func outer() {
  var x = 10
func middle() { x += 1 } // Capture the outer var variable x
  func inner() {
middle() // inner calls middle to capture x (belongs to the outer scope)
  }
return inner // Legal: x is within the outer scope, inner does not directly capture the var variable
}
```


## 5. Practical scenario: Correct usage paradigm for closures

### 5.1 State Encapsulation: Closure Implementation of Counter Components
Use closures to capture immutable variables (or `class` instances) declared by `let` to achieve thread-safe state management.

```typescript
func createCounter(initialValue: Int64 = 0): () -> Int64 {
var count = initialValue // Closure captures mutable variables, but ensures safety by restricting closure escape
  return () -> Int64 {
    count += 1
    return count
  }
}

@Entry
struct CounterApp {
  private increment = createCounter()

  build() {
    Column {
      Text("Count: \(increment())")
      Button("Click").onClick(increment)
    }
  }
}
```

### 5.2 Callback function: Avoid variable variable escape
In asynchronous callbacks, if you need to capture mutable variables, you can limit the closure life cycle through local scope.

```typescript
func fetchData(callback: () -> Unit) {
  var data: String?
  networkRequest {
data = "Loaded data" // Closure capture data (local variable)
    callback()
  }
}

// Safe call: The closure is within the scope of fetchData and has not escaped
fetchData {
  if let d = data {
    println(d)
  }
}
```


## 6. Performance and Security: "Best Practices" of Closures

### 6.1 Priority to use immutable variables (lets)
Closures that capture `let` variables have no escape restrictions and can be freely used as a first-class citizen to improve code flexibility.

**Recommended writing method**
```typescript
func safeClosure() {
let stableVar = 10 // Immutable variable, closure can escape
  func closure() {
    println(stableVar)
  }
return closure // Legal
}
```

### 6.2 Avoid circular references
When the closure captures `this` (class instance), memory leaks need to be avoided through weak reference or scope isolation (assuming Cangjie supports weak reference syntax).

```typescript
class ViewModel {
  func loadData() {
let self = weak(this) // Weak reference avoids looping
    networkCall {
self?.updateUI() // Secure access instance
    }
  }
}
```


## Conclusion: The closure's "Double-edged Sword" philosophy and Hongmeng development practice

Closures are a powerful abstract tool in HarmonyOS Next, and their core value is to implement state encapsulation through variable capture, but excessive use of mutable variable capture can cause code to be uncontrollable.The following principles must be followed in development:
1. **Minimum capture principle**: Only necessary variables are captured, and `let` is preferred rather than `var`;
2. **Scope isolation**: Complex logic is encapsulated by class or module to avoid excessive closure expansion;
3. **Compilation period check**: Use the compiler to strictly check the capture rules to expose potential problems in advance.

By deeply understanding the working mechanism and constraints of closures, developers can write safer and more efficient code in Hongmeng applications, giving full play to the functional programming advantages of Cangjie language.
