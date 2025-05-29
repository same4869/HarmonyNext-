
# HarmonyOS Next closure practice: From variable capture rules to memory management optimization

> This article aims to deeply explore the technical details of Huawei HarmonyOS Next system and summarize them based on actual development practices.It is mainly used as a carrier of technology sharing and communication, and it is inevitable to miss mistakes. All colleagues are welcome to put forward valuable opinions and questions in order to make common progress.This article is original content, and any form of reprinting must indicate the source and original author.


## 1. Analysis of the core rules of "variable capture" of closures

In the Cangjie language of HarmonyOS Next, the behavior of closures is defined by strict variable capture rules.Understanding these rules is the basis for correct use of closures.

### 1.1 Capture type and scope relationship
Closures can only capture local variables** within the scope when defined (including function parameter defaults, outer function variables) and non-static member variables** of class ** instances. Access to global variables, static members, or function parameters is not considered to be captured.

| **Scenario** | **Does it belong to variable capture** | **Sample code** |
|------------------------------|--------------------|------------------------------------------|
| Lambda accesses the outer `let` variable inside the function | Yes | `func f() { let x=1; let g=()=>x; }` |
| Class member function accesses `this` member | No (implicitly pass `this`) | `class C { var x=0; func f() { println(this.x); } }` |
| Lambda access global variables | No | `var g=0; let f=()=>g;` |

### 1.2 Compilation period mandatory verification: visibility and initialization
- **Visibility**: The captured variable must be declared when the closure is defined, otherwise the compiler will report an error.
  ```typescript
  func errorCase() {
let f = () => y // Error: y is not defined
    let y = 10
  }
  ```
- **Initialization**: Variables need to be initialized before closure definition, and uninitialized variables cannot be captured.
  ```typescript
  func errorCase() {
var x: Int64 // Not initialized
let f = () => x // Error: x is not initialized
    x = 10
  }
  ```


## 2. The practice of "escape restriction" for variable variable capture

### 2.1 “First Class Citizen” permission restrictions
When the closure captures a mutable variable declared by `var`, the closure ** is prohibited as a first-class citizen** (cannot be assigned to the variable, as a parameter/return value), and only allows direct calls.

**Error Example: Trying to escape to capture `var`' closure**
```typescript
func badUsage() {
  var x = 1
func g() { x += 1 } // Capture var variable x
let closure = g // Error: Cannot assign value to variable
return g // Error: cannot be used as return value
}
```

**Correct example: Direct calls only**
```typescript
func correctUsage() {
  var x = 1
  func g() { x += 1 }
g() // Legal call
println(x) // Output: 2
}
```

### 2.2 "Rack of Reactions" of Transitive Capture
If function A calls function B that captures `var`, and the variables captured by B are not within the scope of A, A will also be restricted.

```typescript
// Violation: g captures outer var x, f calls g and x is not within f scope
func h() {
  var x = 1
func g() { x += 1 } // Capture x (belongs to the scope of h)
  func f() { g() }
return f // Error: f captures outer var variable x
}

// Compliance: g captures x in f scope, f does not capture other var variables
func h() {
  func f() {
    var x = 1
func g() { x += 1 } // Capture x (belongs to the scope of f)
    g()
  }
return f // legal
}
```


## 3. Capture differences between reference type and value type

### 3.1 Reference type (class): the security boundary of shared state
When a closure captures an instance of `class`, its variable members (such as `var num`) can be modified and the modification is visible to all references.

```typescript
class Counter {
  public var count = 0
}

func createCounter(): () -> Unit {
let c = Counter() // closure captures reference to c
  return () -> Unit {
c.count += 1 // Legal: Modify the reference type member
  }
}

let inc1 = createCounter()
inc1()
println(inc1.count) // Output: 1 (reference type shared state)
```

### 3.2 Value type (struct): copy semantic isolation
A copy is created when closure captures `struct`, and modifications within the closure do not affect the original variable.

```typescript
struct Point { var x: Int64 }

func createPoint(): () -> Point {
var p = Point(x: 0) // Closure captures a copy of p
  return () -> Point {
p.x += 1 // Modify the copy
    return p
  }
}

let movePoint = createPoint()
movePoint()
let original = Point(x: 0)
println(original.x) // Output: 0 (the original value has not changed)
```


## 4. Typical application scenarios of closures in Hongmeng development

### 4.1 Responsive component state management
Use closures to encapsulate the private state of components to avoid global pollution.

```typescript
@Entry
struct CounterComponent {
private counter = createCounterClosure() // closure management status

  build() {
    Column {
      Text("Count: ${counter()}")
      Button("Increment").onClick(counter)
    }
  }
}

// Closure factory function
func createCounterClosure(initial: Int64 = 0): () -> Int64 {
  var count = initial
  return () -> Int64 {
    count += 1
    return count
  }
}
```

### 4.2 Cache closures in high-performance computing
Capture cache objects with closures to avoid repeated calculations.

```typescript
func memoize<T: Equatable, U>(fn: (T) -> U): (T) -> U {
  var cache = [T: U]()
  return { x in
    if let value = cache[x] { return value }
    let result = fn(x)
    cache[x] = result
    return result
  }
}

// Use scenario: Fibonacci sequence cache
let fib = memoize { n in
  n <= 1 ? n : fib(n-1) + fib(n-2)
}
println(fib(10)) // First calculation
println(fib(10)) // Directly read cache
```


## 5. Memory management and performance optimization

### 5.1 Avoid circular references: explicitly disconnect closure references
When using closures in class member functions, weak references are held through local variables (assuming Cangjie supports the `weak` keyword).

```typescript
class ViewModel {
  private var data: String?
  func fetchData() {
let self = weak(this) // Weak reference avoids looping
    networkRequest {
self?.data = "Loaded" // Secure access instance
    }
  }
}
```

### 5.2 Compilation period optimization: using `const` closure
For closures that do not depend on runtime status, use the `const` keyword to force the compilation period calculation.

```typescript
const func compileTimeClosure() -> Int64 {
let x = 10 // Initialization during compilation
return () -> Int64 { x + 5 }() // Compile period calculation result 15
}

let result = compileTimeClosure() // Use the result directly at runtime
```


## 6. Guide to avoid pits: Common errors and solutions

| **Problem Scenario** | **Cause Analysis** | **Solution** |
|--------------------------|--------------------------------|-----------------------------------|
| The UI is not updated after the closure is modified with the `var` variable | Responsive framework update is not triggered | Use `@State` to modify the state variable or use class to manage the state instead |
| An error occurred during the compilation period "variable not initialized" | The closure definition is earlier than the variable initialization | Move the closure definition after variable initialization |
| Passing closures as parameters as errors in time type | Capture `var` variables lead to closure limitations | Use `let` instead to declare variables or extract state into the class |
| Reference type closure memory leak | Closure long-term holding instance references | Use weak references or limit closure life cycle |


## Conclusion: The "rule-first" development model of closures

In HarmonyOS Next development, the powerful ability of closures is built on strict adherence to rules.Developers need:
1. **Preferential use of `let` variable to capture**: Avoid escape restrictions brought by `var`;
2. **Clear scope boundaries**: Encapsulate closure logic through nested functions or class;
3. **Combined with the characteristics of the Hongmeng framework**: Use closures in ArkUI to achieve lightweight state management, and improve efficiency by caching closures in high-performance scenarios.

By integrating closure rules into architectural design, it can ensure code flexibility while avoiding potential runtime risks and fully unlock the development potential of HarmonyOS Next.
