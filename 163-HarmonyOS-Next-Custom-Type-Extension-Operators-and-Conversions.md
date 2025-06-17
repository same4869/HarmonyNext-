# HarmonyOS Next Custom Type Extension: Operators and Conversions
In HarmonyOS Next development, through custom type extensions, developers can break through the limitations of basic types and build exclusive data types according to business needs.Operator overloading and type conversion are the core technologies of custom type extension. They give custom types similar to basic types to improve the readability and maintainability of code.Next, we will dive into how to perform operator overloading and type conversion of custom types in HarmonyOS Next.

## 1. Operator overload application: assign unique behavior to custom types
Operator overloading allows developers to define specific behaviors of standard operators (such as `+`, `-`, `*`, etc.) for custom types, so that custom types can be seamlessly integrated into the grammar system of programming languages ​​and enhance the code expression ability.

### 1. Numerical operator overloading: vector operation
Taking the two-dimensional vector `Vector2D` as an example, the addition and number multiplication of vectors are realized by overloading the `+` and `*` operators:
```cj
struct Vector2D {
    var x: Float64
    var y: Float64
}

// Overload + operator implements vector addition
func +(lhs: Vector2D, rhs: Vector2D) -> Vector2D {
    return Vector2D(x: lhs.x + rhs.x, y: lhs.y + rhs.y)
}

// Overload the * operator to implement number multiplication
func *(lhs: Vector2D, scalar: Float64) -> Vector2D {
    return Vector2D(x: lhs.x * scalar, y: lhs.y * scalar)
}
```
When used, you can operate `Vector2D` like the basic value type:
```cj
let v1 = Vector2D(x: 1.0, y: 2.0)
let v2 = Vector2D(x: 3.0, y: 4.0)
let sum = v1 + v2
let scaled = v1 * 2.0
```

### 2. Comparison operator overloading: custom sorting rules
For custom `Person` type, overload the `<` operator to sort people by age:
```cj
struct Person {
    var name: String
    var age: Int
}

func <(lhs: Person, rhs: Person) -> Bool {
    return lhs.age < rhs.age
}

let people = [
    Person(name: "Alice", age: 25),
    Person(name: "Bob", age: 30),
    Person(name: "Charlie", age: 20)
]
let sortedPeople = people.sorted()
```

### 3. Logical operator overloading: Boolean custom type
Define a `TriState` enumeration representing tristate logic (true, false, unknown) and overload the logic operators `&&` and `||`:
```cj
enum TriState {
    case trueValue, falseValue, unknown
}

func &&(lhs: TriState, rhs: TriState) -> TriState {
    when (lhs, rhs) {
        (.trueValue,.trueValue): return.trueValue
        (.trueValue,.falseValue), (.falseValue,.trueValue), (.falseValue,.falseValue): return.falseValue
        else: return.unknown
    }
}

func ||(lhs: TriState, rhs: TriState) -> TriState {
    when (lhs, rhs) {
        (.trueValue,.trueValue), (.trueValue,.falseValue), (.falseValue,.trueValue): return.trueValue
        (.falseValue,.falseValue): return.falseValue
        else: return.unknown
    }
}
```
In this way, the `TriState` type can also perform logical operations to meet the needs of complex business logic.

## 2. Type conversion design: realize seamless connection between data types
Type conversion enables different types of data to be converted to each other. In HarmonyOS Next, developers can convert between custom types and basic types or other custom types through custom type conversion.

### 1. Conversion from custom type to basic type
Define a `Complex` type to represent a complex number and implement its conversion to the `Float64` type to obtain the modulus of the complex number:
```cj
struct Complex {
    var real: Float64
    var imaginary: Float64
}

func toFloat64(complex: Complex) -> Float64 {
    return sqrt(complex.real * complex.real + complex.imaginary * complex.imaginary)
}
```
It is convenient to convert the `Complex` type to `Float64` when used:
```cj
let complex = Complex(real: 3.0, imaginary: 4.0)
let magnitude = toFloat64(complex: complex)
```

### 2. Conversion between custom types
Assume that there are two types: `Point2D` and `Vector2D`, and implement mutual conversion between them:
```cj
struct Point2D {
    var x: Float64
    var y: Float64
}

func toVector2D(point: Point2D) -> Vector2D {
    return Vector2D(x: point.x, y: point.y)
}

func toPoint2D(vector: Vector2D) -> Point2D {
    return Point2D(x: vector.x, y: vector.y)
}
```
Through these conversion functions, switching between different types becomes more flexible and can better adapt to different business scenarios.

### 3. Implicit and explicit conversion
According to actual requirements, type conversion can be divided into implicit conversion and explicit conversion.Implicit conversions are automatically performed if the compiler considers safe, while explicit conversions require developers to call the conversion function manually.For example, for the `Complex` type, you can define a safe implicit conversion to the `String` type, which is used to output a plural string representation:
```cj
func toString(complex: Complex) -> String {
    return "\(complex.real) + \(complex.imaginary)i"
}

let complexString = toString(complex: complex)
```
For situations where data loss or conversion failure risk may be present, explicit conversion should be used to ensure the security of type conversion.

## 3. Custom type safety: Strict control during the compilation period
When doing custom type extensions, it is crucial to ensure type safety.HarmonyOS Next compiler is able to strictly check custom types of operations during the compilation period to avoid runtime errors.

### 1. Protocol constraints ensure type capability
By defining a protocol, constraining custom types must implement certain methods or properties to ensure that the types have specific capabilities.For example, defining a `Serializable` protocol requires the implementation of data serialization methods:
```cj
protocol Serializable {
    func serialize() -> String
}

struct User: Serializable {
    var name: String
    var age: Int

    func serialize() -> String {
        return "{\"name\": \"\(name)\", \"age\": \(age)}"
    }
}
```
Any type that follows the Serializable protocol must implement the Serialize method, otherwise the compiler will report an error, thereby ensuring the correctness of the type during the compilation period.

### 2. Operator parameter type limitation
When operator overloading, explicitly limit the operator's parameter type to prevent illegal operations.For example, in the `+` operator overload of `Vector2D`, make sure both operands are of type `Vector2D`:
```cj
func +(lhs: Vector2D, rhs: Vector2D) -> Vector2D {
// Make sure the parameter types are correct and avoid misoperation with other types
    return Vector2D(x: lhs.x + rhs.x, y: lhs.y + rhs.y)
}
```
If you try to add `Vector2D` with other incompatible types, the compiler will immediately report an error, effectively avoiding potential runtime errors.

## Summarize
In HarmonyOS Next, custom type extensions greatly enrich the expression capabilities of programming languages ​​through operator overloading and type conversion, allowing developers to build data types that are more in line with business needs.At the same time, a strict type safety check mechanism ensures the stability and reliability of custom types during use.Mastering these technologies can help developers write more efficient and flexible code, injecting powerful power into HarmonyOS Next application development.
