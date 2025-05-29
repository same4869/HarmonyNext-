# HarmonyOS Next conditional expression depth analysis: if and pattern matching
In the development of HarmonyOS Next, the conditional expressions of the Cangjie language are an important means to implement program logic branches.Among them, if expression and pattern matching mechanism complement each other, providing developers with powerful and flexible programming capabilities.As a technician with rich practical experience in this field, I will analyze this key knowledge point in depth below.

## 1. Basic if syntax
### (I) Strong type check vs. C language implicit conversion difference
The if expressions in Cangjie language have strict strong typing requirements in terms of conditional judgment, which is significantly different from the implicit conversion of C language.In C language, types such as integers, floating-point numbers, etc. can be implicitly converted to Boolean values, non-zero values ​​are usually regarded as true, and zero values ​​are regarded as false.For example in C language:
```c
int num = 5;
if (num) {
// The code block will be executed
}
```
In Cangjie language, the conditions of an if expression must be of a Boolean type, and implicit conversions are not allowed using integers or floating-point numbers.The following code will compile and report errors in Cangjie language:
```cj
main() {
    let number = 1
    if (number) { // Error, mismatched types
println("non-zero number")
    }
}
```
Although this strong type check increases the constraints when writing code to a certain extent, it can find type mismatch errors during the compilation stage, greatly improving the reliability and stability of the code.In large projects, this early error detection mechanism can avoid many potential runtime errors and reduce maintenance costs.

## 2. Multi-level conditional chain
### (I) Cosmic speed rating judgment code optimization skills
In actual development, we often encounter scenarios where multi-level conditional judgment is required.Taking the grading judgment of cosmic speed as an example, we can improve the readability and maintainability of the code by optimizing the structure of if expressions.
The original code might look like this:
```cj
import std.random.*
main() {
    let speed = Random().nextFloat64() * 20.0
    println("${speed} km/s")
    if (speed > 16.7) {
println("The third cosmic speed, meeting with the Magpie Bridge")
    } else {
        if (speed > 11.2) {
println("Second Universe Speed, Chang'e Flying to the Moon")
        } else {
            if (speed > 7.9) {
println("The first cosmic speed, flying into the clouds and fog")
            } else {
println("Down to the ground, look up at the stars")
            }
        }
    }
}
```
Although this nested if structure can implement functions, the code appears lengthy and poorly readable.We can use the else if form in Cangjie language to optimize:
```cj
import std.random.*
main() {
    let speed = Random().nextFloat64() * 20.0
    println("${speed} km/s")
    if (speed > 16.7) {
println("The third cosmic speed, meeting with the Magpie Bridge")
    } else if (speed > 11.2) {
println("Second Universe Speed, Chang'e Flying to the Moon")
    } else if (speed > 7.9) {
println("The first cosmic speed, flying into the clouds and fog")
    } else {
println("Down to the ground, look up at the stars")
    }
}
```
The optimized code logic is clearer, and each condition branch is clear at a glance, which facilitates subsequent modification and expansion.When writing multi-level conditional chains, using else if reasonably can make the code more concise and clear and improve development efficiency.

## 3. Type derivation mechanism
### (I) Example of automatic inference of minimum common parent type
The if expressions in Cangjie language have a unique mechanism in type derivation. When used as the initial value of variable definition, it will automatically infer that its type is the smallest common parent type of each branch code block type.For example:
```cj
main() {
    let zero: Int8 = 0
    let one: Int8 = 1
    let voltage = 5.0
    let bit = if (voltage < 2.5) {
        zero
    } else {
        one
    }
}
```
In this example, the two branch code block types of the if expression are Int8, so the type of the if expression is determined to be Int8, and the type of the variable bit is also derived as Int8.If the branch code block type is different, for example:
```cj
main() {
    let voltage = 5.0
    let result = if (voltage < 2.5) {
"Low Voltage"
    } else {
        1
    }
}
```
Since the type of "low voltage" is String and the type of 1 is Int, these two types do not have a common parent type, an error will be reported during compilation.Understanding this type derivation mechanism will help developers accurately grasp the types of variables when writing code and avoid type-related errors.In complex program logic, correctly using type derivation can reduce unnecessary type annotations and improve the simplicity and readability of the code.
