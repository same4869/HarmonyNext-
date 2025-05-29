
# HarmonyOS Next Function Overloading and Operator Overloading Collaborative Practical Practice: Polymorphic Design and Domain Modeling

> This article aims to deeply explore the technical details of Huawei HarmonyOS Next system. It is based on the document content of the "0009-Closure-Function-Cangjie Programming Language Development Guide-Learn Cangjie Language.docx", and summarizes the collaborative application of function overloading and operator overloading based on actual development practices.The cases in the article are based on document rules to avoid involving unmentioned features.


## 1. The "polymorphic complementarity" mechanism between function overloading and operator overloading

In Cangjie language, function overloading implements different logic of the same name function through parameter differences, while operator overloading assigns native operator semantics to custom types.The combination of the two can build a flexible polymorphic system, especially in models in fields such as mathematical calculations and data structures.

### 1.1 Different dimensions of polymorphism
| **Features** | **Function Overload** | **Operator Overload** |
|------------------|-----------------------------|-----------------------------|  
| **Definition method** | Function with the same name, different parameter types/number of numbers | `operator` keyword modification function |
| **Syntax representation** | The function name is the same and it will automatically match when called | Use native operators (such as `+`, `[]`) |
| **Typical Scenarios** | Constructors, Data Transformation Functions | Custom Types of Arithmetic/Logical Operations |

### 1.2 Collaborative Rules
- Operator overloading functions can participate in function overloading (such as defining different `+` operations for different types);
- Function overloading has higher priority than operator overloading (such as explicit function calls take precedence over operator implicit calls).


## 2. Numerical type extension: from function overload to operator overload

### 2.1 Polymorphic implementation of complex types
The construction and conversion of complex numbers are realized through function overloading, and arithmetic operations are supported in combination with operator overloading.

#### Function Overload: Complex Constructor
```typescript  
struct Complex {  
  var real: Float64  
  var imag: Float64  

// Function overload: no parameter constructor, single parameter constructor, double parameter constructor
  public init() {  
    real = 0.0  
    imag = 0.0  
  }  

  public init(value: Float64) {  
    real = value  
    imag = 0.0  
  }  

  public init(real: Float64, imag: Float64) {  
    this.real = real  
    this.imag = imag  
  }  
}  
```  

#### Operator overloading: complex addition and multiplication
```typescript  
struct Complex {  
// Overload binary addition operator
  public operator func +(other: Complex): Complex {  
    return Complex(real: real + other.real, imag: imag + other.imag)  
  }  

//On-partial multiplication operator overload (number multiplication)
  public operator func *(scalar: Float64): Complex {  
    return Complex(real: real * scalar, imag: imag * scalar)  
  }  
}  

// Use example
let c1 = Complex(1.0, 2.0)  
let c2 = Complex(3.0)  
let sum = c1 + c2 // is equivalent to c1.+(c2), result: Complex(4.0, 2.0)
let scaled = c1 * 2.0 // Result: Complex(2.0, 4.0)
```  


## 3. Collection type modeling: the coordination between index operators and function overloading

### 3.1 Index and slicing operations of dynamic arrays
Element access and modification are realized through the overload of the index operator `[]`, and a variety of indexing methods are provided (such as integer index and range index) combined with function overload.

#### Index operator overloading: value and assignment
```typescript  
class DynamicArray<T> {  
  private var data: Array<T> = []  

// Value: Int64 index
  public operator func [](index: Int64): T? {  
    guard index >= 0 && index < data.length else { return nil }  
    return data[index.toInt()]  
  }  

// Assignment: Int64 index + value parameter
  public operator func [](index: Int64, value: T): Unit {  
    if index >= 0 && index < data.length {  
      data[index.toInt()] = value  
    }  
  }  
}  

// Use example
let arr = DynamicArray<Int64>()  
arr[0] = 10 // Call the assignment operator
let value = arr[0] // Call the value operator, value is 10
```  

