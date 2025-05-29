
# HarmonyOS Next const function and constant evaluation: Compilation period optimization and type safety design

> This article aims to deeply explore the technical details of Huawei HarmonyOS Next system and summarize them based on actual development practices.It is mainly used as a carrier of technology sharing and communication, and it is inevitable to miss mistakes. All colleagues are welcome to put forward valuable opinions and questions in order to make common progress.This article is original content, and any form of reprinting must indicate the source and original author.


## 1. Const's "compilation contract": Static calculation from variables to functions

In the Cangjie language of HarmonyOS Next, the `const` keyword is used to mark entities that can be evaluated during the compilation period, including variables, functions, and constructors.This feature reduces runtime overhead by calculating expression values ​​in advance while ensuring type safety.

### 1.1 const variable: "immutable constant" during the compilation period
The `const` variable must be initialized at definition time, and the initialization expression must be **const expression** (such as literals, arithmetic operations, enumeration constructors, etc.).

**Example: Physical Constant Definition**
```typescript
const G = 6.67430e-11  // 万有引力常数，编译期求值
const PI = 3.1415926535

struct Planet {
  const init(mass: Float64, radius: Float64) {
    this.mass = mass
    this.radius = radius
  }
  const func surfaceGravity(mass: Float64): Float64 {
// Calculate gravity acceleration during compilation
    return G * mass / (radius * radius)
  }
}

// Initialize const variable during compilation
const earth = Planet(mass: 5.972e24, radius: 6.371e6)
const gravity = earth.surfaceGravity(earth.mass) // Compile period calculation result
```

### 1.2 "Whitelist" rule for const expression
Not all expressions can be used in the `const` context and the following conditions are met:
- All operands are `const` expressions (such as literals, `const` variables, enumeration constructors);
- No side effects (such as I/O operations, modification of global status);
- Call only the `const` function or the enumeration constructor.

**Comparison of legal and illegal scenarios**
| **Legal Scene** | **Illegal Scene** |
|--------------------------|--------------------------------|
| `const a = 1 + 2 * 3` | `const b = random()` (runtime function) |
| `const c = [1, 2, 3]` | `const d = var x = 0` (variable declaration) |
| `const e = MyEnum.Value` | `const f = this.someVar` (inst member) |


## 2. Const function: "pure function" abstraction during compilation period

### 2.1 "Purity" requirements for const function
The `const` function must be a pure function**, i.e.:
- Rely on only input parameters and `const` variables;
- No side effects (no external state modification, no non-const function is called);
- All expressions are `const` expressions.

**Example: Const function for geometric calculation**
```typescript
struct Point {
  const init(x: Float64, y: Float64) {
    this.x = x
    this.y = y
  }
// Calculate two points of distance during compilation
  const func distance(to other: Point): Float64 {
    let dx = x - other.x
    let dy = y - other.y
    return sqrt(dx * dx + dy * dy)
  }
}

// Calculate distance during compilation
const p1 = Point(x: 3, y: 4)
const p2 = Point(x: 0, y: 0)
const dist = p1.distance(to: p2) // The result is 5, the compilation period is determined
```

### 2.2 "Dual Mode" Call of Const Function and Ordinary Functions
The `const` function performs compilation calculations in the `const` context (such as `const` variable initialization) and is executed when running as a normal function in a non-const` context.

**Example: Dynamic calculation at runtime**
```typescript
func calculateDistance(a: Point, b: Point): Float64 {
return a.distance(to: b) // Call the const function at runtime
}

@Entry
struct DistanceApp {
  @State private pointA = Point(x: 0, y: 0)
  @State private pointB = Point(x: 0, y: 0)

