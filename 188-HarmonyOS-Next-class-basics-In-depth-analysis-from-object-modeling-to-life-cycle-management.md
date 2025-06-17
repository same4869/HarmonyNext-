
# HarmonyOS Next class basics: In-depth analysis from object modeling to life cycle management

In HarmonyOS Next development, Class (Class) serves as the core carrier of object-oriented programming, and plays the dual role of data encapsulation and behavior definition.This article combines the "Cangjie Programming Language Development Guide" to analyze how to build a robust application model through classes based on the basic definition of classes, object life cycle and inheritance mechanism.


## 1. Basic definition of class: encapsulation of data and behavior
Classes are defined through the `class` keyword, including member variables, constructors, member functions, etc., and are encapsulation units of data and behavior.

### 1. Member definition and access control
```cj
// Define rectangle class
open class Rectangle {
public var width: Int64 // Public instance variable
private var height: Int64 // Private instance variable

// Main constructor: Initialize member variables
    public Rectangle(let width: Int64, let height: Int64) {
        this.width = width
        this.height = height
    }

// Expose member function: calculate area
    public func area(): Int64 {
        width * height
    }

// Static variables: all instances are shared
    public static var count: Int64 = 0
}
```  

### 2. Overloading and initialization order of constructors
- **Main constructor**: The same name as the class, the parameters can be directly declared as member variables (such as `let width: Int64`);
- **Normal constructor**: Overloading is supported through `init` declaration:
  ```cj
  class Rectangle {
      public init(side: Int64) {
          this.width = side
this.height = side // Square initialization
      }
public init(width: Int64, height: Int64) { ... } // Overload the constructor
  }
  ```  
- **Initialization order**: First initialize the member variable, then execute the constructor body, and finally call the parent class constructor (see the inheritance chapter for details).


## 2. Object life cycle: the entire process management from creation to destruction
### 1. Object creation and reference semantics
Classes are reference types, and object assignments pass references rather than copying:
```cj
let rect1 = Rectangle(width: 10, height: 20)
let rect2 = rect1 // rect1 and rect2 point to the same object
rect1.width = 15
println(rect2.width) // Output 15, reference type characteristics
```  

### 2. Static initialization and resource allocation
- **Static variable initialization**: Initialize complex static resources through `static init` block:
  ```cj
  class FileHandler {
      static let defaultPath: String
      static init() {
defaultPath = getSystemPath() // Static initializer
      }
  }
  ```  
- ** Finalizer**: Release unmanaged resources (such as C memory) through `~init`:
  ```cj
  class NativeBuffer {
      private var ptr: UnsafePointer<CChar>?
      init(size: Int) {
ptr = malloc(size) // Allocate memory
      }
      ~init() {
ptr?.deallocate() // The terminal automatically releases memory
      }
  }
  ```  

### 3. Object type conversion and checking
Use the `is` and `as` operators for type checking and conversion:
```cj
let obj: Any = Rectangle(width: 5, height: 5)
if obj is Rectangle {
let rect = obj as! Rectangle // Safe conversion (must ensure the correct type)
    println(rect.area())
}
```  


## 3. Inheritance mechanism: single inheritance and code reuse
HarmonyOS Next supports single inheritance, and subclasses inherit the parent class through the `<:` keyword. The inheritance rules are as follows:

### 1. Member Inheritance and Overwrite
- **Inheritable members**: Except for the `private` member and the constructor, they can be inherited;
- **Override**: Subclass overrides the parent class `open` member function:
  ```cj
  open class Animal {
public open func speak(): String { "sound" }
  }
  class Dog <: Animal {
public override func speak(): String { "Wangwang" } // Override parent class method
  }
  ```  

### 2. Constructor inheritance rules
- The subclass constructor needs to explicitly call the parent class constructor (`super()`) or other constructors of this class (`this()`):
  ```cj
  open class Shape {
      public init() {}
  }
  class Circle <: Shape {
      public init(radius: Int) {
super() // Call the parent class parameterless constructor
      }
  }
  ```  
- If the parent class has no parameter constructor, the subclass must explicitly call the parameter constructor:
  ```cj
  open class Base {
      public init(value: Int) {}
  }
  class Derived <: Base {
      public init() {
super(value: 0) // The parent class parameter constructor must be called
      }
  }
  ```  

### 3. Abstract classes and inheritance restrictions
- **Abstract class**: Contains abstract functions (`abstract func`), and subclasses must implement all abstract members;
- **`sealed` class**: Inheritance is prohibited, used to enclose implementation details:
  ```cj
sealed class CoreService { /* System core service, inheritance is prohibited */ }
  ```  


## 4. Practical scenario: Class design of equipment status management
### Scenario: Design smart home equipment, supporting status monitoring, configuration storage and remote control.

#### 1. Base Class: Device Abstraction
```cj
open class Device {
    public var deviceId: String
public var status: DeviceStatus = .Offline // Enumeration status
    public init(deviceId: String) {
        self.deviceId = deviceId
    }

// Abstract function: subclass implements state update
    public abstract func updateStatus() -> Bool
}

enum DeviceStatus { .Online, .Offline, .Updating }
```  

#### 2. Subclass: Smart bulbs
```cj
class SmartBulb <: Device {
    private var brightness: Int = 0
    public init(deviceId: String, brightness: Int) {
        self.brightness = brightness
        super.init(deviceId: deviceId)
    }

    public override func updateStatus(): Bool {
        status = .Online
println("Light bulb\(deviceId) is online, brightness\(brightness)")
        return true
    }

// New member: Adjust brightness
    public func setBrightness(level: Int) {
        brightness = level
        if status == .Online {
            sendCommand("brightness=\(level)")
        }
    }
}
```  

#### 3. Object management and polymorphic applications
```cj
let bulb = SmartBulb(deviceId: "bulb_001", brightness: 50)
bulb.updateStatus() // Call subclass implementation
if bulb is Device {
let device: Device = bulb // Upward transformation
println("Device status:\(device.status)") // Output Online
}
```  


## 5. Common Traps and Best Practices

### 1. Member variable initialization order
- Avoid accessing uninitialized members in constructors:
  ```cj
  class A {
      let x: Int = 10
let y: Int = x + 5 // Legal: Member variables are initialized in declaration order
  }
  ```  

### 2. Limitations of Terminator
- The terminator cannot be called explicitly and cannot be used in the `open` class;
- Avoid executing complex logic or throwing exceptions in the finalizer.

### 3. Prefer combination rather than inheritance
When the functional reuse requirements are weak, use a combination pattern (such as including interface type members) instead of inheritance:
```cj
class NetworkDevice {
private let communicator: Communicator // Combined interface object
    public func send(data: String) {
communicator.transmit(data) // Delegate to the combined object
    }
}
```  


## 6. Summary: Class design philosophy
The class design of HarmonyOS Next follows the principle of "encapsulation changes, retaining stability":
- **Encapsulation**: Hide implementation details by access modifiers (`public`/`private`);
- **Inheritance**: Single inheritance ensures clear logic, abstract classes and interfaces coordinate to achieve polymorphism;
- **Life Cycle**: Constructors and terminators ensure resource security management.
