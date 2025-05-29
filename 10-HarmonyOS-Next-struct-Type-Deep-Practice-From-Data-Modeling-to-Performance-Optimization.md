
# HarmonyOS Next struct Type Deep Practice: From Data Modeling to Performance Optimization

In HarmonyOS Next development, `struct`, as the core carrier of value types, plays an important role in lightweight data modeling.Its design integrates compilation period verification, value semantic characteristics and object-oriented ideas, and is especially suitable for scenarios such as IoT device state management, UI component data encapsulation, etc.This article combines development practice to deeply analyze the key features and best practices of `struct`.


## 1. Scope rules and member design for struct type definition

### 1.1 Unique constraints for top-level scope
`struct` must be defined at the top-level scope of the source file, and nested definitions are prohibited inside functions or classes.This rule ensures global consistency in type visibility and avoids namespace pollution.

**Counterexample: Nested definitions cause compile error**
```typescript
func outerFunc() {
  struct InnerStruct { /*...*/ } // Error: struct must be at top level
}
```

### 1.2 Initialization strategy for member variables
#### Delay initialization of instance members
Instance member variables can be initialized in the constructor, or specified default values ​​when defined.Uninitialized member variables need to be assigned in the constructor, otherwise a compilation error will be triggered.

| **Initialization method** | **Applicable scenarios** | **Sample code** |
|--------------------|--------------------------------|-------------------------------------|  
| Constructor initialization | Dynamic values ​​of dependency parameters | `struct Point { var x: Int64; init(x: Int64) { this.x = x } }` |
| Assign value at definition | Fixed default value | `struct Size { let width = 100, height = 200 }` |

#### Initializer mechanism for static members
Static member variables need to be assigned through the static init initializer, and each `struct` is limited to one static initializer.

```typescript
struct MathConstants {
  static let PI: Float64
  static init() {
PI = 3.1415926535 // Initialization is completed during the compilation period
  }
}
```

### 1.3 Access control of member functions
Fine-grained permission control is achieved through the `public/private/internal/protected` modifier, with the default permission being `internal` (current package is visible).

**Cross-package access scenario**
```typescript
// public struct in package a
public struct User {
public var name: String // Public field
private var age: Int64 // Private field
}

// Access the User instance in package b
import a.*
let user = User(name: "Alice")
user.name = "Bob" // Legal: public members can access across packages
// user.age = 30 // Illegal: private member is not visible
```


## 2. Overload design and performance optimization of constructors

### 2.1 Selection of ordinary constructors and main constructors
#### Normal constructor: Flexible parameter verification
Suitable for scenarios where complex initialization logic or parameter conversion is required.

```typescript
struct Rectangle {
  var width: Int64
  var height: Int64
// Constructor with parameter verification
  public init(width: Int64, height: Int64) {
    guard width > 0 && height > 0 else {
throw InvalidSizeError() // Runtime verification
    }
    this.width = width
    this.height = height
  }
}
```

#### Main constructor: Syntax sugar simplified definition
Suitable for simple data modeling, parameters are mapped directly into member variables.

```typescript
// is equivalent to a normal constructor that defines a member variable of the same name
struct Point {
public Point(let x: Int64, let y: Int64) {} // Main constructor
}
let p = Point(x: 10, y: 20) // Direct initialization
```

### 2.2 Core rules for constructor overloading
The overloaded constructor must satisfy the differences in the number, type or order of parameters to avoid ambiguity.

**Legal overload example**
```typescript
struct Size {
  var width: Int64
  var height: Int64
// Single parameter structure (square)
  public init(side: Int64) {
    width = side
    height = side
  }
// Double parameter structure (rectangle)
  public init(width: Int64, height: Int64) {
    this.width = width
    this.height = height
  }
}
```

### 2.3 Conditions for automatically generating constructors
When all instance members have default values ​​and no custom constructors are not available, the compiler automatically generates a parameterless constructor.

```typescript
struct DefaultSize {
let width = 100 // with default value
let height = 200 // with default value
// Automatically generate init()
}
let size = DefaultSize() // Directly call the parameterless construct
```


## 3. Value type characteristics and practical constraints of mut functions

### 3.1 Analysis of copy behavior of value semantics
A copy is generated when the `struct` instance is assigned or passed, and the original instance is isolated from the copy status.

**Status isolation case**
```typescript
struct Counter {
  var count = 0
}
var c1 = Counter()
var c2 = c1 // Copy the instance
c1.count = 10 // Modifying c1 does not affect c2
print(c2.count) // Output: 0
```

### 3.2 Modification permission control of mut function
#### Syntax Requirements
The function that can modify instance members can be modified through the mut keyword, and `this` has special write permissions in the mut function.

