
# HarmonyOS Next class access modifier deep practice: precise control of encapsulation and visibility

In HarmonyOS Next development, the access modifier of the class is the core mechanism for implementing data encapsulation and module isolation.Through the `private`, `internal`, `protected` and `public` modifiers, developers can accurately control the visible range of class members and balance the encapsulation and extensibility of code.This article is based on the "Cangjie Programming Language Development Guide", which analyzes the rules, application scenarios and best practices of access modifiers.


## 1. Scope rules for access modifiers
HarmonyOS Next provides four access modifiers to control the visibility of members in different scopes:

| Modifier | Scope Description |
|--------------|--------------------------------------------------------------------------|  
| `private` | Only visible inside the class that defines the member.|
| `internal` | visible in the current package and subpackage (default modifier).|
| `protected` | is visible in the current class and its subclasses and is only available in the same module.|
| `public` | is visible in all modules, but the export rules of the package must be followed.|

**Example: Package Structure and Access Permissions**
```  
package device.core  
public open class Hardware {  
private var serialNumber: String // Only visible inside the Hardware class
internal func reset() { ... } // device.core package and subpackage are visible
protected var firmwareVersion: String // Subclass is visible (needed to be in the same module)
public var model: String // Globally visible
}  
```  


## 2. Access control practices of class members

### 1. `private`: Strictly encapsulate internal implementation
- **Applicable scenarios**: Private logic that prohibits external access, such as sensitive data, intermediate computed variables.
- **Example**:
  ```cj
  class SecureSensor {  
private var rawData: [UInt8] = [] // Private member: raw sensor data
      public func processData() {  
rawData.decode() // Internal processing logic
      }  
// rawData cannot be accessed externally, and can only be operated through public methods
  }
  ```  

### 2. `internal`: Private module visible in the package
- **Applicable scenarios**: Tool classes or helper functions that collaborate internally to avoid polluting the global namespace.
- **Example**:
  ```cj
  package network.internal  
  internal class SocketManager {  
func connect() { ... } // Only visible in network.internal packages and subpackages
  }  
  ```  

### 3. `protected`: Inheritance extension visible to subclasses
- **Applicable scenario**: Base class members that allow subclasses to rewrite or access, but restrict cross-module access.
- **Example**:
  ```cj
  open class BaseDevice {  
protected var status: DeviceStatus // Subclasses are accessible, but only for the same module
      public func getStatus() -> DeviceStatus { status }  
  }  
  class WirelessDevice <: BaseDevice {  
      public func updateStatus() {  
status = .Online // Subclasses can access protected members
      }  
  }  
  ```  

### 4. `public`: a globally visible public interface
- **Applicable scenarios**: Core interfaces or data that need to be exposed to other modules.
- **Notes**: The members of the `public` class defaults to `internal`, and need to be explicitly declared `public` to be visible globally:
  ```cj
  public class PublicAPI {  
public var publicField: Int // public must be declared explicitly
var internalField: String // Default is internal and is not visible across modules
  }  
  ```  


## 3. Constructor and access control

### 1. Access modification of constructor
The constructor can control instantiation permissions through modifiers to implement the design pattern:
- **Singleton Pattern**: Private constructor prohibits external instantiation
  ```cj
  class Singleton {  
      public static let instance = Singleton()  
private init() { /* Initialization Logic */ } // Private constructor
  }  
  ```  
- **Factory Mode**: The visible constructor in the package is combined with the static factory method
  ```cj
  package database  
  internal class DatabaseConnection {  
      internal init(url: String) { ... }  
      public static func create(url: String) -> DatabaseConnection {  
DatabaseConnection(url: url) // Create an instance in the package
      }  
  }  
  ```  

### 2. Constructor visibility in inheritance
The access modifier of the subclass constructor must match the parent class or be looser:
```cj
open class Parent {  
protected init() { /* protected constructor */ }
}  
class Child <: Parent {  
// The subclass constructor defaults to internal, and the parent class protected constructor can be accessed
    public init() { super.init() }  
}  
```  


## 4. Cross-module access and package management

### 1. Package export rules
- The `public` class in the module needs to be exported in the package declaration, otherwise it will not be visible across modules:
  ```cj
  // package.json  
  {  
    "name": "my.module",  
    "exports": {  
      ".": ["public-classes"]  
    }  
  }  
  ```  

### 2. Access modifiers and interface implementation
The default interface members are `public`, and the implementation class requires the same or more relaxed modifiers:
```cj
interface PublicInterface {  
    func publicMethod()  
}  
class Implementation <: PublicInterface {  
// Public must be declared, otherwise the default internal does not meet the interface requirements
    public func publicMethod() { ... }  
}  
```  


## 5. Common Traps and Best Practices

### 1. Avoid overuse of `public`
- Counterexample: Exposed too many implementation details and destroys encapsulation
  ```cj
  public class BadDesign {  
public var internalLogic: Int // It can be modified directly from the outside, violating the encapsulation principle
  }  
  ```  
- Formal example: Indirect access to private members through public methods
  ```cj
  public class GoodDesign {  
      private var _value: Int = 0  
      public func getValue() -> Int { _value }  
      public func setValue(newValue: Int) { _value = newValue }  
  }  
  ```  

### 2. `protected` module limitations
- The `protected` member is not visible in cross-module subclasses, and needs to be exposed using `public` or through the interface:
  ```cj
// Module A
  open class Base {  
protected func protectedFunc() { ... } // Subclasses in module A are visible
  }  
// Module B
  class Child <: Base {  
      func useProtected() {  
protectedFunc() // Compilation error: protected members are not accessible across modules
      }  
  }  
  ```  

### 3. Collaboration between interface and access modifiers
The access level of interface members determines the minimum requirements for the implementation class:
```cj
interface RestrictedInterface {  
internal func restrictedMethod() // Interface member is internal
}  
class Implementation <: RestrictedInterface {  
// The implementation method is at least internal (default) and cannot be declared as private
    func restrictedMethod() { ... }  
}  
```  


## 6. Summary: Design principles for access modifiers
The access modifier system of HarmonyOS Next follows the following core principles:
1. **The principle of minimum privilege**: Default `internal`, only necessary public interfaces are exposed;
2. **Encapsulation priority**: Use `private` to hide implementation details and provide access portals through public methods;
3. **Module Isolation**: Use `internal` and `protected` to control visibility within packages and inheritance levels.
