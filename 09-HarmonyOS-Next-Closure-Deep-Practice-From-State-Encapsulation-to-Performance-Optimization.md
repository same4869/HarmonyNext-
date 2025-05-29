
# HarmonyOS Next Closure Deep Practice: From State Encapsulation to Performance Optimization

> This article aims to deeply explore the technical details of Huawei HarmonyOS Next system and summarize them based on actual development practices.It is mainly used as a carrier of technology sharing and communication, and it is inevitable to miss mistakes. All colleagues are welcome to put forward valuable opinions and questions in order to make common progress.This article is original content, and any form of reprinting must indicate the source and original author.


## 1. The "state container" role of closure: life cycle management beyond the scope of function

In the Cangjie language of HarmonyOS Next, closures become natural state containers through the "variable capture" mechanism.When a closure captures variables in an external scope, the life cycle of these variables will be bound to the closure, and the closure can still maintain its state even if the original scope is destroyed.This feature is crucial in scenarios where the result of the last execution is required.

### 1.1 Counter Scenario: Closure Encapsulates Private State
Capturing mutable variables (`var`) through closures can achieve more encapsulated state management and avoid global variable pollution.Here is a typical counter closure implementation:

```typescript
func createCounter(initialValue: Int64 = 0): () -> Int64 {
var count = initialValue // Private state captured by closure
  return () -> Int64 {
count += 1 // Each call increases automatically
    return count
  }
}

// Example of usage: Binding closures in ArkUI
@Entry
struct CounterApp {
  private counter = createCounter()

  build() {
    Column {
      Text("Current Count: ${counter()}")
        .fontSize(24)
      Button("Increment")
.onClick(() => counter()) // Click to trigger closure status update
    }
  }
}
```

### 1.2 Cache Scenario: "Memory Effect" of Closures
Using the feature that variables captured by closures are not released with the end of the call, simple calculation results can be cached and repeated calculations can be avoided.For example, pre-calculate the Fibonacci sequence:

```typescript
func fibonacciCache(): (Int64) -> Int64 {
var cache = [Int64: Int64]() // Closure captures cache object
  return (n: Int64) -> Int64 {
    if cache.containsKey(n) {
      return cache[n]!
    }
    let result = n <= 1 ? n : fibonacciCache(n-1) + fibonacciCache(n-2)
cache[n] = result // cache the result
    return result
  }
}

// Performance optimization: After the first calculation, the subsequent calls directly read the cache
let fib = fibonacciCache()
println(fib(10)) // First calculation, output 55
println(fib(10)) // Directly read the cache, no duplicate calculations
```


## 2. The boundary of the "capture rules" of the closure: from the compilation period to the runtime limit

### 2.1 Variable visibility and initialization: Strict constraints during compilation
When closure definition is defined, the compiler will force the visibility and initialization status of the captured variable to avoid "dangling references".Here are two typical error scenarios:

#### Scenario 1: Capture undefined variables
```typescript
func scopeErrorExample() {
  func innerFunc() {
println(undefinedVar) // Error: Variable undefinedVar undefined
  }
// UndefinedVar is not within scope when closure is defined
  let closure = innerFunc
}
```

#### Scenario 2: Capture uninitialized variables
```typescript
func initErrorExample() {
var uninitializedVar: Int64 // Not initialized
  func innerFunc() {
println(uninitializedVar) // Error: Variable not initialized
  }
let closure = innerFunc // Error during compilation
}
```

### 2.2 Escape limits for mutable variables: security policies at runtime
To prevent closures from escaping from carrying mutable variables (`var`) from escaping from the scope, Cangjie Language imposes the following restrictions on closures that capture `var`:
- **Not as a first-class citizen**: Cannot assign values ​​to variables, as function parameters or return values.
- **Only allow direct calls**: It can only be called immediately within the defined scope and cannot be passed across scopes.

**Example: Error usage of violation of escape restrictions**
```typescript
func varEscapeError() {
  var temp = 10
  func escapeClosure() {
temp += 1 // Legal: Capture variables
  }
  
// Error: Try to assign closure to variable
  // let closureVar = escapeClosure  
// Error: Try to pass the closure as a function parameter
  // otherFunc(escapeClosure)  
// Correct: Only direct calls are allowed
  escapeClosure() 
}
```


## 3. Interaction between closures and reference types: Cross-scope management of object state

### 3.1 Variable state capture of class instances
When the closure captures a `class` instance (reference type), its mutable member variable can be modified directly, and the modification will be reflected in all places where the instance is referenced.This feature is suitable for scenarios where shared state is required.

```typescript
class CounterClass {
  public var count: Int64 = 0
}

func createClassCounter(): () -> Unit {
let counter = CounterClass() // Closure capture class instance
  return () -> Unit {
counter.count += 1 // Modify instance members
    println("Class Counter: \(counter.count)")
  }
}

// Example of usage: Multiple closures share the same instance state
let counter1 = createClassCounter()
let counter2 = createClassCounter() // New closure, new instance
counter1() // 输出：Class Counter: 1
counter1() // Output: Class Counter: 2
counter2() // Output: Class Counter: 1 (independent instance)
```

