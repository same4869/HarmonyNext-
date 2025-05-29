# HarmonyOS Next function advancement: parameter characteristics and calling mechanism
In the development of Cangjie language in HarmonyOS Next, the parameter characteristics and calling mechanism of the function are the key to building flexible and efficient code.As a technician who has been deeply engaged in this field for a long time, I will combine my actual project experience to deeply analyze the core points such as parameter default values, variable parameters, and evaluation strategies in the calling mechanism.

## 1. Parameter default value
### (I) Parameter design mode in UI component initialization
In UI component development, the rational use of parameter default values ​​can significantly improve the ease of use of the API.Take the button component as an example:
```cj
class Button {
    var text: String
    var backgroundColor: Color
    var textColor: Color
    var fontSize: Float

    init(
text: String = "click",
        backgroundColor: Color = Color.BLUE,
        textColor: Color = Color.WHITE,
        fontSize: Float = 16.0
    ) {
        this.text = text
        this.backgroundColor = backgroundColor
        this.textColor = textColor
        this.fontSize = fontSize
    }
}
```
In this design, the common properties of the button are set with reasonable default values.When a developer creates a button, he can only focus on the properties that need to be customized, such as:
```cj
let primaryButton = Button() // Use all default values
let cancelButton = Button(
text: "Cancel",
    backgroundColor: Color.RED
) // Only customize text and background colors
```
This design pattern follows the "minimum surprise principle" and lowers the threshold for using APIs.At the same time, through parameter grouping and logical sorting, the clear structure of the initialization parameters is maintained.In actual projects, this model is widely used in various UI components, such as TextField, Slider, etc., which greatly improves development efficiency.

### (II) Compilation-time parsing mechanism of parameter default values
From the perspective of compilation principles, the default value of the parameter will be converted to a specific bytecode instruction when compiling.When the function is called, if no value of a parameter is provided, the virtual machine will automatically insert the default value.For example:
```cj
func greet(name: String = "Guest") {
    println("Hello, \(name)!")
}

// Compiled pseudo-code
func greet(name: String) {
    let actualName = if (name == null) "Guest" else name
    println("Hello, \(actualName)!")
}
```
This mechanism ensures that the processing of default values ​​is transparent to developers while maintaining consistency in function calls.The compiler will perform strict type checks to ensure that the default value matches the parameter type.In complex generic scenarios, the type derivation of default values ​​needs to be carried out in conjunction with the context, which puts higher requirements on the compiler's type system.

## 2. Variable parameters
### (I) Flexible parameter processing in the log system
In log system development, variable parameters provide great flexibility.For example:
```cj
func log(level: LogLevel, message: String, args: Any...) {
    let formattedMessage = format(message, args)
    println("[${level}] ${formattedMessage}")
}

// Use example
log(.INFO, "System startup completed")
log(.ERROR, "file %s does not exist", filePath)
log(.DEBUG, "calculation result: %d + %d = %d", a, b, a + b)
```
In this log function, `args: Any...` represents a list of mutable parameters.This design allows log functions to accept different numbers and types of parameters to adapt to various log scenarios.In the internal implementation, the mutable parameters are converted into an array for processing:
```cj
func log(level: LogLevel, message: String, args: Array<Any>) {
// Implement code
}
```
This transformation is done automatically by the compiler, and developers do not need to manually process the creation of arrays.It should be noted that the mutable parameter must be the last parameter of the function to avoid parameter parsing ambiguity.

### (II) Performance optimization: Avoid excessive use of variable parameters
While variable parameters provide convenience, overuse can lead to performance problems.Each time a function with mutable parameters is called, a new array object is created.In high-performance scenarios, this overhead may become unnegligible.For example, in the core algorithm of high-frequency calls:
```cj
// Implementation with poor performance
func calculateSum(values: Int...) {
    var sum = 0
    for (value in values) {
        sum += value
    }
    return sum
}

// Optimized implementation
func calculateSum(values: Array<Int>) {
    var sum = 0
    for (value in values) {
        sum += value
    }
    return sum
}
```
The optimized version requires the caller to explicitly pass the array, avoiding the overhead of array creation on each call.In actual projects, we usually provide two API versions: a convenient version that uses variable parameters, and a high-performance version that uses arrays for different scenarios to choose from.

## 3. Evaluation strategy
### (I) Application of lazy evaluation in conditional judgment
Cangjie language adopts the eager evaluation strategy by default, but in some scenarios, lazy evaluation can bring significant advantages.For example, in conditional judgment:
```cj
func expensiveOperation(): Int {
println("Execute time-consuming operation...")
    return 42
}

// Instant evaluation
if (false && expensiveOperation() > 10) {
println("conditions satisfy")
}

// Lazy evaluation simulation
func lazyCondition(condition: () -> Bool) {
    if (condition()) {
println("conditions satisfy")
    }
}

lazyCondition { false && expensiveOperation() > 10 }
```
In the instant evaluation example, `expensiveOperation()` is still called even if the first condition is false.In lazy evaluation simulation, the code in the closure is executed only when the conditional result needs to be calculated.This strategy is especially useful in scenarios where conditional judgments depend on expensive calculations or may throw exceptions.

### (II) Performance trade-off between function currying and some applications
Function Currying is a technique of converting multi-parameter functions into a series of single-parameter functions.In Cangjie language, it can be implemented through closures:
```cj
func add(a: Int, b: Int) -> Int {
    return a + b
}

// Curry version
func curriedAdd(a: Int) -> (Int) -> Int {
    return { b in a + b }
}

// use
let add5 = curriedAdd(5)
println(add5(3)) // Output 8
```
The main advantage of Curryization is to improve the flexibility and reusability of the function.However, each currying creates a new closure object, which can bring additional memory overhead.In performance-sensitive scenarios, it is necessary to weigh the flexibility and performance costs brought by Currying.

In real projects, we usually use currying where we need to be highly abstract and reusable, while keeping the original form of the function in performance-critical code.For example, in UI event processing, Currying can conveniently bind contexts, but is rarely used in underlying algorithms.

Understanding the parameter characteristics and calling mechanism of functions can help developers write more efficient and expressive code.In the development of HarmonyOS Next, rational use of these features is an important foundation for building high-quality applications.