```typescript
struct MutablePoint {
  var x: Int64, y: Int64
  public mut func move(dx: Int64, dy: Int64) {
x += dx // Legal modification
    y += dy
  }
}
var p = MutablePoint(x: 0, y: 0)
p.move(dx: 5, dy: 3) // Call the mut function to modify the instance
```

#### Restricted scenarios
- **The instance declared by the `let` prohibits calling the mut function**
  ```typescript
  let fixedPoint = MutablePoint(x: 0, y: 0)
// fixedPoint.move(dx: 1, dy: 1) // Error: The struct declared by let is immutable
  ```
- **Closure prohibits catching `this`** in mut function
  ```typescript
  struct Foo {
    public mut func f() {
let closure = { this.x = 1 } // Error: This is not captured
    }
  }
  ```

### 3.3 Comparison of core differences with class
| **Properties** | **struct (value type)** | **class (reference type)** |
|------------------|---------------------------|---------------------------|  
| Instance copy behavior | Deep copy (member value copy) | Shallow copy (reference address copy) |
| Modify instance members | mut function required (value type limitation) | Direct modification (reference type natural support) |
| Memory management | Stack allocation, automatic release | Heap allocation, dependency on GC |
| Applicable scenarios | Lightweight data, temporary status | Complex logic, state sharing |


## 4. Best practices for struct in architecture design

### 4.1 IoT device status modeling
Using the value semantic characteristics of `struct`, thread-safe transmission of device state is realized.

```typescript
// Equipment sensor data structure
struct SensorData {
let timestamp: Int64 // Timestamp (immutable)
var value: Float64 // Current value (variable)
  public mut func updateValue(newValue: Float64) {
value = newValue // mut function allows modification
  }
}

// Safe delivery in multi-threaded scenarios
let data = SensorData(timestamp: now(), value: 25.5)
let copyData = data // modify independently after copying
```

### 4.2 Immutable state management of UI components
Use `struct` to encapsulate the internal immutable state of the component in ArkUI, and combine `@State` to achieve responsive updates.

```typescript
@Entry
struct CardComponent {
// Immutable structure state
  let config = CardConfig(
    cornerRadius: 8,
    shadowOffset: Size(width: 2, height: 2)
  )
  @State private isHovered = false

  build() {
    Card()
      .radius(config.cornerRadius)
      .shadow(config.shadowOffset, color: isHovered ? Color.Black : Color.Transparent)
  }
}

//Configuration structure (all members are let)
struct CardConfig {
  let cornerRadius: Int64
  let shadowOffset: Size
}
```

### 4.3 Numerical type optimization in high-performance computing
High-precision numerical types are realized through `struct`, and value semantics are used to avoid race conditions brought about by shared states.

```typescript
// High-precision integers (avoid the loss of floating-point accuracy)
struct BigInt {
  private var digits: Array<Int64>
  public init(number: String) {
digits = number.map { Int64(String($0))! } // Characters to numbers array
  }
// Addition operation (return to new instance, no modification of the original data)
  public func add(other: BigInt): BigInt {
// Numerical addition logic, return a new BigInt instance
  }
}
```


## 5. Common traps and performance optimization suggestions

### 5.1 Alternatives to recursive definition
Recursive `struct` definition is prohibited, and hierarchical structures can be implemented indirectly through classes or enumerations.

**Counterexample: Recursive structure error**
```typescript
struct Node {
let child: Node // Error: Recursively reference itself
}
```

**Alternative: Use classes to implement tree structure**
```typescript
class Node {
  let value: Int64
  var children: [Node] = []
  init(value: Int64) { self.value = value }
}
```

### 5.2 Optimization of replication performance of large structures
For `struct` with more members, the replication overhead can be reduced in the following ways:
- **Use `inout` parameter**: Avoid copy generation when function arguments are passed
  ```typescript
  func updatePoint(inout point: Point, dx: Int64) {
point.x += dx // directly modify the original value
  }
  ```
- **Split into small structure**: Group fields by function to reduce the amount of data copied in a single time


## Conclusion
The design philosophy of `struct` is integrated into HarmonyOS Next's lightweight and high-reliability development philosophy.In actual projects, it is recommended to follow the following principles:
1. **Lightweight priority**: Use `struct` to model simple data (such as coordinates, configuration items), and the class is used for complex logic;
2. **Immutable priority**: Try to use `let` to declare member variables, and explicitly mark mutability through the mut function;
3. **Compilation period verification priority**: Use constructor overloading and access modifiers to expose design defects during the compilation period.

By deeply understanding the value semantic characteristics and compilation rules of `struct`, developers can build a safer and more efficient data model in HarmonyOS Next, especially in resource-constrained IoT devices and high-performance computing scenarios, fully unleashing the system potential of HarmonyOS Next.
