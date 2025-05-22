# HarmonyOS Next development essentials: efficient type system and type inference of Cangjie language
In the process of using Cangjie language to develop HarmonyOS Next applications, I became more and more aware that the design of a type system directly determines the development efficiency and program reliability of a language.Cangjie did a very good job in this regard. He not only had a powerful static type system, but also greatly reduced the development burden through intelligent type inference.

In this article, I will combine the actual development experience to learn more about the type system and type inference mechanism of Cangjie language, and how to write more concise, safer and more efficient code through them.

## Static type system: the first line of defense guaranteed during compilation period
Cangjie is a statically typed language, that is, the types of variables, functions, and expressions are determined at compile time, rather than dynamically determined at runtime.This design brings several huge advantages:
|Advantages | Description |
|--|--|
|Type Safety | Avoid runtime crashes or hidden bugs caused by type mismatch |
|Strong maintainability | Clear interface contracts, call errors can be exposed in advance |
|Best performance optimization | Compiler can perform more radical optimization based on type information |
|Smart IDE support | More accurate automatic completion, jump, and reconstruction functions |

For example, Cangjie language is very subdivided in basic data types:
|Cangjie Type|Description|
|--|--|
|Int8, Int16, Int32, Int64| Various bit width integer types|
|Float32, Float64|Single-precision, double-precision floating point number|
|String|String type|
|Bool|Bool type|

During the development process, if I try to assign the String type to the Int32 variable, the compiler will directly report an error without leaving any hidden dangers to the runtime.
```
let a: Int32 = "123" // ❌ Compilation error: Type mismatch
```

## Type Inference: Elegant and Efficient Development Experience
Although Cangjie is a static typed language, it does not force you to write lengthy type statements everywhere like C++.Cangjie has built-in powerful type inference mechanism, which can intelligently infer the types of variables and functions from the context, greatly simplifying code writing.
### 1. Type inference in variable definition
在定义变量时，只要赋初值，仓颉就能推断出类型，无需显式标注：
```
let foo = 123 // Inferred as Int64
var bar = "hello" // Inferred as String
let isValid = true // Inferred as Bool
```
Practical experience: This makes the code more concise, while retaining the security and performance advantages brought by static typing, almost achieving a smooth experience in Kotlin/Swift.
### 2. Type inference of function return value
Cangjie supports expressions at the end of the function body as the basis for inference of the return value:
```
func add(a: Int, b: Int) {
    a + b
}
```
Although the function signature does not explicitly write the return type, the compiler can still accurately infer that the return type of `add` is `Int`.

Note: If the function is logically complex or has multiple return paths, it is recommended to explicitly label the return type to improve readability.
### 3. Generic parameter inference
When using generic functions, Cangjie also supports automatic inference of generic parameter types, making generic programming easier and more natural.
For example, the `map` function in the standard library:
```
func map(f: (T) -> R): (Array) -> Array {
    ...
}
```
There is no need to manually specify the types of `T` and `R` when calling:
```
map({ i => i.toString() })([1, 2, 3])
// Automatically inferred as map
```
Practical experience: In handling collections, streaming operations, asynchronous orchestration and other scenarios, Cangjie's generic inference greatly reduces template code, and the development experience is comparable to TypeScript/Kotlin.

### Cangjie type inference summary table
For the sake of quick understanding, I made a Cangjie type inference support table:
|Scenario|Support inference?|Notes |
|--|--|--|
|Variable definition initial value|✅|Initialize assignment to infer|
|Function return value inference|✅|Simple functions can be inferred, complex functions are recommended for labeling|
|Generic parameter inference|✅|Support automatic inference|
|Lambda Expression Parameters|Section ✅|Context-dependent chains|
|Class member variable definition|❌|Need explicit declaration of type|

### Example code: Cangjie type inference practice project
Let’s take a slightly more complicated example to demonstrate Cangjie’s inference ability:
```
func findFirstEven(arr: Array): Int? {
    for (let n in arr) {
        if (n % 2 == 0) {
            return n
        }
    }
    return null
}

main() {
    let nums = [1, 3, 5, 8, 9, 10]
    let evenNum = findFirstEven(nums)

    match (evenNum) {
        case n: Int => println("Found even number: ${n}")
        case _ => println("No even number found")
    }
}
```
Analysis:
1. `nums` is inferred as `Array<Int>`
2. `evenNum` is inferred as `Int?` (nullable type)
3. The `match` expression pattern matching based on the inferred type

这种写法既简洁又保证了类型安全，写着写着，开发者自然就形成了更好的代码习惯。

## Summary
The type system and type inference of Cangjie language allow HarmonyOS Next developers to enjoy:
1. Safety and performance of static types
2. Dynamic language-like development fluency
3. The minimum mental burden when facing complex generics

Judging from my own practical project experience, Cangjie type system is particularly important in large-scale development: whether it is multi-person collaboration, module layering, or interface design and data transmission, strong type guarantee is the cornerstone of quality, while automatic inference greatly improves the speed and pleasure of development.

If HarmonyOS Next is an ecological upgrade, then the Cangjie language type system is one of the foundations of this upgrade.
