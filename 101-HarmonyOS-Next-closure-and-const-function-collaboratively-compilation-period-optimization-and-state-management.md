
# HarmonyOS Next closure and const function collaboratively: compilation period optimization and state management

> This article aims to deeply explore the technical details of Huawei HarmonyOS Next system and summarize them based on actual development practices.It is mainly used as a carrier of technology sharing and communication, and it is inevitable to miss mistakes. All colleagues are welcome to put forward valuable opinions and questions in order to make common progress.This article is original content, and any form of reprinting must indicate the source and original author.


## 1. The "compilation period-runtime" collaborative rules for closures and const functions
In Cangjie language, the combination of closure and `const` function can realize the hybrid programming mode of "compilation period pre-calculation + runtime dynamic scheduling".The `const` function ensures the compile-time determinism of the logic, while the closure provides runtime flexibility, which can optimize performance and improve type safety.

### 1.1 Closure capture restrictions for const function
The closure defined inside the `const` function can only capture the `const` variable or parameter, and prohibit the capture of the `var` variable or runtime state to ensure that the compilation period is evaluable.

**Legal example: Capture const variable**
```typescript  
const func compileTimeClosure() {  
const x = 10 // const variable
return { => x + 5 } // Closure captures const variable, evaluates the value during compilation
}  
  
let result = compileTimeClosure()() // The compilation period is calculated as 15
```  

**Error Example: Capture var variable**
```typescript  
const func errorCase() {  
var x = 10 // var variable, not captured during compilation
return { => x + 5 } // Error: Cannot capture var variable in const function
}  
```  

### 1.2 Scenario where closure calls const function
The closure can call the `const` function at runtime, using its pre-calculated results during compilation to improve operational efficiency.

```typescript  
const func add(a: Int64, b: Int64): Int64 {  
return a + b // It can be evaluated during the compilation period
}  
  
func createAdder(b: Int64) {  
return { a: Int64 => add(a, b) } // Closure captures b, and the const function is called at runtime
}  
  
let add5 = createAdder(5)  
println(add5(3)) // Output: 8 (call const function add when running)
```  


## 2. "Constant Evaluation" Practice of Compilation Period Closures
### 2.1 Static calculation of const closure
The closure is marked with the `const` keyword, and it is forced to complete the calculation during the compilation period. It is suitable for mathematical formulas, configuration parameters and other determination scenarios.

**Example: Pre-calculation of physical formulas**
```typescript  
const G = 6.67430e-11 // universal gravitational constant, compile period constant
const func calculateGravity(mass1: Float64, mass2: Float64, distance: Float64) {  
return { => G * mass1 * mass2 / (distance * distance) }() // Compile expressions
}  
  
// Determine the result during the compilation period and use it directly during the runtime
const gravity = calculateGravity(5.972e24, 70, 6.371e6)  
println(gravity) // Output: about 695.66 (consistent with the documentation example)
```  

### 2.2 Type safety of const closures
The parameters and return types of the `const` closure must meet the inference during the compilation period to avoid uncertainty caused by dynamic types.

```typescript  
const func identity<T>(x: T): T {  
return { => x }() // Generic const closure, infer type during compilation
}  
  
const intIdentity = identity<Int64>(10) // The type is determined to be Int64 during the compilation period
const stringIdentity = identity<String>("hello") // Determine the type as String during the compilation period
```  


## 3. Performance optimization of runtime closures and const functions
### 3.1 Mixed mode: Compilation period calculation + runtime parameters
The runtime parameters are captured by closures, combined with the compilation period logic of the `const` function, multiple reuses are realized.

**Example: Geometric Area Calculation**
```typescript  
const func baseArea(width: Int64): Int64 {  
return width * width // Calculate the base area during compilation
}  
  
func createAreaCalculator(height: Int64) {  
return { width: Int64 => baseArea(width) * height } // Closure captures the runtime height and calls the const function
}  
  
let calculateRectangleArea = createAreaCalculator(5)  
println(calculateRectangleArea(3)) // Output: 45 (3*3*5, baseArea is calculated as 9 during the compilation period)
```  

### 3.2 Avoid duplicate calculations: cache the results of the compile period
Using the memory effect of closures, cache the calculation results of the `const` function to reduce runtime overhead.

```typescript  
const func fibonacci(n: Int64): Int64 {  
  if n <= 1 { return n }  
return fibonacci(n-1) + fibonacci(n-2) // Recursive calculation during compilation
}  
  
func memoizeFib() {  
  var cache = [Int64: Int64]()  
  return { n: Int64 =>  
    if let value = cache[n] { return value }  
let result = fibonacci(n) // Call the const function, the result of the compilation period
    cache[n] = result  
    return result  
  }  
}  
  
let memoizedFib = memoizeFib()  
println(memoizedFib(10)) // First calculation, output 55
println(memoizedFib(10)) // Read cache, no additional calculations
```  


## 4. Constraints and avoid pits: The use boundary of const closures
### 4.1 Disable capture of runtime status
The `const` closure is strictly prohibited from capturing runtime variables (such as `@State`, function parameters), otherwise it will cause compilation failure.

**Error Example: Capture Runtime Parameters**
```typescript  
func runtimeParam(n: Int64) {  
  const func errorClosure() {  
return { => n + 5 } // Error: Capture runtime parameter n
  }  
}  
```  

### 4.2 Type constraints of generic const functions
The generic `const` function needs to ensure that the type parameters meet the compilation period to be evaluated (such as numeric types, enumerations) and avoid reference types or dynamic types.

```typescript  
const func genericConst<T: Number>(x: T): T {  
return { => x * 2 }() // Only Number subtypes are supported, and the compilation period can be calculated
}  
  
// Legal call
const double = genericConst<Int64>(10) // Compile period determines the numerical calculation
// Illegal call (String does not support arithmetic operations)
// const errorCase = genericConst<String>("hello")  
```  

### 4.3 Side effects limitations of const closure
Const` closure prohibits side-effect operations (such as I/O, modifying global status) to ensure purity during the compile period.

**Error Example: Printing during compilation**
```typescript  
const func sideEffectClosure() {  
return { => println("Compile time") } // Error: I/O operations are not allowed during the compilation period
}  
```  


## Conclusion: The "dual-track development" paradigm in compilation period and runtime
The coordination between closures and `const` function reflects HarmonyOS Next's dual pursuit of performance optimization and type safety:
- **Compilation period optimization**: Use the `const` closure to calculate and determine logic in advance to reduce runtime load;
- **Flexibility in runtime**: Use closures to capture dynamic parameters and adapt to business scenario changes.

In actual development, it is recommended to encapsulate the unchanged business logic (such as mathematical formulas and configuration rules) into a `const` closure, and dynamic logic is processed through ordinary closures to form an efficient development model of "static logic solidification during compilation period and dynamic logic flexible during running time".Through this division of labor, it can not only improve application performance, but also avoid runtime risks through compilation period verification, which is especially suitable for Hongmeng equipment development scenarios with high stability and efficiency requirements.
