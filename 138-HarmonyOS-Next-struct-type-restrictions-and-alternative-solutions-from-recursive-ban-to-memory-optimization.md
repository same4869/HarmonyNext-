
# HarmonyOS Next struct type restrictions and alternative solutions: from recursive ban to memory optimization

In HarmonyOS Next development, the design rules of the `struct` type put clear restrictions on data modeling, such as prohibiting recursive definitions, value type copy semantics, etc.Understanding the underlying logic of these limitations and mastering alternatives is the key to building complex data structures and efficient applications.This article is based on the document "0010 Creating a struct Example - Structure Type - Cangjie Programming Language Development Guide - Learning Cangjie Language.docx" to deeply analyze the core limitations and practical solutions of `struct`.


## 1. Disable recursive definition: Memory layout constraints for value types

### 1.1 Recursive/mutual recursive definition prohibition rules
`struct` does not allow direct or indirect reference to its own type. The following scenarios will trigger compilation errors:
- **Direct Recursion**: Structure members contain their own type instances.
  ```typescript  
  struct Node {  
    let value: Int64  
let next: Node // Error: Direct recursive reference
  }  
  ```  
- **Mutual recursion**: Two structures refer to each other's type instances.
  ```typescript  
  struct A { let b: B }  
struct B { let a: A } // Error: A and B recursively
  ```  

### 1.2 The underlying reason for prohibiting recursion
- **Value type memory allocation limit**: The `struct` instance allocates continuous memory on the stack, and recursive references will cause the type size to be undetermined (unlimited nesting).
- **Copy semantic conflict**: When copying a value type, a complete copy must be generated. Recursive references will lead to infinite recursive copying.

### 1.3 Alternatives: Reference Types and Indirect Modeling
#### Use class to implement recursive structure
Classes are reference types, and instances are stored as pointers, supporting recursive references.
```typescript  
class ListNode {  
  var value: Int64  
var next: ListNode? // Optional reference, allowing null
  init(value: Int64, next: ListNode? = nil) {  
    self.value = value  
    self.next = next  
  }  
}  
// Build a linked list: 1 -> 2 -> 3
let node3 = ListNode(value: 3)  
let node2 = ListNode(value: 2, next: node3)  
let head = ListNode(value: 1, next: node2)  
```  

##### Enumeration + class combination implements logical recursion
By enumerating member wrapping class instances, the hierarchy is implemented indirectly.
```typescript  
enum Tree {  
  case node(Int64, ChildNodes)  
}  
typealias ChildNodes = [Tree]  
// Use class encapsulation node operation
class TreeHandler {  
  func addChild(parent: Tree, child: Tree) -> Tree {  
// Operate enumeration nodes to avoid struct recursion
  }  
}  
```  


## 2. Copy overhead and optimization strategy for value types

### 2.1 Performance impact of replication semantics
The `struct` instance assignment or transfer participation will generate a complete copy. The more members or the more complex members, the more overhead it will be.

**Performance comparison (100,000 operations)**
| **Operation type** | **Small structure (2 Int members)** | ** Large structure (100 Int members)** |
|--------------------|---------------------------|-----------------------------|  
| Initialization time | 12ms | 187ms |
| Copying time | 8ms | 152ms |

### 2.2 Optimization Solution: Reduce replication and sharing references
#### Use the `inout` parameter to avoid copying
Pass the instance reference through `inout` and directly modify the original value, which is suitable for high-frequency operation scenarios.
```typescript  
struct Matrix {  
  var data: [[Float64]]  
}  
func transpose(inout matrix: Matrix) {  
  matrix.data = matrix.data[0].indices.map { col in  
    matrix.data.map { $0[col] }  
} // Modify the original instance directly
}  
var matrix = Matrix(data: [[1, 2], [3, 4]])  
transpose(inout: &matrix) // Avoid copying large matrices
```  

#### Split into small structures
Split large structures into multiple small structures according to their functions to reduce the amount of data copied in a single time.
```typescript  
// Counterexample: Single large structure
struct MonolithicData {  
  var userInfo: String  
  var settings: [String: Any]  
  var logs: [String]  
}  
// Optimization: Split into independent structure
struct UserInfo { var name: String }  
struct Settings { var config: [String: Any] }  
struct Logs { var entries: [String] }  
struct CombinedData { var info: UserInfo, settings: Settings, logs: Logs }  
```  

