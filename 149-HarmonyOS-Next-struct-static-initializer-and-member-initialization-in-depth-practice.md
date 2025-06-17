
# HarmonyOS Next struct static initializer and member initialization in-depth practice

In HarmonyOS Next development, the static initializer (`static init`) and member initialization mechanism of `struct` are the core functions for realizing type-level data initialization.By rationally applying these features, developers can complete the configuration of static members during the compilation period or early stages to ensure consistency of type state.This article is based on the document "0010 Creating a struct instance - Struct Type - Cangjie Programming Language Development Guide - Learning Cangjie Language.docx", and analyzes the rules of static initializers and the best practices for member initialization in detail.


## 1. Definition and initialization rules of static initializer

### 1.1 Syntax Structure of Static Initializer
The static initializer is declared as static init, which is used to initialize static member variables that are not assigned at definition, and each struct is allowed to define at most one.
```typescript  
struct Geometry {  
static let PI: Float64 // Uninitialized static member
static let DEFAULT_SIZE = 10 // Static member assigned when defined
  static init() {  
PI = 3.1415926535 // Initialize unassigned static members
  }  
}  
```  

### 1.2 Initialization order and dependency relationship
The initialization order of static members follows the definition order, and only static members can be operated in the initializer, and access to instance members is prohibited.
```typescript  
struct StaticOrder {  
static let A = computeA() // Define first, initialize first
static let B = computeB() // Post definition, post initialization
  static init() {  
// A and B can be accessed, but instance members cannot be accessed
  }  
  static func computeA() -> Int64 { return 1 }  
static func computeB() -> Int64 { return A + 1 } // Legal: References to an initialized static member
}  
```  

### 1.3 Prohibited behavior of the initializer
- Disable modifier: Static initializers cannot use `public/private` and other access modifiers.
- Disable instance operations: Cannot create instances or call instance member functions in the initializer.
  ```typescript  
  struct ErrorInit {  
    static init() {  
let instance = ErrorInit() // Error: The creation of an instance is prohibited in the static initializer
    }  
  }  
  ```  


## 2. Initialization method of static member variables

### 2.1 Direct assignment during definition
A static constant suitable for value determination during compile time without additional initialization logic.
```typescript  
struct MathConstants {  
static let E = 2.71828 // Compilation period constant
static let GRAVITY = 9.8 // Fixed value
}  
```  

### 2.2 Static initializer assignment
Suitable for scenarios where complex calculations are required or depend on other static members.
```typescript  
struct ComplexConstants {  
  static let BASE = 100  
  static let DERIVED_VALUE: Int64  
  static init() {  
DERIVED_VALUE = BASE * 2 // Depend on BASE value
  }  
}  
```  

### 2.3 Access methods for static members
Direct access through type names, no need to create instances, suitable for global shared data.
```typescript  
print(Geometry.PI) // Output: 3.1415926535
let size = Geometry.DEFAULT_SIZE // Static member assigned when accessing the definition
```  


## 3. Initialization strategy of instance member variables

### 3.1 Constructor initialization
Assign values ​​to instance members in the constructor, supporting dynamic calculations or parameter verification.
```typescript  
struct Rectangle {  
  let width: Int64  
  let height: Int64  
  public init(width: Int64, height: Int64) {  
    guard width > 0 && height > 0 else {  
throw InvalidSizeError() // Runtime parameter verification
    }  
    self.width = width  
    self.height = height  
  }  
}  
```  

### 3.2 Assign value when defining
Set default values ​​for members to simplify the instance creation process.
```typescript  
struct Point {  
let x = 0 // The default value is 0
  let y = 0  
}  
let origin = Point() // Initialize with default values
```  

### 3.3 Simplified initialization of the main constructor
The parameters are mapped directly into member variables through the main constructor, and the manual assignment code is omitted.
```typescript  
struct Size {  
public Size(let width: Int64 = 100, let height: Int64 = 200) {} // Main constructor
}  
let defaultSize = Size() // Use default parameters
let customSize = Size(width: 150) // Overwrite some parameters
```  


## 4. Collaborative application of static members and instance members

