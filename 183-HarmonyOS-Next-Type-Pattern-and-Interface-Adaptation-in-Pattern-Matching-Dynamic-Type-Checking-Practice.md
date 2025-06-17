
# HarmonyOS Next Type Pattern and Interface Adaptation in Pattern Matching: Dynamic Type Checking Practice

In HarmonyOS Next development, Type Patterns are an important part of pattern matching and are used to check whether the type of value is expected at runtime.When used in conjunction with the Interface, type mode can achieve flexible polymorphic behavior while maintaining type safety.This article is based on Cangjie language document, analyzing the syntax rules of type mode, collaborative application with interfaces, and typical scenarios.


## 1. Basic syntax and matching logic of type patterns
Type mode is used to determine whether the runtime type of a value is a subtype of a certain class or interface. It supports two forms:
1. **`id: Type`**: Convert the value to the `Type` type when the match is successful and bind to the identifier `id`.
2. **`_: Type`**: Only check types, do not bind variables.

### Core rules:
- If the value type is a subclass of `Type` or the `Type` interface is implemented, the match is successful.
- When the match fails, continue to try subsequent modes.

#### Example: Type pattern matching of classes
```cj
open class Animal {}
class Dog <: Animal {}
class Cat <: Animal {}

func speak(animal: Animal) {
    match (animal) {
case dog: Dog => println("Wangwang") // Match Dog instance and bind to dog variable
case cat: Cat => println("Meow Meow") // Match Cat instance and bind to cat variable
case _: Animal => println("Unknown Animal") // Match other Animal subclasses
    }
}

let pet = Dog()
speak(animal: pet) // Output: Wangwang
```  


## 2. Collaborative application of type mode and interface
The interface defines a contract for a set of methods, and the type mode can be used to check whether the value implements a specific interface and implements dynamic scheduling at the interface level.

### 1. Interface definition matches type
```cj
interface Flyable { func fly() }
class Bird <: Flyable { 
func fly() { println("Bird is flying") }
}
class Plane <: Flyable { 
func fly() { println("Airplane is flying") }
}
class Car {}

func makeFly(obj: Any) {
    match (obj) {
case flyable: Flyable => flyable.fly() // Match the type that implements the Flyable interface
case _ => println("cannot fly")
    }
}

makeFly(obj: Bird()) // Output: Bird is flying
makeFly(obj: Car()) // Output: Unable to fly
```  

### 2. Multi-interface matching and priority
When a type implements multiple interfaces, it can be matched in order by priority:
```cj
interface Swimmable { func swim() }
interface Flyable { func fly() }
class Duck <: Flyable, Swimmable { 
func fly() { println("Duck Fly") }
func swim() { println("Duck Swim") }
}

func performAction(obj: Any) {
    match (obj) {
case flyable: Flyable => flyable.fly() // Preferentially match the Flyable interface
        case swimmable: Swimmable => swimmable.swim()
        default => ()
    }
}

performAction(obj: Duck()) // Output: Duck Fly
```  


## 3. Advanced application scenarios of type mode
### 1. Dynamic data analysis and conversion
When processing heterogeneous data (such as JSON parsing results), type mode can be used to determine the data type and perform conversion:
```cj
let jsonValue: Any = "hello"

match (jsonValue) {
case str: String => println("String: \(str)")
case num: Int => println("Integer: \(num)")
case bool: Bool => println("Bool: \(bool)")
default => println("Unknown Type")
}
```  

### 2. Type distinction in error handling
Combining custom error types, different error sources are distinguished by type mode:
```cj
interface Error { func getMessage(): String }
class FileError <: Error { 
    let msg: String
    init(msg: String) { self.msg = msg }
    func getMessage() -> String { msg }
}
class NetworkError <: Error { 
    let code: Int
    init(code: Int) { self.code = code }
func getMessage() -> String { "Error code: \(code)" }
}

func handleError(err: Any) {
    match (err) {
case fileErr: FileError => println("File Error: \(fileErr.getMessage())")
case netErr: NetworkError => println("Network Error: \(netErr.getMessage())")
case _: Error => println("Unknown Error")
    }
}

handleError(err: FileError(msg: "File not found")) // Output: File Error: File not found
```  


## 4. Combination of type mode and other modes
### 1. Match with enumeration pattern nesting
Use type patterns in enumeration constructors to implement more complex data destruction:
```cj
enum DataWrapper {
    | Primitive(Any)
    | Object(Any)
}

let wrapper = DataWrapper.Primitive(42)

match (wrapper) {
case .Primitive(num: Int) => println("Integer:\(num)") // Match the enum first, then match the type
case .Primitive(str: String) => println("String:\(str)")
case .Object(obj: Object) => println("Object:\(obj)")
}
```  

### 2. Type mode with conditions
Add extra conditions to type mode via the `where` clause:
```cj
class Student <: Person {
    let grade: Int
    init(grade: Int) { self.grade = grade }
}

func processPerson(person: Any) {
    match (person) {
case student: Student where student.grade >= 90 => println("Excellent Student")
case student: Student => println("Student Grade: \(student.grade)")
case _: Person => println("ordinary person")
    }
}
```  


## 5. Precautions and best practices
### 1. Avoid matching failures caused by type erasure
When using generics or `Any` types, be aware that type erasing may cause the loss of type information at runtime:
```cj
let list: Array<Any> = [Dog()]
match (list[0]) {
case dog: Dog => println("is Dog") // The match is successful, the runtime type is Dog
default => println("non-Dog")
}
```  

### 2. Preferential matching of specific types
Place more specific type patterns on top of the matching branch to avoid being matched in advance by the parent class or interface patterns:
```cj
class Bulldog <: Dog {}

func identifyDog(dog: Dog) {
    match (dog) {
case bulldog: Bulldog => println("bulldog") // Specific subclasses are preferred
case dog: Dog => println("ordinary dog")
    }
}
```  

### 3. Preprocessing in combination with `is` operator
Before complex matching, you can use the `is` operator to quickly filter types to improve performance:
```cj
func fastCheck(obj: Any) {
    if obj is Flyable {
// Filter in advance to reduce pattern matching branches
        match (obj) {
            case flyable: Flyable => flyable.fly()
            default => ()
        }
    }
}
```  


## Summarize
Type mode is the core tool for implementing dynamic type checking in HarmonyOS Next, especially in the following scenarios:
- **Polymorphic behavior implementation**: Through the interface type mode, instances of different implementation classes are handled uniformly.
- **Heterogeneous data processing**: When parsing dynamic data (such as JSON, XML), distinguish different data types.
- **Error classification processing**: Combining with custom error interfaces, implement fine-grained error processing logic.
