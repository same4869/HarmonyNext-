
# HarmonyOS Next closure and operator overload comprehensive combat: from basic rules to architectural design

> This article aims to deeply explore the technical details of Huawei HarmonyOS Next system and summarize them based on actual development practices.It is mainly used as a carrier of technology sharing and communication, and it is inevitable to miss mistakes. All colleagues are welcome to put forward valuable opinions and questions in order to make common progress.This article is original content, and any form of reprinting must indicate the source and original author.


## 1. Analysis of the "rule crossover" scenario of closure and operator overload

In the Cangjie language of HarmonyOS Next, there are special interaction scenarios for the variable capture rules of closures and the operator overloading mechanism.Understanding the intersection of these rules can help developers avoid traps in complex scenarios.

### 1.1 Closure capture in operator overload function
When operator overloads functions (such as `operator func +`) define closures internally, the closure variable capture rules must be followed.For example, in the `+` operator implementation of the `Point` structure, a closure can capture member variables of a struct instance.

```typescript
struct Point {
  var x: Int64, y: Int64
  public operator func +(right: Point): Point {
// Closure captures the x/y member of the current instance
    let offset = { => Point(x: this.x + right.x, y: this.y + right.y) }
    return offset()
  }
}

// Use scenario: Addition of coordinates
let p1 = Point(x: 1, y: 2)
let p2 = Point(x: 3, y: 4)
let p3 = p1 + p2 // Call the operator overload function, and the closure correctly captures member variables
```

### 1.2 Calling operators in closures overload functions
Custom operator overload functions can be called normally within the closure, and their behavior is consistent with ordinary function calls.For example, use the custom `-` operator in a closure to invert the coordinates.

```typescript
struct Point {
  public operator func -(): Point {
    return Point(x: -this.x, y: -this.y)
  }
}

func createInverter(): (Point) -> Point {
return { point in -point } // Call unary operator overload function in closure
}

let invert = createInverter()
let p = Point(x: 5, y: 10)
println(invert(p)) // Output: Point(x: -5, y: -10)
```


## 2. Typical application scenarios of closures in operator overloading

### 2.1 Dynamic operator logic encapsulation
Dynamically generate operator overload functions by closures to realize the configurable operator behavior at runtime.For example, switch the logic of adding coordinates (normal addition or weighted addition) according to different scenarios.

```typescript
enum AddMode {
  Normal,
  Weighted(Float64)
}

func createAddOperator(mode: AddMode): (Point, Point) -> Point {
  switch mode {
  case .Normal:
return { a, b in Point(x: a.x + b.x, y: a.y + b.y) } // Normal addition closure
  case .Weighted(let factor):
    return { a, b in 
      Point(
        x: (a.x * factor + b.x).toInt(), 
        y: (a.y * factor + b.y).toInt()
) // Weighted addition closure
    }
  }
}

//Usage scenario: Dynamically switch addition mode
let normalAdd = createAddOperator(mode: .Normal)
let weightedAdd = createAddOperator(mode: .Weighted(0.5))

println(normalAdd(Point(1, 2), Point(3, 4))) // Output: Point(4, 6)
println(weightedAdd(Point(1, 2), Point(3, 4))) // Output: Point(2, 3) (1*0.5+3=3.5→3, 2*0.5+4=5→5? Pay attention to type conversion)
```

### 2.2 Performance optimization of operator overloading and closures
In high-frequency operation scenarios, the cache characteristics of the closure are used to optimize operator calculations.For example, pre-calculate the inverse operator logic of matrix transformations to avoid repeated calculations.

```typescript
class Matrix {
  var data: Array<Float64>
  public operator func inverse(): Matrix {
// Assuming that the inverse matrix is ​​complicated, the results are cached using closures
    var cachedInverse: Matrix?
    return {
      if let inverse = cachedInverse { return inverse }
// Actual inverse matrix calculation logic (simplified example)
      let inverse = Matrix(data: self.data.map { -$0 })
      cachedInverse = inverse
      return inverse
    }()
  }
}
```


## 3. "Restricted Intersection" and Pit avoidance of Closures and Operator Overload

### 3.1 Conflict between mutable variable capture and operator overloading
If the operator overloads the closure inside the function to capture the `var` variable, the closure is subject to escape restrictions and cannot be used as a return value or parameter of the operator function.

**Error Example: Operator function returns closure that captures `var`**
```typescript
struct Point {
  public operator func *(scalar: Int64): Point {
var factor = scalar // variable variables
// Error: Closure captures var variable, cannot return value as operator function
    return { Point(x: this.x * factor, y: this.y * factor) } 
  }
}
```

