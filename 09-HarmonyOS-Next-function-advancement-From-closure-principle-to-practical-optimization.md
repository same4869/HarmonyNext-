
# HarmonyOS Next function advancement: From closure principle to practical optimization

> This article aims to deeply explore the technical details of Huawei HarmonyOS Next system and summarize them based on actual development practices.It is mainly used as a carrier of technology sharing and communication, and it is inevitable to miss mistakes. All colleagues are welcome to put forward valuable opinions and questions in order to make common progress.This article is original content, and any form of reprinting must indicate the source and original author.


## 1. The "variable capture" mechanism of closures: more than scope penetration

In the Cangjie language of HarmonyOS Next, closures are the "space-time capsule" that connect functions and scopes.When a function or Lambda captures variables with an external scope, references to variables can be retained even if they are out of the original scope.This feature is crucial in scenarios such as state management and callback functions, but it also hides traps.

### 1.1 "Whitelist" and "Blacklist" for Capture Rules
Closure variable capture needs to meet strict rules, and the following table can clearly distinguish between legal and illegal scenarios:

| **Legal capture scenario** | **Illegal capture scenario** |
|------------------------------|------------------------------|
| The default value of the function parameter refers to external local variables | Access local variables defined in the function |
| References of external local variables within Lambda | Accessing function parameters (considered as variables within function) |
| Non-member function access class instance member variables | Access global or static member variables (considered as global scope) |
| Accessing instance members through `this` (within member functions) | Accessing members through `this` within member functions (not considered capture) |

**Example: Legal closure capture**
```typescript
func counterFactory(): () -> Int64 {
var count = 0 // Variable local variable captured by closure
  return () -> Int64 {
    count += 1
    return count
  }
}

// Use scenario: Button click counter
main() {
  let clickCounter = counterFactory()
  Button("Click") {
    onClick() {
println("Count: ${clickCounter()}") // Each click output increments the value
    }
  }
}
```

### 1.2 Verification of "visibility" and "initialization" during the compilation period
When closure is defined, the compiler will strictly check the visibility and initialization status of the captured variable:
- **Visibility**: The variable must exist within the scope when the closure is defined, otherwise the compilation error will be reported (such as `y` undefined in Example 2).
- **Initialization**: The variable needs to be initialized, avoid using unassigned "dangled references" (such as the uninitialized `x` in Example 3).

**Counterexample: Error reporting scenario during compilation**
```typescript
func badClosureExample() {
  func useUndefinedVar() {
println(undefinedVar) // Error: Variable is not defined
  }
var uninitializedVar: Int64 // Not initialized
  func useUninitializedVar() {
println(uninitializedVar) // Error: Variable not initialized
  }
}
```


## 2. "Escape Limit" of Variable Variables: "Shackles" and "Freedom" of Closures

In HarmonyOS Next development, the capture of mutable variables declared by `var` is required to be extra cautious.To avoid memory leaks and uncontrollable state changes, Cangjie Language imposes "escape restrictions" on closures that capture `var` - such closures can only be called as "one-time tools" and are prohibited from being first-class citizens (such as assigned to variables and passed as parameters).

### 2.1 Technical implementation of escape restrictions
When the closure captures the `var` variable, the compiler marks it as a "restricted closure".All of the following operations will trigger a compilation error:
- **Assign to variable**: `let closureVar = capturedVarClosure` ❌
- **As function parameter/return value**: `func takeClosure(closure: () -> Unit)` Pass this closure ❌
- **Use directly as an expression**: `return capturedVarClosure` ❌

**Example: Correct and incorrect usage of restricted closures**
```typescript
func buildRestrictedClosure() {
  var temp = 10
  func restrictedClosure() {
temp += 1 // Legal: Capture variables
    println(temp)
  }
  
// Error: Try to assign closure to variable
  // let closure = restrictedClosure  
// Correct: Only direct calls are allowed
restrictedClosure() // Output: 11
}
```

### 2.2 Capture Transmission: "Ripple Effect" and Scope Chain
Closures are transitive: if the function `A` calls the function `B` that captures the `var` variable, and the variable captured by `B` is not within the scope of `A`, then `A` is also considered to capture the `var` variable, thus being subject to escape restrictions.

