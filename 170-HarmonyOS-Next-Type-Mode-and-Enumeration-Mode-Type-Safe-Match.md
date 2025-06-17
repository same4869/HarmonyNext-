
# HarmonyOS Next Type Mode and Enumeration Mode: Type-Safe Match

In HarmonyOS Next development, type patterns and enumeration patterns are the core tools for achieving type safety matching.Type mode is used for dynamic type checking, while enumeration mode is precisely matched to the enum type constructor.This paper combines the characteristics of Cangjie's language to analyze the grammatical rules, application scenarios and collaborative logic with other modes.


## 1. Type pattern: the core of dynamic type checking
The type mode is used to determine whether the runtime type of a value is a subtype of a certain type, and is suitable for dynamic distribution in polymorphic scenarios.

### 1. Basic syntax and matching logic
```cj
match (value) {
case identifier: Type => Execute logic after type matching
case _: Type => Only type matches, no variable binding
}
```  
- **Rules**: If `value` is an instance or a subtype instance of `type`, the match is successful.
- **Example**: Type judgment of parent class and child class
  ```cj
  open class Animal {}
  class Dog <: Animal {}
  class Cat <: Animal {}

  func speak(animal: Animal) {
      match (animal) {
case dog: Dog => println("Wangwang") // Bind mode dog captures Dog instance
case cat: Cat => println("Meow Meow") // Bind mode cat captures Cat instance
case _: Animal => println("Unknown Animal") // Wildcard pattern matches other Animal subclasses
      }
  }

speak(animal: Dog()) // Output: Wangwang
  ```  

### 2. Type pattern matches interface
When a value implements an interface, you can determine whether it complies with the interface constraints through the type mode:
```cj
interface Flyable { func fly() }
class Bird <: Flyable { func fly() { println("Fly") } }
class Car {}

func testFly(obj: Any) {
    match (obj) {
case flyable: Flyable => flyable.fly() // Match the type that implements the Flyable interface
case _ => println("cannot fly")
    }
}

testFly(obj: Bird()) // Output: Feixiang
testFly(obj: Car()) // Output: Cannot fly
```  

### 3. Limitations of Type Patterns
- Only support type checking for classes and interfaces, and no basic types (such as `Int`, `String`).
- When matching fails, wildcards must be used to ensure logical integrity.


## 2. Enumeration mode: accurate matching of enum values
The enumeration pattern matches enumeration type constructors, and supports precise deconstruction of non-arguments, parameters and recursive constructors.

### 1. Parameterless enumeration constructor matching
Match enum values ​​directly by constructor name:
```cj
enum Direction { | Up | Down | Left | Right }

func move(dir: Direction) {
    match (dir) {
case Up => println("up")
case Down => println("down")
case Left | Right => println("Horizontal Move") // Multi-constructor Merge Match
    }
}

move(dir: .Left) // Output: horizontal movement
```  

### 2. Destruction of parameter enumeration constructor
Extract constructor parameter values ​​by pattern matching:
```cj
enum Temperature { | Celsius(Float) | Fahrenheit(Float) }

func convert(temp: Temperature) {
    match (temp) {
case Celsius(c) => println("\(c)℃ = \(c * 1.8 + 32)℉") // Binding mode c extracts the temperature of Celsius
case Fahrenheit(f) => println("\(f)℉ = \((f - 32) / 1.8)℃") // Binding mode f extracts Fahrenheit temperature
    }
}

convert(temp: .Celsius(25)) // Output: 25℃ = 77℉
```  

### 3. Pattern matching of recursive enumerations
Recursive enumeration is often used to build tree-like structures (such as expression parsing), and pattern matching requires processing of recursive hierarchy:
```cj
enum Expr {
    | Num(Int)
| Add(Expr, Expr) // Recursively reference the Expr type
    | Sub(Expr, Expr)
}

func evaluate(expr: Expr) -> Int {
    match (expr) {
case Num(n) => n // Basic numeric node
case Add(l, r) => evaluate(l) + evaluate(r) // Recursively calculate the addition node
case Sub(l, r) => evaluate(l) - evaluate(r) // Recursively calculate subtraction node
    }
}

let expr = Add(Num(5), Sub(Num(10), Num(3)))
println(evaluate(expr: expr)) // Output: 5 + (10 - 3) = 12
```  