  build() {
    Column {
// Calculate distance during runtime
      Text("Distance: \(calculateDistance(pointA, pointB))")
    }
  }
}
```


## 3. Const constructor: initialization of custom types during compilation

### 3.1 Const initialization of struct
`struct` defines a `const init` constructor, allowing instances to be created during compilation, and all member variables must be of type `const` (or value type).

**Example: Compilation period configuration item**
```typescript
struct Config {
  const init(
    timeout: Int64 = 1000,
    retryCount: Int64 = 3
  ) {
    this.timeout = timeout
    this.retryCount = retryCount
  }
  const var timeout: Int64
  const var retryCount: Int64
}

// Create a Config instance during the compilation period
const defaultConfig = Config()
const customConfig = Config(timeout: 2000, retryCount: 5)
```

### 3.2 class const restrictions
If the `class` type is defined as `const init`, it must meet:
- All instance members are declared `const` or `let` (cannot contain `var`);
- The parent class must provide a `const init` constructor.

**Counterexample: class containing var members cannot define const init**
```typescript
class Counter {
var count: Int64 = 0 // Contains var members, cannot define const init
// const init() { ... } Compilation error
}
```


## 4. Practical optimization: The application of const in high-performance scenarios

### 4.1 Pre-calculation of compilation period of mathematical formulas
In scientific calculations, graphic rendering and other scenarios, use the `const` function to pre-calculate the constant to avoid repeated calculations at runtime.

**Example: Fourier transform coefficient calculation**
```typescript
const PI_2 = 2.0 * PI // Compile period calculation

const func fourierCoefficient(n: Int64, x: Float64): Float64 {
return cos(PI_2 * n * x) // Expand during the compilation period to calculate the specific numerical value
}

// Use the compilation results directly at runtime
let result = fourierCoefficient(1, 0.5)
```

### 4.2 Compilation period verification of enum types
Use the `const` function to verify the enum value during compilation period to ensure input legitimacy.

```typescript
enum HttpMethod {
  Get,
  Post,
  Put,
  Delete
}

const func isValidMethod(method: HttpMethod): Bool {
  return method == .Get || method == .Post || method == .Put || method == .Delete
}

// Compilation period verification
const method: HttpMethod = .Post
if !isValidMethod(method) { // The compilation period is determined to true, and the conditional branch is optimized
  error("Invalid method")
}
```


## 5. Restrictions and avoidance of pits: "Border Conditions" of const

### 5.1 "Runtime Compromise" for Dynamic Data
If the data needs to be obtained at runtime (such as user input or network request), `const` cannot be used and it needs to be degenerated into runtime logic.

**Counterexample: Runtime data cannot be used in const context**
```typescript
func getRuntimeValue(): Int64 {
return 42 // Runtime function, not used for const
}

// const value = getRuntimeValue() compile error
```

### 5.2 "Type Constraints" between generics and const
If a generic function needs to be used as a `const` function, you need to ensure that the type parameters meet the `const` expression requirements (such as numeric types, enums, etc.).

```typescript
const func genericConst<T: Number>(x: T, y: T): T {
return x + y // legal only if T is a numeric type
}

// Legal call: T=Int64
const sum = genericConst(1, 2)  
// Illegal call: T=String (non-numeric type)
// const strSum = genericConst("a", "b") 
```


## Conclusion: Const's "Compilation Revolution" and Architectural Design

The `const` feature is an important innovation in performance optimization and type safety of HarmonyOS Next. By advanced deterministic behavior to the compilation period, it not only improves operational efficiency but also reduces runtime errors.In architectural design, it is recommended:
1. **Separate the compile period and runtime logic**: Encapsulate unchanged configurations, mathematical formulas, etc. into `const` entities;
2. **Preferential use of struct**: For simple data models, use `const init` to achieve initialization during the compilation period;
3. **Treat side effects with caution**: Ensure that the `const` function is absolutely pure and avoid implicit dependence on runtime state.

By rationally using `const`, developers can build more efficient and secure code bases in Hongmeng applications, especially in performance-sensitive scenarios such as IoT devices and embedded systems, which fully release the potential for compilation period optimization.