**Case: Limits caused by transitive capture**
```typescript
var globalMutable = 0 // Global variable (non-captured scenario)

func outerFunc() {
  var outerVar = 5
  func middleClosure() {
outerVar += 1 // Capture outerVar (belongs to the outerFunc scope)
  }
  
  func innerFunc() {
middleClosure() // Call to capture outerVar closure
// Because outerVar is defined within the innerFunc scope, innerFunc is not subject to escape restrictions
  }
  
return innerFunc // Legal: innerFunc does not capture external var variable
}
```


## 3. Practical scenarios and optimization strategies for closures in HarmonyOS Next

### 3.1 Responsive Component State Management
In ArkUI development, closures can be used to encapsulate the private state of components to avoid global state pollution.For example, implement a button component with counting function:

```typescript
@Entry
struct CounterComponent {
  private countClosure: () -> Int64 = {
    var count = 0
    return () -> Int64 {
      count += 1
      return count
    }()
  }()

  build() {
    Column() {
Text("Number of clicks: ${this.countClosure()}")
        .fontSize(18)
Button("+ click")
        .onClick(() => {
this.countClosure() // The internal state of the closure is increased automatically
        })
    }
  }
}
```

### 3.2 Closure Optimization in High Performance Computing
In computing logic that requires frequent calls, rational use of the "memory effect" of closures can improve performance.For example, pre-calculate the graph transform matrix:

```typescript
func createTransformMatrix(scale: Float64, angle: Float64): () -> Matrix4x4 {
// Closure captures scaling and angle parameters, returns the transformation matrix generation function
  let cosAngle = cos(angle)
  let sinAngle = sin(angle)
  return () -> Matrix4x4 {
    Matrix4x4(
      scale * cosAngle, -scale * sinAngle, 0, 0,
      scale * sinAngle, scale * cosAngle, 0, 0,
      0, 0, 1, 0,
      0, 0, 0, 1
    )
  }
}

// Scene: Quickly obtain the transformation matrix when an animation frame is updated
let transform = createTransformMatrix(1.5, Math.PI/4)
for (let frame in 0..<100) {
let matrix = transform() // directly use closure cache calculation results
  render(matrix)
}
```

### 3.3 Closure adaptation with Java interoperability
In HarmonyOS Next, when bridging a Java callback interface through closures, you need to pay attention to variable capture rules.For example, pass the Cangjie closure as `Runnable` to the Java layer:

```typescript
// Java interface
public interface Callback {
  void onResult(String data);
}

// Cangjie code
func callJavaWithClosure() {
  var resultData = "Initial"
// Closure captures mutable variables and requires local scope to avoid escape restrictions
  {
    let localVar = resultData
    JavaCallback.invoke((data: String) => {
resultData = data // Legal: the localVar captured by the closure is of type let (immutable reference)
    })
  }
}
```


## 4. Pit avoidance guide: FAQs and solutions for closures

| **Problem Scenario** | **Cause Analysis** | **Solution** |
|--------------------------|--------------------------------|-----------------------------------|
| The interface is not updated after the closure is modified with `var` variable | Status notifications for responsive frameworks are not triggered | Use `@State` or `@Link` to modify the state variable |
| An error occurred during the compilation period "Variable not initialized" | Variable not assigned during the closure definition | Move the closure definition after variable initialization |
| Passing closures as parameters Times type mismatch | Capture closures for `var` variables that violate escape restrictions | Use `let` instead to declare variables or extract state into class instance |
| Using closures in a loop causes all instances to share state | Closures capture the same reference to loop variables | Create a new closure scope inside the loop body (such as using the execution function immediately) |


## Conclusion: The "double-edged sword" attribute and architecture balance of closures
Closures are both flexible "Swiss Army Knife" and "double-edged sword" that need to be treated with caution.Rationally utilizing its variable capture mechanism can achieve elegant state encapsulation and logic multiplexing, but excessive use of mutable variable capture may lead to a decrease in code maintainability.It is recommended to follow the following principles in architectural design:
1. Priority is given to using `let` to declare captured variables to avoid uncontrollable state changes;
2. In complex state management scenarios, combine the `class` or `ViewModel` mode to replace the pure closure solution;
3. In performance-sensitive scenarios (such as high-frequency animations, computing-intensive tasks), optimize the calculation path using the cache characteristics of closures.

By deeply understanding the underlying rules of closures and the adaptation strategy of HarmonyOS Next, developers can ensure the stability and scalability of the system while maintaining code simplicity.
