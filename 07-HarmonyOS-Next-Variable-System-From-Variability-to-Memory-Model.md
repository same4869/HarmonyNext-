# HarmonyOS Next Variable System: From Variability to Memory Model
In the development of Cangjie language in HarmonyOS Next, the variable system is the basis for building programs. The variability, value types and reference types it covers, as well as the compiler-related strategies, profoundly affect the running logic and performance of the program.As a technician who has accumulated rich practical experience in this field, I will analyze these key points in depth based on actual cases.

## 1. Let/var comparison
### (I) Advantages of immutable variables in concurrent programming
In Cangjie language, `let` is used to define immutable variables, and `var` is used to define mutable variables.These two variables have significant differences in concurrent programming scenarios, and immutable variables show unique advantages in concurrent programming.

In a concurrent environment, multiple threads may access and modify shared data at the same time, which can easily cause data competition and inconsistency.For example, when multithreading operations on shared counters:
```cj
// Assume this is in a concurrent environment
var counter = 0
// Thread 1 execution
counter++
// Thread 2 execution
counter++
```
Since thread 1 and thread 2 may read and modify the value of `counter` at the same time, the final value of `counter` may not be the expected 2, but 1 (assuming that thread 1 and thread 2 read the value of `counter` is 0, then add 1 and write it back, which will happen).

Using the immutable variable `let` can effectively avoid this kind of problem.Because once an immutable variable is initialized, its value cannot be modified, which eliminates the risk of data competition.In concurrent programming, we can define shared data as immutable variables and then process the data through functional programming.For example, when calculating the results of operations on data by multiple threads, each operation can be regarded as a transformation of immutable data, returning new immutable data, rather than directly modifying the shared data.In this way, each thread operates an independent data copy and will not interfere with each other, thus ensuring data consistency and program stability.

## 2. Deep analysis of value/reference type
### (I) Differences in copy behavior between struct and class (memory allocation diagram)
In Cangjie language, `struct` belongs to the value type and `class` belongs to the reference type. There are obvious differences in their copy behavior, which is closely related to the memory allocation method.

For value type `struct`, a new copy is created when the assignment is performed.For example:
```cj
struct Point {
    var x: Int
    var y: Int
}

main() {
    let p1 = Point(x: 1, y: 2)
    var p2 = p1
    p2.x = 3
    println("p1.x: \(p1.x), p2.x: \(p2.x)")
}
```
In the above code, when `p2 = p1`, `p2` obtains a copy of `p1`, modifying `p2.x` will not affect `p1.x`, and the output result is "p1.x: 1, p2.x: 3".From the perspective of memory allocation, `p1` and `p2` have their own independent memory space on the stack, storing the same data value, as shown below:
```mermaid
graph TD;
A[stack memory] --> B[p1(x:1,y:2)];
A --> C[p2(x:1,y:2)];
```

For reference type `class`, the assignment operation only establishes a reference relationship.For example:
```cj
class Point {
    var x: Int
    var y: Int

    init(x: Int, y: Int) {
        this.x = x
        this.y = y
    }
}

main() {
    let p1 = Point(x: 1, y: 2)
    let p2 = p1
    p2.x = 3
    println("p1.x: \(p1.x), p2.x: \(p2.x)")
}
```
Here, after `p2 = p1`, `p1` and `p2` point to the same object in the heap memory. Modifying `p2.x` will affect `p1.x`, and the output result is "p1.x: 3, p2.x: 3".The memory allocation situation is as follows:
```mermaid
graph TD;
A[stack memory] --> B[p1 (points to objects in heap memory)];
A --> C[p2 (points to the same object in heap memory)];
D[heap memory] --> E[object(x:1,y:2, then becomes x:3,y:2)];
```

Understanding this difference in copy behavior is essential to writing the right code.In actual development, if an independent data copy is needed, the value type should be selected; if you want to share data and improve memory utilization, the reference type should be selected.

## 3. Compiler conservative strategy
### (I) The principle of variable initialization error report in try-catch block
In Cangjie language, the compiler adopts a conservative strategy to handle variable initialization, which is particularly obvious in the `try-catch` block.For example:
```cj
main() {
    let a: String
    try {
        a = "1"
    } catch (_) {
        a = "2" // Error, cannot assign to immutable value
    }
}
```
The above code will report an error because the compiler assumes that all the `try` blocks are always executed and exceptions are always thrown.Under this assumption, `a` may enter the `catch` block without being initialized in the `try` block, and the immutable variable `a` cannot be assigned multiple times, so the compiler reports an error.

From a compiler's perspective, this conservative strategy is to ensure the security and stability of the code.In complex program logic, the code in the `try` block may involve various operations that may throw exceptions, and the compiler cannot determine whether the variables in the `try` block will be initialized.Therefore, in order to avoid potential runtime errors, the compiler adopts a conservative strategy to report an error message to this situation.In actual development, we need to pay attention to the compiler's behavior and handle variable initialization reasonably, such as initializing variables outside the `try-catch` block, or adjusting the code structure according to the specific logic to meet the compiler's requirements and ensure that the program can be compiled and run correctly.
