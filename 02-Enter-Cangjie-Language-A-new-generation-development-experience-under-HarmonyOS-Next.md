# Enter Cangjie Language: A new generation development experience under HarmonyOS Next
As HarmonyOS Next gradually matures, developers have put forward higher requirements for programming languages ​​under the new ecosystem: they must not only develop efficiently, but also ensure performance and security, and can easily adapt to complex scenarios of smart terminals, edge computing and cloud collaboration.Against this background, Cangjie language (Cangjie) came into being.

As an engineer who actually participated in the development of HarmonyOS Next application, I deeply felt in the process of using Cangjie language that this is not just a simple language replacement, but a complete innovation from language design to development experience.In this article, I will combine practice, starting from language characteristics, paradigm support to basic grammar, to take you to truly understand the charm of Cangjie's language.

## Introduction to Cangjie Language and HarmonyOS Next Background
HarmonyOS Next focuses on the "full-scene intelligent ecosystem" and is no longer compatible with traditional Linux kernel applications (such as APK), but builds a new application ecosystem entirely based on self-developed kernels and unified compilation systems.Cangjie Language is tailor-made for this goal:
|Properties | Description |
|--|--|
|Multi-paradigm programming | Support functional, imperative, object-oriented paradigm fusion |
|Extreme performance optimization | Front-end IR optimization + Back-end instruction-level optimization + Runtime optimization |
|Strong security | Static type system + automatic memory management + runtime multiple checks |
|Concurrent friendly | Lightweight user-state thread + concurrent object library |
|Easy to use and extensibility | Rich syntactic sugar, type inference, type extension support |
|Advanced application development for all scenarios |Full coverage from mobile phones to IoT devices, from end to cloud |

In essence, Cangjie language is the default preferred language for HarmonyOS Next application development, with extremely high official support, and new features will be given priority to Cangjie's language system in the future.

## Multi-paradigm support for Cangjie Language: Really born for developers
In real projects, Cangjie made me feel the most intuitive: it does not stick to a single paradigm, but naturally integrates multiple programming styles, allowing us to freely choose the most appropriate expression according to the characteristics of the business.
### 1. Object-Oriented Programming (OOP)
Cangjie fully supports traditional class and interface models:
```
public open class Animal {
    public open func speak(): Unit {
        println("Animal speaks")
    }
}

public class Dog <: Animal {
    public override func speak(): Unit {
        println("Dog barks")
    }
}

main() {
    let a: Animal = Dog()
a.speak() // Dynamic dispatch, output "Dog barks"
}
```
- Support single inheritance and multi-interface implementation
- Control inheritance and rewrite permissions through open
- All types implicitly inherit Any, unify object model

Practical experience: It is very consistent with the design concept of modern programming languages ​​(such as Kotlin/Swift), reduces redundancy, and is safe by default.
### 2. Functional Programming (FP)
In Cangjie language, functions are "first-class citizens" and can be assigned, passed and returned freely:
```
let square = {x: Int => x * x}

func apply(f: (Int) -> Int, v: Int): Int {
    return f(v)
}

main() {
println(apply(square, 5)) // Output 25
}
```
- Supports Lambda expressions
- Supports higher-order functions and currying
- Built-in ** pattern matching (match-case) ** mechanism, greatly enhancing expression power

Practical experience: Cangjie's functional characteristics are so easy to handle in scenarios such as list operations, state machines, asynchronous orchestration.
### 3. Imperative programming
Of course, for most daily business logic, such as UI control and IO processing, traditional imperative programming is also inconsistent in Cangjie:
```
var total = 0
for (let i in 1..10) {
    total += i
}
println(total)
```
Practical experience: It can maintain a sense of familiarity without forcing developers to adapt to a certain "high-end" style, which is very friendly.

## Basic syntax of Cangjie language and the first Hello World example
If you have mastered modern languages ​​such as Swift and Kotlin, it will be very easy to get started with Cangjie language.It maintains conciseness and consistency in grammatical design without a lot of lengthy keywords and symbols.
|Features | Cangjie Language Examples |
|--|--|
|Variable definition|let a = 10 (immutable) var b = 20 (variable)|
|Func add(x: Int, y: Int): Int { return x + y }|
|Conditional Statement|if (a > b) { ... } else { ... }|
|Loop statement|for (let i in 0..10) { ... }|
|Class and Objects|class A { ... }let obj = A()|

The simplest Hello World program is as follows:
```
func main() {
    println("Hello, HarmonyOS Next!")
}
```
Note: Cangjie's main function is the default entry for the program, and cumbersome modifications such as public static void main are omitted.

A slightly more complete example:
```
public class Greeter {
    let message: String

    init(msg: String) {
        this.message = msg
    }

    public func greet(): Unit {
        println(this.message)
    }
}

main() {
    let greeter = Greeter("Welcome to HarmonyOS Next with Cangjie!")
    greeter.greet()
}
```
Output result:
Welcome to HarmonyOS Next with Cangjie!

## Summary
Cangjie language is not just developed for development, but behind it is a strategic layout of HarmonyOS Next for the future ecosystem.

Judging from my actual development experience, Cangjie is modern, simple and powerful, especially suitable for building intelligent applications for device collaboration and end-cloud collaboration.

Whether it is a small IoT application or a complex mobile terminal or a car computer system, Cangjie can find an excellent balance between development efficiency and execution performance.

Next step of exploration: Cangjie language type inference, generics, and concurrency models will be the key to determining development efficiency and the direction I plan to study in depth.