### 3.2 Capture properties of structure value type
Unlike classes, a copy is created when a `struct` (value type) is captured by a closure, and modifications within the closure will not affect the original variable.This feature can be used for isolating state changes.

```typescript
struct Point {
  var x: Int64, y: Int64
}

func createValueClosure(point: Point): () -> Point {
var copiedPoint = point // Closure captures the value type copy
  return () -> Point {
copiedPoint.x += 1 // Modify the copy
    return copiedPoint
  }
}

// Example of usage: The original value is not affected by closure
let originalPoint = Point(x: 0, y: 0)
let closure = createValueClosure(originalPoint)
println(closure()) // Output: Point(x: 1, y: 0)
println(originalPoint.x) // Output: 0 (the original value has not changed)
```


## 4. Performance optimization strategy for closures: Avoid memory leaks and redundant computing

### 4.1 Prevention of circular references: explicitly disconnecting closure references
When closures capture `this` (class instance), beware of memory leaks caused by circular references.It can be avoided by:
- **Weak reference**: Use the `weak` keyword to modify the captured instance (if Cangjie supports it).
- **作用域限制**：将闭包定义在临时作用域内，避免长期持有引用。

**Example: Temporary scope avoids circular references**
```typescript
class ViewModel {
  func fetchData(completion: () -> Unit) {
// Declare temporary variables to hold this outside the closure
    let self = this
    networkRequest {
self.processResult() // Use temporary variables to avoid circular references
      completion()
    }
  }
}
```

### 4.2 编译期优化：利用 const 闭包减少运行时计算
For closures that do not depend on runtime status, you can use the `const` keyword tag to force the calculation to be completed during the compilation period to improve performance.

```typescript
const func compileTimeClosure(): Int64 {
let compileTimeVar = 10 // Initialization during compilation
  return () -> Int64 {
compileTimeVar + 5 // Compile period calculation result
  }()
}

// Use the compiled results directly at runtime
let result = compileTimeClosure() // Result: 15 (Compilation period has been calculated)
```


## 5. Practical case: Composite application of closures in Hongmeng UI components

### 5.1 Reusable Form Verification Component
The form component that dynamically generates verification rules is realized through closure encapsulation verification logic:

```typescript
@Component
struct ValidatedInput {
  private value: string
  private validator: (string) -> bool

  init(initialValue: string, validator: (string) -> bool) {
    this.value = initialValue
this.validator = validator // Closure capture verification function
  }

  build() {
    Column {
      TextInput({ value: $value })
        .onChange((newValue) => {
          this.value = newValue
        })
      if !this.validator(this.value) {
        Text("Invalid input").fontColor(Color.Red)
      }
    }
  }
}

// Example of usage: Dynamically generate mailbox verification closure
let emailValidator = (value: string) => {
  let pattern = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/
  return pattern.test(value)
}

@Entry
struct FormApp {
  build() {
    ValidatedInput(initialValue: "", validator: emailValidator)
  }
}
```

### 5.2 动画状态机：闭包管理帧更新逻辑
Use closures to capture animation parameters to achieve complex animation effect control:

```typescript
func createAnimation(
  duration: number,
  callback: (progress: number) -> void
): () -> void {
  var startTime: number?
  return () -> void {
    if !startTime {
startTime = Date.now() // The first call record start time
    }
    let elapsed = (Date.now() - startTime!) / duration
    let progress = Math.min(elapsed, 1)
callback(progress) // Pass the progress of animation
    if progress < 1 {
requestAnimationFrame(createAnimation(duration, callback)) // Recursive call
    }
  }
}

// Example of usage: Start animation in ArkUI
@Entry
struct AnimationDemo {
  @State private progress: number = 0

  build() {
    Column {
      Rectangle()
        .width(100 * this.progress)
        .height(50)
        .backgroundColor(Color.Blue)
    }
    .onAppear(() => {
      let animation = createAnimation(1000) { p in
        this.progress = p // 闭包捕获 @State 变量，触发 UI 更新
      }
animation() // Start animation
    })
  }
}
```


## Conclusion: The "Design Philosophy" of Closures and the Best Practices for Hongmeng Development

Closures play the dual role of "lightweight state manager" and "logical wrapper" in HarmonyOS Next development.Using its features rationally can significantly improve the modularity of the code, but always pay attention to:
1. **Life cycle of variable capture**: Avoid unnecessary long-life cycle references causing memory leakage;
2. **Border of use of variable variables**: Use `let` first to declare the captured variable, and strictly restrict closure escape when it is necessary to do `var`;
3. **与引用类型的交互模式**：区分`class`与`struct`的捕获语义，选择合适的数据结构。

By combining closures with Hongmeng's responsive framework and component architecture, developers can build high-performance and easy-to-maintain applications in a more concise way, fully unleashing the development potential of HarmonyOS Next.