#### Function overloading: Supports scope indexing
```typescript  
class DynamicArray<T> {  
// Function overload: range index (such as arr[1..3])
  public func [](range: Range<Int64>): Array<T> {  
    let start = range.start.toInt()  
    let end = range.end.toInt()  
    return data[start..<end]  
  }  
}  

// Use example
let subArray = arr[0..2] // Call function overload to get the element with index 0-1
```  


## 4. Error handling and compatibility: overloaded boundary rules

### 4.1 Limitations of operator overloading
- Logical operators (such as `&&`, `||`) cannot be overloaded, and only the operators listed in the document are supported;
- The index operator assignment form (`[]=`) requires the return type to be `Unit` and only mutable types that are not `enum` are supported.

**Error Example: Overload Logical Operator**
```typescript  
struct BooleanWrapper {  
public operator func &&(other: BooleanWrapper): BooleanWrapper { // Error: Logical operator overloading is not supported
    return BooleanWrapper(value: self.value && other.value)  
  }  
}  
```  

### 4.2 Priority conflicts in function overloading
When there are multiple matching overloaded functions, the compiler resolves in the following order:
1. Exactly match parameter types;
2. Implicit type conversion matching;
3. Variable length parameter matching (last option only).

**Example: Parameter type conflict**
```typescript  
func f(a: Int64) { println("Int") }  
func f(a: Float64) { println("Float") }  
f(3.14) // Output: Float (exactly match Float64)
f(10) // Output: Int (exactly match Int64)
```  


## 5. Domain model practice: polymorphic operations of geometric figures

### 5.1 Operator overloading of graphics base classes and derived classes
Define the Shape interface, and the derived classes Circle and Rectangle are respectively overloaded with the area calculation operator.

```typescript  
interface Shape {  
  var area: Float64 { get }  
}  

class Circle : Shape {  
  var radius: Float64  
public operator func area: Float64 { // Operator overloading is used to calculate area
    return PI * radius * radius  
  }  
}  

class Rectangle : Shape {  
  var width: Float64  
  var height: Float64  
  public operator func area: Float64 {  
    return width * height  
  }  
}  

// Polymorphic call
func calculateArea(shape: Shape) {  
println("Area: \(shape.area)") // Automatically call the operator overload of derived classes
}  
```  

### 5.2 Function overloading implements graphical transformation
```typescript  
// Function overload: translation transformation
func translate(shape: Circle, dx: Float64, dy: Float64) {  
  shape.center.x += dx  
  shape.center.y += dy  
}  

func translate(shape: Rectangle, dx: Float64, dy: Float64) {  
  shape.origin.x += dx  
  shape.origin.y += dy  
}  
```  


## 6. Performance and design principles

### 6.1 Avoid overloading
- The number of operator overloads of a single type is recommended to not exceed 5, and core operations are preferred (such as `+`, `*`, `[]`);
- The parameter differences in function overloading should have clear semantics (such as the number of parameters of the constructor represents the differences in initialization mode).

### 6.2 Prefer generics over overloading
When the logic is similar but the types are different, generics are more concise than overloading.

**Recommended example: Generic sorting function**
```typescript  
func sort<T: Comparable>(array: Array<T>) {  
// Generic implementation, supporting all Comparable types
  array.sort()  
}  
```  

**Don't recommend: Overload sorting functions for each type**
```typescript  
func sort(numbers: Array<Int64>) { ... }  
func sort(strings: Array<String>) { ... } // Redundant code
```  


## Conclusion: The value of "domain modeling" of the overload mechanism

The coordination between function overloading and operator overloading is essentially mapping the complex logic of the real world into a concise code model through polymorphism.In Hongmeng development, it is recommended:
1. **Domain-driven design (DDD)**: Design overload rules for business models (such as financial computing, graphic rendering) to improve code semantic expression;
2. **Consistency principle**: Ensure that the behavior of overloaded operators is consistent with the native semantics (such as `+` always means "combination" or "addition");
3. **Test coverage**: Perform boundary testing on different branches of overloaded functions to ensure that polymorphic behavior is in line with expectations.

By rationally applying the reload mechanism, our developers can build more scalable and readable domain models in Hongmeng applications, providing elegant solutions for complex business scenarios.
