
# HarmonyOS Next struct Cross-module Access and Permission Control Practice

In HarmonyOS Next development, cross-module access of `struct` involves member visibility control, package dependency management, and compile-time verification.Rational use of access modifiers and module mechanisms can ensure efficient circulation of data within the security boundary.This article is based on the document "0010 Creating a struct Example - Struct Type - Cangjie Programming Language Development Guide - Learning Cangjie Language.docx" to analyze the core rules and practical strategies of `struct` cross-module access.


## 1. Scope rules for access modifiers

### 1.1 Level 4 permission model
| **Modifier** | **Scope** | **Spanning Access** |
|--------------|--------------------------------------------------------------------------|----------------|  
| `private` | Only visible in the body in the `struct` definition | Invisible |
| `internal` | Current package and subpackage are visible (default modifier) ​​| visible to the same module |
| `protected` | Current module is visible (module dependencies need to be configured) | same module is visible |
| `public` | Visible inside and outside the module | Visible across modules |

**Example: Access differences between different modifiers**
```typescript  
// struct in module a
public struct User {  
public var name: String // Visible across modules
internal var age: Int64 // visible to the same module
private var token: String // Only visible in struct
}  
```  

### 1.2 Necessity of `public` modification
When accessing `struct` and its members across modules, `public` must be explicitly declared, otherwise the default `internal` permission will cause compilation errors.
```typescript  
// The public struct in module b refers to module a
import a.*  
let user = User(name: "Alice")  
user.name = "Bob" // Legal: public members can be writable across modules
// user.age = 30 // Error: Internal members are not visible across modules
```  


## 2. Compilation period verification of cross-module access

### 2.1 Module Dependency Configuration
Dependencies must be declared in `build.gradle` before cross-module calls, otherwise the compiler will not be able to resolve the type.
```gradle  
dependencies {  
implementation project(':module-a') // Declare dependencies on module a
}  
```  

### 2.2 Strict matching of member permissions
If `struct` is `public`, but its member is `internal`, the member cannot be accessed across modules.
```typescript  
// Module a
public struct DataModel {  
var internalField: String // Default is internal and is not visible across modules
  public var publicField: String  
}  
// Module b
import a.*  
let model = DataModel(publicField: "visible")
// model.internalField = "not visible" // Error: Internal member is not accessible
```  


## 3. Practical scenario: cross-module data interaction

### 3.1 Public data model definition
Define `public struct` in a standalone module as the data carrier for cross-module communication.
```typescript  
// Common structure in module common
public struct NetworkResponse<T> {  
  public var code: Int64  
  public var data: T  
  public var message: String  
}  
// Used in module feature
import common.*  
func processResponse(response: NetworkResponse<String>) {  
print(response.code) // Legal: public members access across modules
}  
```  

### 3.2 Cross-module configuration center
The global configuration is provided through static members, and the `internal` member can be accessed within the module, and the external operation can only be operated through the `public` interface.
```typescript  
// Module config
public struct AppConfig {  
internal static var internalConfig: String = "In-module configuration"
public static var publicConfig: String = "Cross-module configuration"
  public static func getInternalConfig() -> String {  
return internalConfig // Functions inside the module can access internal members
  }  
}  
// Module feature
import config.*  
print(AppConfig.publicConfig) // Legal
// print(AppConfig.internalConfig) // Error: Internal static member is not visible
```  

### 3.3 Interface abstraction and cross-module polymorphism
Use interfaces to hide the specific `struct` implementation, and only rely on abstract interfaces across modules.
```typescript  
// Module api (interface definition)
public interface DataLoader {  
  func load() -> String  
}  
// Module impl (struct implementation)
public struct FileLoader : DataLoader {  
  public func load() -> String { /*...*/ }  
}  
// Module app (cross-module call)
import api.*  
import impl.*  
func fetchData(loader: DataLoader) -> String {  
return loader.load() // Depend on interface rather than specific struct
}  
```  


## 4. Common errors and evasion strategies

### 4.1 Cross-module access to `internal` members
**Cause of error**: The member is not declared because `public` is invisible.
```typescript  
// Internal struct in module a
struct InternalData { /*...*/ }  
// References in module b
import a.*  
let data = InternalData() // Error: struct not declared public
```  

**Solution**: Declare the `public` modifier and make sure the module dependencies are correct.
```typescript  
public struct PublicData { /*...*/ }  
```  

### 4.2 Circular dependency causes compilation failure
**Error scenario**: Module a refers to module b, and module b refers to module a.
```gradle  
// build.gradle of module a
dependencies { implementation project(':module-b') }  
// build.gradle of module b
dependencies { implementation project(':module-a') }  
// Compilation error: Circular dependency
```  

**Solution**: Extract public modules and split dependencies.

### 4.3 Cross-module access restrictions for static members
Static members must also follow the access modifier rules. If the static members of `public struct` are `internal`, they are not visible across modules.
```typescript  
public struct StaticData {  
internal static var version = "1.0" // Not visible across modules
}  
// Access in module b
print(StaticData.version) // Error: Internal static member is not visible
```  


## 5. Best practices and performance optimization

### 5.1 The principle of minimum permissions
- Declare only the necessary `struct` and members as `public`, and the rest remain `internal` or `private`.
- Avoid exposing internal implementation details such as temporary calculation fields or intermediate states.

### 5.2 Optimize compilation speed using in-package visibility (`internal`)
The `struct` shared within the module uses the default `internal` modifier to reduce cross-module compilation dependencies.

### 5.3 Cross-module data transfer optimization
- **Value type copy optimization**: Use the `inout` parameter or split into small structures when passing large `struct`.
- **Reference type encapsulation**: Encapsulate the shared state across modules through `class` to avoid value type replication overhead.

```typescript  
// Module a
public class SharedState {  
  public var data: String  
  public init(data: String) { self.data = data }  
}  
// Module b
import a.*  
func updateState(state: SharedState) {  
state.data = "Updated data" // Reference type, no copy overhead
}  
```  


## Conclusion
Cross-module access of `struct` is the basic capability of HarmonyOS Next component development.By accurately controlling access modifiers, rationally designing module dependencies, and following the principle of minimum permissions, a safe and efficient cross-module data interaction system can be built.In practice, attention should be paid to:
1. **Permission control priority**: Ensure that sensitive data is visible only within the necessary scope;
2. **Module decoupling**: Detailed implementation through interface or abstract class isolation to reduce coupling between modules;
3. **Performance sensitive design**: For high-frequency data passed across modules, reference types or optimized value type structure are preferred.

Mastering these rules can give full play to the lightweight advantages of `struct` in the modular development of Hongmeng applications, especially in microservice architecture, cross-device collaboration and other scenarios to achieve safe and efficient data circulation.