### 4.1 Hierarchical design of global configuration and instance configuration
- **Static Member**: Stores global default configurations (such as system-level parameters).
- **Instance Member**: Stores personalized configurations (such as user-defined parameters).
```typescript  
struct AppConfig {  
// Static default configuration
  static let DEFAULT_FONT_SIZE = 14  
  static let DEFAULT_THEME = "light"  
// Instance configuration
  var fontSize: Int64  
  var theme: String  
  public init() {  
fontSize = AppConfig.DEFAULT_FONT_SIZE // Load the default value
    theme = AppConfig.DEFAULT_THEME  
  }  
  public mut func updateTheme(theme: String) {  
self.theme = theme // Dynamically modify instance configuration
  }  
}  
```  

### 4.2 Separation of constants and calculations of mathematical tool library
```typescript  
struct GeometryUtils {  
// Static constants
  static let PI = 3.14159  
// Example function: Calculate the circle area
  public func calculateArea(radius: Float64) -> Float64 {  
return GeometryUtils.PI * radius * radius // Call static constants
  }  
}  
let calculator = GeometryUtils()  
let area = calculator.calculateArea(radius: 5.0)  
```  

### 4.3 Static counter for counting the number of instance creations
```typescript  
struct InstanceCounter {  
static var count = 0 // Static statistics member
  public init() {  
InstanceCounter.count += 1 // Update static members in the constructor
  }  
}  
let c1 = InstanceCounter()  
let c2 = InstanceCounter()  
print(InstanceCounter.count) // Output: 2
```  


## 5. Common Errors and Best Practices

### 5.1 Instance Operation in Static Initializer
**Error case**: Access instance members or create instances in a static initializer.
```typescript  
struct ErrorStaticAccess {  
var instanceVar = 0 // Instance member
  static init() {  
let instance = ErrorStaticAccess() // Error: Disable instance creation
print(instance.instanceVar) // Error: Disable access to instance members
  }  
}  
```  

**Solution**: The static initializer operates only static members, and the instance logic is moved to the constructor or member function.

### 5.2 Compilation error for uninitialized static members
**Error Case**: Uninitialization of all static members causes compilation failure.
```typescript  
struct UninitializedStatic {  
static let VALUE: Int64 // Not initialized
// static init() { /* VALUE not assigned */ } // Error: VALUE not initialized
}  
```  

**Solution**: Assign values ​​to all uninitialized static members in the static initializer.

### 5.3 Thread safety assurance for static members
HarmonyOS Next ensures thread safety for static initializers and can be used in multithreaded scenarios with confidence.
```typescript  
struct ThreadSafeConfig {  
  static let GLOBAL_SETTINGS: Settings  
  static init() {  
GLOBAL_SETTINGS = Settings.loadFromDisk() // Safe initialization in multithreaded environment
  }  
}  
```  


## 6. Performance optimization and design principles

### 6.1 Performance advantages of compile period constants
Declare the static members of the determined value as compile-time constants (such as `const`) to improve access efficiency.
```typescript  
const struct FixedConfig {  
static let VERSION = "1.0.0" // Compile period constant
}  
```  

### 6.2 Avoid cyclic dependencies of static members
Ensure that the initialization order of static members does not form a loop, otherwise a compilation error will be triggered.
```typescript  
struct CircularDependency {  
static let A = B.value + 1 // Depend on B
static let B = A.value - 1 // Depend on A to form a loop
}  
// Error: Static member initialization order circular dependency
```  

### 6.3 Naming specifications for static members
- Static constants: all capital or `k` prefix (such as `kMaxSize/DEFAULT_VALUE`).
- Static variables: camel nomenclature (such as `sharedInstance/currentSettings`).
```typescript  
struct Constants {  
  static let kDefaultTimeout = 5000  
  static var currentLanguage = "en-US"  
}  
```  


## Conclusion
The static initializer and member initialization mechanism of `struct` is the key to implementing type-level logic in HarmonyOS Next.By rationally designing the initialization method of static members and combining the dynamic configuration of instance members, developers can build clear-level, efficient and secure data models.In practice, attention should be paid to:
1. **Responsibilities of static members**: Focus on type-level constants, configurations, or statistics to avoid complex logic;
2. **Initialization order**: Ensure that static members are initialized in the defined order to avoid circular dependencies;
3. **Thread Safety**: Use the static initialization thread safety guaranteed by the system to simplify multi-thread scenario development.

By mastering these features, you can efficiently manage the global status in Hongmeng applications, especially in tool library, configuration center and other scenarios, and give full play to the global sharing advantages of static members.
