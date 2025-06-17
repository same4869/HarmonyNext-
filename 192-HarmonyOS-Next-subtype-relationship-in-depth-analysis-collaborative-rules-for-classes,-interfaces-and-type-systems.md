
# HarmonyOS Next subtype relationship in-depth analysis: collaborative rules for classes, interfaces and type systems

In HarmonyOS Next development, subtype relationships are the core logic for implementing polymorphic programming and type safety.Cangjie Language defines subtype rules between types such as classes, interfaces, tuples, etc. through a strict type system.This article is based on the "Cangjie Programming Language Development Guide", which analyzes the rules of determining subtype relationships, application scenarios and practical points in architecture design.


## 1. Core definition and judgment rules for subtype relationships
Subtype refers to the ability of one type to replace another type.If type S is a subtype of type T (S <: T), an instance of S can be used in any scenario where T is required.

### 1. Subtype relationship between class and interface
- **ClassInheritance**: The subclass is a child type of the parent class (`ClassSub <: ClassSuper`).
- **Interface Implementation**: The class that implements an interface is a subtype of the interface (`Class <: Interface`).
- **Interface Inheritance**: The child interface is a child type of the parent interface (`InterfaceSub <: InterfaceSuper`).

**Example**:
```cj
open class Animal {}
class Dog <: Animal {} // Dog is a subtype of Animal

interface Flyable {}
class Bird <: Flyable {} // Bird is a subtype of Flyable

interface Pet <: Animal {} // Pet is an Animal subinterface
```  

### 2. Subtype relationship of basic types
- **Number type**: There is no direct subtype relationship, and it needs to be explicitly converted (such as `Int` non-Number` subtype, it needs to be abstracted through the interface).
- **Special Type**:
- `Nothing` is a subtype of all types (`Nothing <: T`);
- All types are subtypes of `Any` (`T <: Any`).


## 2. Application of subtype relationships in polymorphisms
### 1. Subtype adaptation of function parameters
When the function parameter is a parent type, subtype instances can be accepted:
```cj
func feed(animal: Animal) {
println("Feed the animal")
}

let dog: Dog = Dog()
feed(animal: dog) // Legal: Dog is an Animal subtype
```  

### 2. Interface as return type
When a function returns a subtype instance, it can be assigned to the interface variable:
```cj
interface Vehicle {}
class Car <: Vehicle {}

func createVehicle(): Vehicle {
return Car() // Legal: Car is a Vehicle subtype
}

let vehicle: Vehicle = createVehicle()
```  

### 3. Subtype compatibility of arrays and containers
- Subtype arrays can be assigned to parent type arrays (covariant rules):
  ```cj
  let dogs: [Dog] = [Dog()]
let animals: [Animal] = dogs // Legal: [Dog] is a subtype of [Animal]
  ```  


## 3. Subtype rules for complex types

### 1. Subtype relationship of tuple type
Tuple subtypes require that each element type be a child type of the corresponding parent type:
```cj
let point2D: (Int, Int) = (1, 2)
let point3D: (Number, Number, Number) = (1.0, 2.0, 3.0)

// Legal: Int is a subtype of Number (assuming Number is parent type)
let superPoint: (Number, Number) = point2D 

// Illegal: Inconsistent number of elements
let errorPoint: (Number, Number) = point3D 
```  

### 2. Subtype relationship of function type
Function type `(S) -> R` is a subtype of `(T) -> U` if and only if:
- Parameter type `T <: S` (inverter);
- Return type `R <: U` (covariance).

**Example**:
```cj
func superFunc(arg: Animal) -> String { "Animal" }
func subFunc(arg: Dog) -> Dog { Dog() }

// Legal: The parameter Dog is an Animal subtype, and the return Dog is an Any subtype
let funcVar: (Animal) -> Any = subFunc 
```  

### 3. Subtype constraints for generic types
Generic functions can limit subtype relationships through the `where` clause:
```cj
func printName<T: Animal>(animal: T) where T <: Named {
println(animal.name) // Require T to be a subtype of both Animal and Named
}
```  


## 4. Practical scenarios and traps of subtype relationships

### 1. Application of Interface Isolation Principle (ISP)
Split the large interface into small interfaces to avoid subtypes being forced to implement irrelevant functions:
```cj
interface Animal {
    func eat()
}
interface Flyable {
    func fly()
}

// Correct: Bird implements the required interface
class Bird <: Animal, Flyable { 
    func eat() {}
    func fly() {}
}

// Error: Fish is forced to implement fly()
class Fish <: Animal, Flyable { // If ISP is violated, Fish will not fly
    func eat() {}
func fly() { throw Error() } // Redundant implementation
}
```  

### 2. Security traps for subtype conversion
- **Misuse of covariance and inversion**:
  ```cj
let numbers: [Number] = [Int(1), Float(2.0)] // Legal, assuming Number is the parent interface
numbers.append(String("3")) // Compile error: String non-Number subtype
  ```  
- **Restrictions on cross-package `sealed` interface**:
  ```cj
  package A
  sealed interface PrivateInterface {}

  package B
  import A.*
class ImplementsInterface <: PrivateInterface {} // Compilation error: Sealed interface cannot be implemented across packages
  ```  

### 3. Performance impact of subtypes and dynamic distribution
- Dynamic distribution of instance functions (virtual function tables) may bring slight performance overhead;
- Static functions and attributes have no dynamic overhead, and are directly bound during the compilation period.


## 5. Sub-type strategies in architectural design

### Scenario: Subtype adaptation of device driver plug-in system
#### 1. Define core interfaces and base classes
```cj
// Device driver interface
interface DeviceDriver {
    func connect(): Bool
}

// Abstract class with default implementation
open abstract class AbstractDriver <: DeviceDriver {
    public func connect(): Bool {
checkPermissions() // General permission check
return doConnect() // Abstract function, subclass implementation
    }
    protected abstract func doConnect(): Bool
}
```  

#### 2. Subtype implementation and polymorphic loading
```cj
// Serial port driver (subclass)
class SerialDriver <: AbstractDriver {
    protected override func doConnect(): Bool {
// Specific connection logic
    }
}

// Network driver (subclass)
class NetworkDriver <: AbstractDriver {
    protected override func doConnect(): Bool {
// Specific connection logic
    }
}

// Plug-in loader (polymorphic processing)
func loadDriver(driver: DeviceDriver) {
    if driver is AbstractDriver {
        let abstractDriver = driver as! AbstractDriver
abstractDriver.connect() // Call general logic
    }
// Other processing...
}
```  

#### 3. Generic optimization of subtype constraints
```cj
func registerDriver<T: AbstractDriver>(driver: T) {
drivers.append(driver) // Only accept AbstractDriver subtypes
}
```  


## 6. Summary: Design criteria for subtype relationships
The subtype system of HarmonyOS Next follows the following core principles:
1. **Explanatory constraints**: explicitly define subtype relationships through `interface` and `open class` to avoid implicit dependencies;
2. **Minimum dependency**: Prioritize dependence on interfaces over specific classes to reduce coupling between modules;
3. **Type Safety**: Use the compiler to check the integrity of subtype implementations to avoid runtime errors.