**Correct example: Use `let` variable or class instance**
```typescript
struct Point {
  public operator func *(scalar: Int64): Point {
let factor = scalar // immutable variable, closures can escape
    return { Point(x: this.x * factor, y: this.y * factor) }()
  }
}
```

### 3.2 Cooperator priority and closure logic
Operator overloading will not change the native priority. If the closure contains complex operations, the order must be specified explicitly in brackets.

```typescript
struct Vector {
  public operator func +(right: Vector): Vector { /* ... */ }
  public operator func *(scalar: Float64): Vector { /* ... */ }
}

let v = Vector() + Vector() * 2.0 // is equivalent to v + (Vector() * 2.0), meeting native priority
```


## 4. Architectural design: a collaborative mode of closure and operator overloading

### 4.1 Domain-specific language (DSL) construction
Define domain semantics through operator overloading, combine closures to implement dynamic logic, and build a concise DSL.For example, define transformation operations in graphical rendering DSL.

```typescript
// Define coordinate transformation operator
struct Transform {
  public static operator func <<(transform: (Point) -> Point, point: Point): Point {
    return transform(point)
  }
}

// Closure definition specific transformation logic
let translate = { (p: Point) -> Point in Point(x: p.x + 10, y: p.y + 10) }
let scale = { (p: Point) -> Point in Point(x: p.x * 2, y: p.y * 2) }

// Use DSL combination transformation
let finalTransform = translate << scale // Scale first and then pan
let point = Point(x: 1, y: 1)
println(finalTransform(point)) // Output: Point(x: 1*2+10=12, y: 1*2+10=12)
```

### 4.2 Operator extension in plug-in architecture
Implemented by closure dynamic registration operator, it supports loading different operation logic plug-ins at runtime.For example, in financial calculation, dynamically switch the exchange rate calculation method.

```typescript
protocol CurrencyOperator {
  func calculate(base: Float64, target: Float64): Float64
}

func registerAddOperator(plugin: () -> CurrencyOperator) {
// Closure captures plug-in instances to implement dynamic operator expansion
  let operatorClosure = plugin()
  operator func +(a: Float64, b: Float64): Float64 {
    return operatorClosure.calculate(base: a, target: b)
  }
}

// Plugin example: Addition plugin
registerAddOperator {
  struct AddPlugin: CurrencyOperator {
    func calculate(base: Float64, target: Float64) -> Float64 {
      return base + target
    }
  }
  return AddPlugin()
}

let result = 100.0 + 50.0 // Call dynamically registered addition operator
```


## 5. Performance optimization: Coordinated optimization of closures and operator overloading

### 5.1 Avoid repeated calculations in closures
In operator overloading functions, the unchanged computational logic is moved outside the closure, reducing runtime overhead.

**Pre-optimization**
```typescript
struct Complex {
  public operator func *(other: Complex): Complex {
// Repeat calculation of the module length
    let magnitude = sqrt(this.re * this.re + this.im * this.im)
    return {
      Complex(
        re: this.re * other.re - this.im * other.im,
        im: this.re * other.im + this.im * other.re
      )
    }()
  }
}

**Optimized**
```typescript
struct Complex {
  public operator func *(other: Complex): Complex {
// Calculate the module length in advance
    let magnitude = sqrt(this.re * this.re + this.im * this.im)
    let re = this.re * other.re - this.im * other.im
    let im = this.re * other.im + this.im * other.re
return Complex(re: re, im: im) // Return the calculation result directly to avoid closure overhead
  }
}
```

### 5.2 Optimize operators using compile-time closures
For mathematical formula class operators, use the `const` closure to complete pre-calculation during the compilation period to improve runtime performance.

```typescript
const func compileTimeMultiply(factor: Int64): (Int64) -> Int64 {
return { x in x * factor } // Generate multiplication closure during compilation
}

// Determine multiplication factor during compilation
const double = compileTimeMultiply(2)
let result = double(5) // The code generated during the runtime is directly executed, and the result is 10
```


## Conclusion: Rules-driven Hongmeng Development Paradigm

The combination of closures and operator overload reflects the characteristics of "rule-first, declarative programming" in HarmonyOS Next development.Developers need:
1. **Strictly follow the capture rules**: Ensure the legitimacy of closures in operator overloading functions;
2. **Priority immutable design**: Avoid escape restrictions through `let` variables and reference types;
3. **Combined with compile-time optimization**: Use `const` closure and operator overload to improve performance.

By combining the flexibility of closures with the expressive power of operator overloading, efficient and easy-to-maintain domain-specific logic can be built in Hongmeng applications, providing powerful tool support for collaborative development of multiple devices.
