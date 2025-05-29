
# HarmonyOS Next struct static initializer and member functions practice guide

In HarmonyOS Next, the static initializer and member functions of `struct` are the core mechanisms for implementing type-level logic and instance operations.The former is used to initialize static members, while the latter provides rich instance operation capabilities.This article combines development practice to deeply analyze its design rules and best application scenarios.


## 1. Static initializer: type-level initialization logic

### 1.1 Initialization rules for static members
Static member variables need to be assigned through the `static init` initializer, and all uninitialized static members must be assigned, otherwise an error will be reported in the compilation.

**Example: Geometric constant initialization**
```typescript  
struct Geometry {  
static let PI: Float64 // Uninitialized static member
static let DEFAULT_LENGTH: Int64 = 10 // Assign value when declaring, no initializer is required
  static init() {  
PI = 3.1415926535 // Initialize unassigned static members
  }  
}  
```  

### 1.2 Singleton of static initializer
Each `struct` allows to define at most one static initializer, and repeated definitions will trigger a compilation error.

**Counterexample: Repeat definition of initializer**
```typescript  
struct ErrorExample {  
  static let VALUE: Int64  
  static init() { VALUE = 10 }  
static init() { VALUE = 20 } // Error: Repeat definition of static initializer
}  
```  

### 1.3 Access methods for static members
Static members are directly accessed by type names without creating instances, suitable for globally shared configurations or constants.

```typescript  
struct Config {  
  static let TIMEOUT: Int64 = 5000  
  static init() {  
// It can be further optimized in combination with compiled constants
  }  
}  
//Usage scenario: Network request timeout configuration
let timeout = Config.TIMEOUT // Access directly through type name
```  


## 2. Member functions: the core carrier of instance operations

### 2.1 Differences between instance member functions and static member functions
| **Properties** | **Instance member functions** | **Static member functions** |
|------------------|-----------------------------|---------------------------|  
| Access | Call via instance (`instance.func()`) | Call via type name (`Type.func()`) |
| Member access | Access to instance members and static members | Access to static members only |
| this keyword | point to the current instance | `this` cannot be used |

**Example: Implementation of two member functions**
```typescript  
struct MathOps {  
// Instance function: calculates the square of an instance
  public func square() -> Int64 {  
return this.value * this.value // Access instance members
  }  
// Static function: calculate the global maximum value
  public static func max(a: Int64, b: Int64) -> Int64 {  
return a > b ? a : b // Access only static logic
  }  
}  
let ops = MathOps(value: 5)  
let result = ops.square() // Instance function call
let maxValue = MathOps.max(a: 10, b: 20) // Static function call
```  

### 2.2 mut function: the modification portal of value type
#### Syntax Requirements
Functions that allow modification of instance members through the mut keyword, where `this` has special write permissions.

```typescript  
struct Counter {  
  var count: Int64 = 0  
  public mut func increment() {  
count += 1 // Legally modify the instance member
  }  
}  
var counter = Counter()  
counter.increment() // Call mut function to modify the value
```  

####User Limitations
- **The instance declared by the `let` prohibits calling the mut function**
  ```typescript  
  let fixedCounter = Counter()  
// fixedCounter.increment() // Error: The instance declared by let is immutable
  ```  
- **Closure prohibits catching `this`** in mut function
  ```typescript  
  struct Foo {  
    public mut func f() {  
let closure = { this.count = 1 } // Error: This is not captured
    }  
  }  
  ```  

### 2.3 Implementation of mut function in interface
When `struct` implements the mut function in the interface, the same `mut` modifier must be maintained, and this modification is not required when `class` is implemented.

```typescript  
interface Mutable {  
  mut func update(value: Int64)  
}  
struct MutStruct : Mutable {  
public mut func update(value: Int64) { /*...*/ } // Mut must be added
}  
class MutClass : Mutable {  
public func update(value: Int64) { /*...*/ } // No mut (reference type is naturally mutable)
}  
```  


## 3. Advanced application scenarios of member functions

### 3.1 Chain call design of instance member functions
By designing the mut function that returns `this`, chain operations are implemented and code readability is improved.

```typescript  
struct Point {  
  var x: Int64, y: Int64  
  public mut func moveX(dx: Int64) -> Self {  
    x += dx  
return this // Return this current instance
  }  
  public mut func moveY(dy: Int64) -> Self {  
    y += dy  
    return this  
  }  
}  
var p = Point(x: 0, y: 0)  
p.moveX(dx: 5).moveY(dy: 3) // Chain call, final coordinates (5, 3)
```  

### 3.2 Tool-based encapsulation of static member functions
Encapsulate general algorithms or verification logic into static functions to avoid duplicate code.

```typescript  
struct Validation {  
  public static func isEmailValid(_ email: String) -> Bool {  
// Email format verification logic
    let pattern = "^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}$"  
    return Regex(pattern).matches(email)  
  }  
}  
// Use scenario: Registration page verification
if Validation.isEmailValid("user@example.com") {  
// Legal email processing
}  
```  

### 3.3 Combining static initializer with singleton mode
Take advantage of the uniqueness of static members to implement a lightweight singleton configuration center.

```typescript  
struct AppConfig {  
  static let instance: AppConfig  
  let theme: Theme  
  static init() {  
// Load configuration files during compilation (simplified example)
    instance = AppConfig(theme: Theme.default)  
  }  
  private init(theme: Theme) {  
    self.theme = theme  
  }  
}  
// Use: let currentTheme = AppConfig.instance.theme // Globally unique instance
```  


## 4. Common Errors and Best Practices

### 4.1 Thread safety issues for static members
When the static initializer is executed for the first time, you need to pay attention to the initialization security in a multi-threaded environment (HarmonyOS Next ensures thread safety for static initialization).

**Best Practice**
```typescript  
struct ThreadSafeConfig {  
  static let GLOBAL_SETTINGS: Settings  
  static init() {  
// Initialization logic can contain file reads or network requests (make thread safe)
    GLOBAL_SETTINGS = Settings.loadFromDisk()  
  }  
}  
```  

### 4.2 Side effects control of mut function
Avoid executing time-consuming operations or global side effects in the mut function, and maintain its simplicity of responsibility.

**Counterexample: I/O operations are performed in mut function**
```typescript  
struct FileWriter {  
  public mut func write(data: String) {  
FileSystem.write(to: "path.txt", data: data) // Time-consuming operation, should be encapsulated into independent functions
  }  
}  
```  

### 4.3 Naming specifications for member functions
- The instance function starts with a verb (such as `mov/validate/update`)
- Static functions start with noun phrases or verb phrases (such as `calculateMax/isValid`)

**Recommended Naming**
```typescript  
struct StringUtils {  
public static func capitalize(_ str: String) -> String { /*...*/ } // Static tool function
public func trimWhitespace() -> String { /*...*/ } // Instance operation function
}  
```  


## Conclusion
The static initializer and member functions of `struct` are key components in HarmonyOS Next to implement type-level logic and instance operations.In development, it is recommended:
1. **Static member priority**: Encapsulate global configurations, constants, or tool functions into static members to reduce instance overhead;
2. **mut function minimization**: Only mark the mut function when necessary, and priority is given to implementing immutable design by returning new instances;
3. **Interface consistency**: When implementing interfaces across types (struct/class), pay attention to the compatibility of mut modifiers.

By rationally applying these features, developers can build a data operation system with clear structure and efficient performance in Hongmeng applications, especially in tool library, configuration management and other scenarios, to give full play to the lightweight advantages of `struct`.
