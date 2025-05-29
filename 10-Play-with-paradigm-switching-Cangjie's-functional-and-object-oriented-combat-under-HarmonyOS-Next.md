# Play with paradigm switching: Cangjie's functional and object-oriented combat under HarmonyOS Next
If the powerful type system and type inference have laid a solid foundation for Cangjie language, then its flexible integration in multi-paradigm programming has truly given developers great freedom and creativity.

In HarmonyOS Next application development, I personally experienced: whether it is complex business modeling, concurrent processing, or data flow, as long as the functional and object-oriented paradigms are switched reasonably, Cangjie can always express clear and efficient logic in the most elegant way.

In this article, let me take you to explore: how to play with different programming paradigms in Cangjie and master the best practices in actual development.

## Functional programming: a concise tool for expressing business logic
In Cangjie, the function is "first-class citizen".This means:
1. Functions can be assigned, passed, and returned like ordinary variables.
2. Supports higher-order functions, lambda expressions, and currying.
3. Rich pattern matching (match-case) greatly simplifies conditional branches.

### Practical Example: Advanced Functions + Lambda
Suppose we need to process an array of integers, find all even numbers and square them.The implementation of Cangjie's functional style is very natural:
```
func isEven(x: Int): Bool {
    x % 2 == 0
}

func square(x: Int): Int {
    x * x
}

main() {
    let nums = [1, 2, 3, 4, 5, 6]

    let result = nums
       .filter(isEven)
       .map(square)

    println(result) // [4, 16, 36]
}
```
1. `filter` and `map` are commonly used higher-order functions.
2. Lambda expressions can be further simplified:
```
let result = nums
   .filter({ it => it % 2 == 0 })
   .map({ it => it * it })
```
Practical experience: Cangjie's functional programming syntax is very consistent with the natural expression of business logic, and the code is not only concise, but also highly readable.

## Object-Oriented Programming: The cornerstone of modeling complex systems
Although Cangjie has strong support for functional forms, its object-oriented (OOP) capabilities are equally solid, especially in the following scenarios:
1. Complex business modeling (such as orders, payments, logistics systems)
2. Interface component encapsulation (UI controls, interactive logic)
3. Cross-module communication (service interface, protocol definition)

### Cangjie OOP core features summary table
|Features | Description |
|--|--|
|Single inheritance|A class can only have one parent class|
|Multi-interface implementation | A class can implement multiple interfaces |
|open modifier | Control whether the class or method can be inherited/rewrited|
|All classes inherit Any|Ensure the unification of the basic object model|

### Practical examples: classes, interfaces and polymorphisms
```
public interface Shape {
    func area(): Float64
}

public class Circle <: Shape {
    let radius: Float64

    init(r: Float64) {
        this.radius = r
    }

    public func area(): Float64 {
        3.1415 * radius * radius
    }
}

public class Rectangle <: Shape {
    let width: Float64
    let height: Float64

    init(w: Float64, h: Float64) {
        this.width = w
        this.height = h
    }

    public func area(): Float64 {
        width * height
    }
}

main() {
    let shapes: Array = [Circle(3.0), Rectangle(4.0, 5.0)]

    for (let shape in shapes) {
        println(shape.area())
    }
}
```
Output:
```
28.2735
20.0
```
1. `Shape` is an interface that defines common behavior.
2. `Circle` and `Rectangle` respectively implement specific logic.
3. Implement polymorphic calls through the interface array `Array<Shape>`.

Practical experience: Cangjie's OOP model is clean and concise, without the problem of complex and multiple inheritance, and can meet most object-oriented needs, which is very suitable for large-scale system modeling.

## Hybrid paradigm practice: free switching, easy to handle
In real projects, we often need a combination of functional + object-oriented.

For example: In a chat application, the `MessageProcessor` class may be organized in an object-oriented manner, while the internal specific processing logic uses functional style combinations.
```
public class MessageProcessor {
    public func process(messages: Array): Array {
        messages
           .filter({ msg => msg != "" })
           .map({ msg => msg.trim() })
           .map({ msg => "Processed: " + msg })
    }
}

main() {
    let rawMessages = [" Hello ", "", "World "]
    let processor = MessageProcessor()
    let cleanMessages = processor.process(rawMessages)

    println(cleanMessages)
}
```
Output:
```
["Processed: Hello", "Processed: World"]
```
1. The overall processing process of class encapsulation.
2. Use `filter` + `map` advanced function internally to quickly process collections.

This mixed paradigm is extremely natural in Cangjie, and the development experience is very smooth and there is no sense of separation.

## Summary
In HarmonyOS Next development, the multi-paradigm feature of the Cangjie language is not a gimmick, but a real productivity tool.
|Scenarios | Recommended Paradigm | Reasons |
|--|--|--|
|Collection operation|Functional|Simple, high abstract|
|Flow control | Imperative | Simple and intuitive |
|Business Modeling|Object Orientation|Clear Structure|
|Complex system architecture | Hybrid paradigm | Flexible and efficient |

My practical experience tells me: developers who know how to flexibly switch paradigms can complete complex tasks faster and higher quality.And Cangjie was born for this flexibility.