## 3. Mode collaboration: a hybrid application of type mode and enumeration mode
In complex scenarios, type mode and enumeration mode can be combined to achieve accurate matching of multi-layer data.

### 1. Destruction of enumerated nested types
```cj
enum DataWrapper {
    | IntData(Int)
    | StrData(String)
    | ObjData(Object)
}

class Object {}

func processData(wrapper: DataWrapper) {
    match (wrapper) {
case IntData(n: Int) => println("Integer:\(n)") // Enumeration mode + Type mode
case StrData(s: String) => println("String:\(s)")
case ObjData(obj: Object) => println("Object Type")
    }
}

processData(wrapper: .StrData("Hello")) // Output: String: Hello
```  

### 2. Type-safe error handling
Enumerate the pattern to match the error type and combine the type pattern to ensure the validity of the parameter:
```cj
enum Error {
    | InvalidType(String)
    | OutOfRange(Int, Int)
}

func validate(value: Any, min: Int, max: Int) -> Error? {
    match (value) {
case n: Int where n < min || n > max => .OutOfRange(n, max) // Type mode + conditional judgment
case s: String where s.isEmpty => .InvalidType("empty string")
        default => nil
    }
}

let error = validate(value: 5, min: 10, max: 20)
match (error) {
case .OutOfRange(n, max) => println("\(n) exceeds maximum value\(max)")
    case .InvalidType(msg) => println(msg)
    case _ => ()
}
```  

### 3. Type filtering of collection elements
Use type patterns to filter specific type elements in a collection:
```cj
let items: Array<Any> = [1, "a", Dog(), 3.14]
let dogs = items.filter {
    match ($0) {
case _: Dog => true // Type pattern matching Dog instance
        default => false
    }
}
println(dogs.count) // Output: 1 (only one Dog instance)
```  


## 4. Common traps and best practices
### 1. Exhaustion requirements for enumeration patterns
All constructors of the enum must be overwritten or wildcards are added, otherwise the compiler will be errored:
```cj
enum Color { | Red | Green | Blue }

func printColor(color: Color) {
    match (color) {
case Red => println("red")
case Green => println("green")
// Compilation error: Blue constructor not overwritten
    }
}
```  

### 2. Judgment of subtype relationship of type pattern
Make sure that the type in the type pattern is the parent class or interface of the actual type to avoid invalid matches:
```cj
class Animal {}
class Dog <: Animal {}

func feed(animal: Animal) {
    match (animal) {
case _: Dog => println("feed dog food") // Correct: Dog is a subclass of Animal
case _: String => println("Error type") // Error: String has no inheritance relationship with Animal
    }
}
```  

### 3. Termination conditions for recursive enumeration
In recursive pattern matching, you need to ensure that there is a basic case to avoid infinite recursion:
```cj
enum List {
    | Nil
| Cons(Int, List) // Recursive constructor
}

func sum(list: List) -> Int {
    match (list) {
case .Nil => 0 // Basic case, terminate recursion
case .Cons(n, rest) => n + sum(list: rest) // Recursively calculate the remaining elements
    }
}

let list = Cons(1, Cons(2, Cons(3, Nil)))
println(sum(list: list)) // Output: 6
```  


## Summarize
Type mode and enumeration mode are important components of HarmonyOS Next type safety system:
- **Type mode**Implement polymorphic logic through dynamic type checking, which is suitable for hierarchical judgments of classes and interfaces;
- **Enum mode**Precise matching of enumeration constructors, supporting non-arguments, and recursive scenarios.
