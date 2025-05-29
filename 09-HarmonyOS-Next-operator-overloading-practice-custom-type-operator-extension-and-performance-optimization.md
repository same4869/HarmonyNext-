
# HarmonyOS Next operator overloading practice: custom type operator extension and performance optimization

> This article aims to deeply explore the technical details of Huawei HarmonyOS Next system and summarize them based on actual development practices.It is mainly used as a carrier of technology sharing and communication, and it is inevitable to miss mistakes. All colleagues are welcome to put forward valuable opinions and questions in order to make common progress.This article is original content, and any form of reprinting must indicate the source and original author.


## 1. The "Contract Spirit" of Operator Overload: Syntax Rules and Type Constraints

In the Cangjie language of HarmonyOS Next, operator overloading allows native operator semantics to custom types (such as `class`, `struct`), making the code more declarative.But this ability needs to follow strict rules to ensure that language consistency is not compromised.

### 1.1 "Access Threshold" for Operator Overloading
Not all operators can be overloaded. Cangjie language limits a list of overloadable operators (priority from high to low):

| **Operator type** | **Supported operators** | **Typical use** |
|----------------|------------------------------------------|--------------------------------|
| Function call | `()` | Custom type call behavior (such as state machine) |
| Index operation | `[]` | Value and assignment of collection type |
| Unary operation | `!`, `-` | Logical non-, numerical inversion |
| Arithmetic operations | `+`, `-`, `*`, `/`, `%`, `**` | Numerical calculation, string splicing |
| Bit operation | `<<`, `>>`, `&`, `^`, `\|` | Binary data processing |
| Relationship Operation | `<`, `<=`, `>`, `>=`, `==`, `!=` | Conditional Judgment |

### 1.2 "Legal Format" of Operator Function
Overloaded operators must define the function through the `operator` keyword and must satisfy the following syntax constraints:
- **Modifier**: `operator` must be used, `static` (instance method semantics);
- **Number of parameters**: The unary operator has no parameters, and the binary operator has only one parameter;
- **Definition location**: Only defined in `class`, `struct`, `interface`, or `extend`.

**Example: Binary operator `+` overload (coordinates added)**
```typescript
struct Point {
  var x: Int64, y: Int64
  public operator func +(right: Point): Point {
    return Point(x: this.x + right.x, y: this.y + right.y)
  }
}

//Usage scenario: Vector operation
let p1 = Point(x: 3, y: 4)
let p2 = Point(x: 1, y: 2)
let p3 = p1 + p2 // is equivalent to p1.+(p2), result: Point(4, 6)
```


## 2. Practical scenario: operator extension from basic types to complex structures

### 2.1 数值类型扩展：自定义向量运算
Heavy loading of arithmetic operators for the `Vector` structure, implementing addition, number multiplication and other operations of vectors, improving the code readability of scientific computing scenarios.

```typescript
struct Vector {
  var values: Array<Float64>
  public init(_ values: Float64...) { self.values = values }

// Binary addition: add up the corresponding elements of vector
  public operator func +(right: Vector): Vector {
    let minLength = min(self.values.length, right.values.length)
    var result = Array<Float64>(repeating: 0, count: minLength)
    for (i in 0..<minLength) {
      result[i] = self.values[i] + right.values[i]
    }
    return Vector(result)
  }

// Univariate multiplication: vector number multiplication
  public operator func *(scalar: Float64): Vector {
    let result = self.values.map { $0 * scalar }
    return Vector(result)
  }
}

// Application example
let v1 = Vector(1.0, 2.0, 3.0)
let v2 = Vector(4.0, 5.0)
let v3 = v1 + v2 // Result: Vector([5.0, 7.0]) (take the shortest length)
let v4 = v3 * 2.0 // Result: Vector([10.0, 14.0])
```

### 2.2 Collection type extension: index operator and compound assignment
By overloading the `[]` operator, indexing and assignment of values ​​for custom collection types is implemented, and composite assignment operators (such as `+=`) are used to improve operational convenience.

```typescript
class FixedSizeArray<T> {
  private var data: Array<T>
  public init(size: Int64, defaultValue: T) {
    data = Array(repeating: defaultValue, count: size.toInt())
  }

// Index value: Supports single or multiple parameters
  public operator func [](index: Int64): T {
    return data[index.toInt()]
  }

// Index assignment: Receive values ​​through the `value` named parameter
  public operator func [](index: Int64, value: T): Unit {
    data[index.toInt()] = value
  }
}

// Use scenario: Fixed length array operation
let array = FixedSizeArray<Int64>(size: 3, defaultValue: 0)
array[0] = 1 // 调用赋值操作符
let firstValue = array[0] // Call the value operator
array += [2, 3] // If overload `+=`, compound assignment can be supported (return type matching is required)
```

### 2.3 Boolean type extension: Custom logical operators
To enumerate the logical operators, it realizes the conditional judgment of the state machine (note: Cangjie does not currently support logical operator overloading, this example is a conceptual demonstration).

```typescript
// Concept example: Assume that `&&` overloading is supported
enum Status {
  Ready,
  Busy,
  Error
}

public operator func &&(left: Status, right: Status): Bool {
  return left == .Ready && right == .Ready // 仅当两者均为 Ready 时返回 true
}

// Usage scenario: Status combination judgment
let status1: Status = .Ready
let status2: Status = .Busy
if status1 && status2 { // Assume this syntax is supported
  startTask()
}
```


