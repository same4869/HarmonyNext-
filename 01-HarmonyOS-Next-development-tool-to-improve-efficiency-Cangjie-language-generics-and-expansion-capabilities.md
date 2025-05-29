# HarmonyOS Next development tool to improve efficiency: Cangjie language generics and expansion capabilities
In the Cangjie language, generics and type extensions are two highly productive characteristics.If multi-paradigm support is Cangjie's soul, then generics and expansion mechanisms are powerful tools for Cangjie to improve development efficiency and code reusability.In my actual development of HarmonyOS Next application, generics and extensions not only helped me greatly reduce duplicate code, but also made the system architecture clearer and more flexible.In this article, we will explore these two powerful characteristics in depth through a practical perspective.

## Generic programming: written at one time, used in multiple places
Generics allows us to use type parameters when defining classes, interfaces, and functions, rather than binding to a specific type.This abstraction not only improves code reuse, but also provides type safety assurance during the compilation period.

### Generic application scenarios in Cangjie language
|Scenarios | Examples |
|--|--|
|Generics |Array<T>, Map<K, V>|
|Generic Functions|func concat<T>(lhs: Array<T>, rhs: Array<T>)|
|Generic interface|interface Repository<T>|
|Generic extensions | extend generic types |

### Example: Generic functions that implement array stitching
Suppose we want to implement a function that can splice arrays of any type. Traditional practice requires writing each type for different types, but using Cangjie's generics only needs to be defined once:
```
func concat<T>(lhs: Array<T>, rhs: Array<T>): Array<T> {
    let defaultValue = if (lhs.size > 0) {
        lhs[0]
    } else if (rhs.size > 0) {
        rhs[0]
    } else {
        return []
    }

    let newArr = Array<T>(lhs.size + rhs.size, item: defaultValue)
    newArr[0..lhs.size] = lhs
    newArr[lhs.size..lhs.size+rhs.size] = rhs
    return newArr
}

main() {
    let a = [1, 2, 3]
    let b = [4, 5, 6]
println(concat(a, b)) // Output [1,2,3,4,5,6]
}
```
1. `T` is a generic type parameter, which can be `Int`, `String`, or even a custom object.
2. Type inference makes it almost unnecessary to care about generic details when calling, and the experience is very silky.

### Generic Constraints: Precise control of available types
In some generic scenarios, we not only care about what the type parameter is, but also hope to limit it to support certain operations, such as judgment, sorting, etc.Cangjie supports generic constraints through the `where` clause, example:
```
func lookup<T>(element: T, arr: Array<T>): Bool where T <: Equatable {
    for (let e in arr) {
        if (element == e) {
            return true
        }
    }
    return false
}
```
Here, `T <: Equatable` means that `T` must be a type that supports equal comparison, otherwise the compiler will refuse to instantiate.
|Technical Points | Description |
|--|--|
|<:|Subtype constraints (must implement a certain interface) |
|Equatable|Supposes that equal value comparison is supported|

Practical experience: This design takes into account both flexibility and security, greatly avoiding runtime type errors.

## Type extension: Enhance existing types without intrusion
Another feature that I like very much about Cangjie language is type extension (Extension).It allows us to add new functions to existing types without modifying the original definition, greatly improving code organization and maintainability.

### Example: Extend new method to String type
For example, we want to add a print length to all `String` objects:
```
extend String {
    func printSize() {
        println(this.size)
    }
}

main() {
"HarmonyOS".printSize() // Output 9
}
```
1. `extend type name` enables extension
2. `this` represents the current object
3. The user experience of the extension method is no different from the built-in method

### Go further: Extend and add interface implementations
Cangjie even allows existing types to implement new interfaces in the expansion!
```
sealed interface Integer {}

extend Int8 <: Integer {}
extend Int16 <: Integer {}
extend Int32 <: Integer {}
extend Int64 <: Integer {}

main() {
    let a: Integer = 123
    println(a)
}
```
1. `sealed` means that the interface is only allowed to be implemented in the current package.
2. Through extension, basic types that were originally unrelated to the Integer interface can now enjoy the convenience of interface programming.

### A summary of a table: A list of Cangjie generics and extension features
|Features | Description |Practical Scenario Examples |
|--|--|--|
|Generic Class/Interface |Build a general structure with type parameters |Array<T>, Repository<T>|
|Generic functions |General algorithm for processing different types of data |concat<T>, lookup<T>|
|Generic constraints |Limit generic types must satisfy certain interfaces | where T <: Equatable|
|Type extension (method) |Add a new method to an existing type |String.printSize() |
|Type extension (interface) |Let existing types implement new interfaces |Int32 <: Integer|

## Summary
During the development of HarmonyOS Next, the generic and expansion mechanism of Cangjie language can greatly improve the reusability, flexibility and maintainability of our complex systems.My true experience is:
1. Generics make tool classes and data structure design extremely elegant, reducing a large amount of template code.
2. Extensions allow us to enhance existing code in an "open-closed" way without breaking the original architecture.

If you are pursuing writing both elegant and robust code, mastering generics and extensions is undoubtedly a compulsory course.
