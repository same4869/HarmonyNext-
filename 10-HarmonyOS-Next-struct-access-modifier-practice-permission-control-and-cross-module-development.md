
# HarmonyOS Next struct access modifier practice: permission control and cross-module development

In HarmonyOS Next development, the access modifier of `struct` is the core mechanism that controls member visibility.Through the four modifiers of `private/internal/protected/public`, data encapsulation and interface exposure can be accurately managed, especially in cross-module collaboration and component development.This paper combines development practice to analyze the scope rules and typical application scenarios of access modifiers.


## 1. Scope rules for access modifiers

### 1.1 Comparison of Level 4 Permission Models
| **Modifier** | **Scope** | **Typical Scenarios** |
|--------------|--------------------------------------------------------------------------|--------------------------------|  
| `private` | Only visible in the `struct` definition | Hide implementation details (such as temporary calculation fields) |
| `internal` | Current package and subpackage are visible (default modifier) ​​| Shared members within the module |
| `protected` | Current module is visible (module dependencies need to be configured) | Member protection of the inheritance system within the module (although `struct` does not support inheritance, but can be used for in-module restrictions) |
| `public` | Visible inside and outside the module | Exposed API interface |

**Note**: The default permission of the `struct` member is `internal`, and cross-packet access requires explicit declaration of `public`.

### 1.2 Compilation period verification for cross-packet access
#### In-package access (default `internal`)
```typescript  
// struct in package a
struct InternalData {  
var internalField: String = "visible in the package" // Default internal modification
}  
// Functions in package a can be accessed directly
func packageAFunc() {  
  let data = InternalData()  
print(data.internalField) // Legal
}  
```  

#### Cross-packet access (requires `public` modification)
```typescript  
// The public struct in package b refers to package a
import a.*  
struct PublicData {  
public var publicField: String = "visible across packages"
}  
// In-package b functions access public members
func packageBFunc() {  
  let data = PublicData()  
print(data.publicField) // Legal
// print(data.internalField) // Error: Internal members are not visible across packages
}  
```  


## 2. Member-level authority control practice

### 2.1 Field encapsulation: Hide implementation details
Encapsulate sensitive fields or intermediate calculation results within `struct` via the `private` modifier, exposing only the necessary interfaces.

**Example: Financial calculation structure**
```typescript  
struct FinancialCalculator {  
private var principal: Float64 // principal (private field)
public var rate: Float64 // Interest rate (public field)
  public init(principal: Float64, rate: Float64) {  
self.principal = principal // Internal initialization
    self.rate = rate  
  }  
  public func calculateInterest() -> Float64 {  
return principal * rate // public interface access private fields
  }  
}  
let calculator = FinancialCalculator(principal: 10000, rate: 0.05)  
print(calculator.calculateInterest()) // Legal: Call the public method
// print(calculator.principal) // Error: The private field is not visible
```  

### 2.2 Constructor permission control
Implement factory pattern or singleton logic by limiting the scope of the constructor's call through modifiers.

**Example: Singleton Structure (Limiting External Construction)**
```typescript  
struct Singleton {  
  public static let instance = Singleton()  
private init() { // Private constructor, prohibit external instantiation
// Initialization logic
  }  
  public func doSomething() {  
// Singleton method
  }  
}  
// Use: let instance = Singleton.instance // Legal
// let direct = Singleton() // Error: The private constructor is not callable
```  

### 2.3 Permission rating of member functions
Apply different modifiers to member functions to control the visibility of operations and the calling scope.

```typescript  
struct NetworkClient {  
public func connect() { /* Public connection interface */ }
internal func sendRequest() { /* request logic within module */ }
private func parseResponse() { /* private parse logic */ }
}  
```  


## 3. Frequently Asked Questions in Cross-Module Development

### 3.1 Module dependency and `protected` modifier
The `protected` modifier is used to restrict members to be visible only in the current module and is suitable for scenarios where cross-package but not public in modular development.

**Scenario**: The basic components in module `a` need to be used by the subpackage of module `a`, but other modules are prohibited from accessing.
```typescript  
// struct in module a
protected struct BaseComponent {  
protected func setup() { /* Initialization logic within the module */ }
}  
// The subpackage of module a can inherit or call setup()
// Module b cannot access BaseComponent and setup()
```  

### 3.2 Stability design of public interface
`public` members need to be carefully designed to avoid frequent modifications that lead to dependency conflicts between modules.Recommended practices:
1. Expose abstract types (such as `interface`) through the `public` interface instead of concrete `struct`
2. When using the `public` modifier, provide documentation to explain the purpose of the interface

```typescript  
// Recommended: Public interface returns abstract type
public interface DataLoader {  
  func load() -> Data  
}  
public struct FileLoader : DataLoader {  
  public func load() -> Data { /*...*/ }  
}  
```  

### 3.3 Cooperation between access modifier and value type characteristics
When passing the value type `struct` across packages, you need to pay attention to:
- `public` modified `struct` and its `public` members can be accessed across packages
- Non-public members cannot be accessed across packages even if they are included in `public struct`

```typescript  
public struct PublicStruct {  
var internalField: String = "Internal Field" // Default internal, not visible across packages
public var publicField: String = "public field"
}  
// Cross-packet access
let str = PublicStruct()  
print(str.publicField) // Legal
// print(str.internalField) // Error: The internal field is not visible
```  


## 4. Best Practices and Pit Avoidance Guide

### 4.1 The principle of minimum permissions
- Priority is given to the use of `internal` or `private` modifier unless it must be disclosed
- Avoid declaring the entire `struct` as `public`, exposing only the necessary members

**Counterexample: Overdisclosure of all members**
```typescript  
public struct OversharedData {  
var data: String // It should be declared private and accessed through public method
  public init(data: String) { this.data = data }  
}  
```  

### 4.2 Testing strategies for cross-packet access
In unit testing, if you need to test the `internal` member, you can temporarily elevate permissions through the `@TestOnly` modifier:
```typescript  
// In the test module
@TestOnly struct TestableData {  
  internal var testField: Int64  
}  
```  

### 4.3 Naming specification suggestions
- `private` members are named with the `_` prefix (such as `_internalValue`)
- The `public` interface follows the camel nomenclature to ensure clear semantics

```typescript  
struct User {  
private var _apiToken: String // Private field naming specification
  public var username: String  
public func getToken() -> String { return _apiToken } // Public access interface
}  
```  


## Conclusion
Access modifiers are the key mechanism in HarmonyOS Next to decouple data encapsulation and modules.In development, the following principles must be followed:
1. **Packaging priority**: Use `private/internal` to hide implementation details, and only expose necessary functions through the `public` interface;
2. **Module isolation**: Use `protected` and `internal` to control the visibility within the module to avoid tight coupling across modules;
3. **Evolution Security**: Version management of the `public` interface to avoid destructive changes affecting external calls.

By accurately controlling the access rights of `struct` members, developers can build flexible and secure module boundaries in Hongmeng applications, especially in large-scale component library development and cross-team collaboration scenarios, which significantly improves the maintainability and stability of the code.