## 3. Performance and design considerations: Avoid over-design and hidden costs

### 3.1 操作符重载的「语义适配性」原则
When overloading operators, you need to ensure that their semantics are consistent with native operators to avoid misleading developers.For example:
- **反例**：为字符串类型重载 `*` 表示重复（如 `str * 3` 生成重复字符串），虽实用但违背常规算术语义；  
- **正例**：为 `Matrix` 类型重载 `*` 表示矩阵乘法，符合数学定义。

### 3.2 "Automatic derivation" mechanism of composite assignment operators
When the return type of the binary operator is consistent with the left operand type, the Cangjie compiler will automatically support the corresponding compound assignment operators (such as `+=`, `*=`).This feature can reduce code redundancy, but attention should be paid to return type matching.

**Example: Automatically support the condition of `+=`**
```typescript
struct Counter {
  var value: Int64
  public operator func +(right: Int64): Counter {
return Counter(value: self.value + right) // The return type is Counter, which is consistent with the left operand
  }
}

let mut counter = Counter(value: 0)
counter += 5 // Automatic derivation support, equivalent to counter = counter + 5
```

### 3.3 Avoid performance loss: Priority to using native operators
For base types (such as `Int64`, `String`), native operators generally perform better than custom overloads.Overloading is considered only in the following scenarios:
- Custom types cannot implement semantics through native operators;
- Operator behavior of multiple types (such as polymorphic interfaces).

**Performance comparison: native vs custom addition**
| **Operation type** | **Native `+`(Int64)** | **Custom `+`(Structure)** |
|--------------------|----------------------|-------------------------|
| Single operation takes time | ~0.1ns | ~10ns (including object creation) |
| Applicable scenarios | High-frequency numerical calculations | Custom type logic packaging |


## 4. Architectural design: Application mode of operator overloading at the framework layer

### 4.1 Expression tree construction: Advanced applications of operator overloading
In data query or mathematical expression parsing scenarios, abstract syntax tree (AST) can be constructed through operator overloading to realize dynamic expression calculation.

```typescript
// Expression node base class
abstract class Expression {
  public abstract operator func +(right: Expression): Expression
  public abstract func evaluate(): Int64
}

// Numeric node
class NumberExpression: Expression {
  var value: Int64
  public operator func +(right: Expression): Expression {
    return BinaryExpression(left: this, op: "+", right: right)
  }
  public func evaluate(): Int64 { return value }
}

// Binary expression node
class BinaryExpression: Expression {
  var left: Expression, op: String, right: Expression
  public operator func +(right: Expression): Expression {
    return BinaryExpression(left: this, op: "+", right: right)
  }
  public func evaluate(): Int64 {
    let leftVal = left.evaluate()
    let rightVal = right.evaluate()
return op == "+" ? leftVal + rightVal : 0 // Simplify logic
  }
}

// 使用示例：动态构建表达式 1 + 2 + 3
let expr = NumberExpression(value: 1) + NumberExpression(value: 2) + NumberExpression(value: 3)
println(expr.evaluate()) // Output: 6
```

### 4.2 类型约束与接口设计
The implementation of specific operators is mandatory through interfaces to ensure consistency of polymorphic types.For example, the `+` operator defined by the `Addable` interface constraint type must support.

```typescript
interface Addable {
  public operator func +(right: Self): Self
}

struct Vector2D: Addable {
  var x: Int64, y: Int64
  public operator func +(right: Vector2D): Vector2D {
    return Vector2D(x: x + right.x, y: y + right.y)
  }
}

func add<T: Addable>(a: T, b: T): T {
return a + b // All types that implement Addable are callable
}

// Application scenario: Unified processing of types that support addition
let v1 = Vector2D(x: 1, y: 2)
let v2 = Vector2D(x: 3, y: 4)
let sum = add(v1, v2) // Call the custom `+` operator
```


## 5. Pit avoidance guide: Common traps of operator overloading

| **Problem Scenario** | **Cause Analysis** | **Solution** |
|--------------------------|--------------------------------|-----------------------------------|
| Error reported during compilation period "operator not defined" | Incorrectly declared `operator` function | Check whether the function definition is within the allowed type (such as `class`/`struct`) |
| Compound assignment operator invalid | The binary operator return type does not match the lvalue type | Modify the return type to the lvalue type or its subtype |
| Enumeration types cannot overload operators | Enumeration only supports finite operators (such as `()`) | Use `struct` or `class` instead of enums |
| Operator priority confusing | Overloading does not follow native operator priority | explicitly specify the order of operations through brackets (such as `a + (b * c)`) |


## 结语：操作符重载的「克制」与「创新」平衡

Operator overloading is the combination of "synthetic sugar" and "powerful functions" in the Cangjie language in HarmonyOS Next.Rational use can make the code closer to business semantics, but abuse can lead to reduced readability or performance problems.In actual development, it is recommended:
1. **Preferential to intuition**: Ensure that the behavior of the overloaded operator is consistent with the developer's general perception of the operator;
2. **Control extension scope**: Only overload necessary operators for domain models (such as geometric figures, financial data) to avoid contaminating basic types;
3. **Performance priority principle**: For operations of high-frequency calls, native implementation or optimization algorithms are preferred rather than dependent operator overloading.

By combining operator overloading with Hongmeng's componentization and generic programming, developers can build more expressive domain-specific languages ​​(DSLs) to provide elegant solutions for complex scenarios.