#### Shared reference type members
For complex data that needs to be shared, use class instances as struct members (reference types only copy pointers).
```typescript  
class SharedData {  
  var largeBuffer: [UInt8]  
  init(buffer: [UInt8]) { largeBuffer = buffer }  
}  
struct DataWrapper {  
var metadata: String // Value type member
var data: SharedData // Reference type members, low replication overhead
}  
```  


## 3. Limitations and alternative modes of mut function

### 3.1 Core limitations of mut function
- **`let` declares that the instance prohibits calling**: The `let` instance is immutable, and the `mut` function is prohibited during the compilation period.
  ```typescript  
  let fixedStruct = MutableStruct()  
// fixedStruct.update() // Error: The mut function cannot be called in the let instance
  ```  
- **Closure prohibits catching `this`**: closures within the `mut` function cannot capture instances or member variables.
  ```typescript  
  struct Foo {  
    public mut func f() {  
let closure = { this.value = 1 } // Error: This is not captured
    }  
  }  
  ```  

### 3.2 Alternative Patterns: Immutable Design and Factory Functions
#### Returns the immutable design of a new instance
Return a new instance through a pure function, replacing the modification logic of the `mut` function to maintain the purity of the data.
```typescript  
struct Point {  
  let x: Int64, y: Int64  
  public func moved(dx: Int64, dy: Int64) -> Point {  
return Point(x: x + dx, y: y + dy) // Return new instance
  }  
}  
var p = Point(x: 0, y: 0)  
p = p.moved(dx: 5, dy: 3) // Explicitly replace the instance
```  

#### Factory function encapsulation complex modification logic
Encapsulate multiple modification steps into factory functions to reduce the frequency of use of mut functions.
```typescript  
struct Config {  
  var timeout: Int64  
  var retries: Int64  
}  
func createConfigWithRetries(base: Config, retries: Int64) -> Config {  
  var config = base  
config.retries = retries // Use mut within the function to temporarily modify it
  return config  
}  
```  


## 4. Permission control and best practices for cross-module access

### 4.1 Cross-packet restrictions for access modifiers
The default permissions of the `struct` member are `internal` (current package is visible), and cross-package access must be declared as `public`.
```typescript  
// public struct in package a
public struct PublicData {  
public var publicField: String // Visible across packages
var internalField: String // Cross-package invisible
}  
// Access in package b
import a.*  
let data = PublicData(publicField: "cross-packet access")
// data.internalField // Error: internal member is not visible
```  

### 4.2 Optimization of data transfer between modules
#### Use the `public` interface to expose necessary members
Avoid direct exposure of `struct` internal details and provide access interfaces through public methods.
```typescript  
public struct User {  
private var age: Int64 // Private member
  public var name: String  
public func getAge() -> Int64 { return age } // Public access method
}  
```  

#### Pass immutable instance (`let` declaration)
Declare instances through `let` to ensure that data cannot be accidentally modified when passed across modules.
```typescript  
func processData(data: PublicData) {  
// Operation copy, the original data will not be affected
}  
let data = PublicData(publicField: "Immutable instance")
processData(data: data)  
```  


## 5. Summary: Finding design balance points in limitations

The limitation of `struct` is essentially to ensure the memory security and performance advantages of value types.In HarmonyOS Next development, it is recommended to follow the following principles:
1. **Clear type selection**: Recursive structure and shared state scenarios are preferred, and `struct` is used for lightweight data;
2. **Replication optimization priority**: Reduce the overhead of value type replication through `inout`, splitting structures, etc.;
3. **Permission minimization**: Use access modifiers to hide implementation details and expose only necessary interfaces.

By reasonably evading restrictions and combining alternative solutions, developers can fully utilize the value semantic advantages of `struct` in Hongmeng applications, especially in resource-constrained embedded devices and high-frequency data processing scenarios, to achieve efficient and secure data modeling.
