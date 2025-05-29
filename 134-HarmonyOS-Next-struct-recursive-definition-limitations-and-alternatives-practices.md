
# HarmonyOS Next struct recursive definition limitations and alternatives practices

In HarmonyOS Next development, the `struct` type prohibits recursive or mutual recursive definition, which is determined by the memory layout characteristics of the value type.Understanding the underlying logic of this limitation and mastering appropriate alternatives is crucial for designing complex data structures.This article combines the document "0010 Creating a struct Example - Struct Type - Cangjie Programming Language Development Guide - Learning Cangjie Language.docx" to analyze the principles and practical solutions of recursive limitations.


## 1. Recursive definition of prohibition rules and principles

### 1.1 Definition scenarios of recursion/mutual recursion
#### Direct recursion
```typescript  
struct Node {  
  let value: Int64  
let next: Node // Error: Node contains its own type instance, recursively defined
}  
```  

#### Mutual recursion
```typescript  
struct A {  
let b: B // A quotes B
}  
struct B {  
let a: A // B refers to A to form mutual recursion
}  
// Error: A and B refer to each other, forming a mutual recursive definition
```  

### 1.2 The underlying reason for prohibiting recursion
- **Value type memory layout limit**: The `struct` instance allocates continuous memory on the stack, and recursive definition will cause the type size to be undetermined (unlimited nesting).
- **Copy semantic conflict**: Recursive references will cause instance replication to fall into an infinite loop, violating the copy rules of value types.


## 2. Alternative: a hierarchical structure based on class or enumeration

### 2.1 Use class to implement recursive structure
Classes are reference types, and instances are stored as pointers, which can support recursive references.

**Single-linked list node (class implementation)**
```typescript  
class ListNode {  
  var value: Int64  
var next: ListNode? // Optional reference, allowing null
  init(value: Int64, next: ListNode? = nil) {  
    self.value = value  
    self.next = next  
  }  
}  
// Use: Build a link list
let node3 = ListNode(value: 3)  
let node2 = ListNode(value: 2, next: node3)  
let head = ListNode(value: 1, next: node2)  
```  

### 2.2 Enumeration + Indirect Reference
By enumerating member wrapping class instances, a logical recursive structure is implemented.

**Expression tree (enumeration + class combination)**
```typescript  
enum Expression {  
  case number(Int64)  
  case add(ExpressionNode)  
  case multiply(ExpressionNode)  
}  
class ExpressionNode {  
  let left: Expression  
  let right: Expression  
  init(left: Expression, right: Expression) {  
    self.left = left  
    self.right = right  
  }  
}  
// Build expression: (1 + 2) * 3
let addExpr = Expression.add(ExpressionNode(left: .number(1), right: .number(2)))  
let multiplyExpr = Expression.multiply(ExpressionNode(left: addExpr, right: .number(3)))  
```  

### 2.3 Interface abstraction and non-recursive design
Abstract recursive logic into an interface and implement traversal or operation through non-recursive means.

**File system node (interface abstraction)**
```typescript  
interface FileSystemNode {  
  var name: String { get }  
// Non-recursive method: Get all child nodes (provided by the specific implementation)
  func getChildren(): [FileSystemNode]  
}  
struct File: FileSystemNode {  
  let name: String  
  func getChildren(): [FileSystemNode] { return [] }  
}  
struct Directory: FileSystemNode {  
  let name: String  
  let children: [FileSystemNode]  
  func getChildren(): [FileSystemNode] { return children }  
}  
```  


## 3. Non-recursive pattern of data structure design

### 3.1 Iterative substitution recursion: traversal of trees
Use stack or queue to implement traversal of the tree to avoid recursive definitions.

**Binary tree preorder traversal (iteration method)**
```typescript  
struct BinaryTreeNode {  
  let value: Int64  
  let left: BinaryTreeNode?  
  let right: BinaryTreeNode?  
}  
func preorderTraversal(root: BinaryTreeNode?) -> [Int64] {  
  var result = [Int64]()  
  var stack = [root]  
  while let node = stack.pop() {  
    if let node = node {  
      result.append(node.value)  
      stack.append(node.right)  
      stack.append(node.left)  
    }  
  }  
  return result  
}  
```  

### 3.2 Flat data structure
Flatten the hierarchy into a linear structure, and associate nodes through an index or ID.

**JSON data model (key-value pair storage)**
```typescript  
struct JsonNode {  
  enum Type { object, array, string, number }  
  let type: Type  
  let value: String  
// Use dictionary to store child nodes (non-recursive)
  let children: [String: JsonNode]  
}  
// Example: Flat object
let obj = JsonNode(  
  type: .object,  
  value: "root",  
  children: [  
    "key1": JsonNode(type: .string, value: "value1", children: [:]),  
    "key2": JsonNode(type: .number, value: "42", children: [:])  
  ]  
)  
```  

### 3.3 External reference table
Manage node relationships through independent reference tables to avoid recursive references inside the structure.

**Graph Structure (Adjacent Table Implementation)**
```typescript  
struct GraphNode {  
  let id: String  
  let data: String  
}  
// Adjacent table: The mapping between storage node ID and adjacent node ID
var adjacencyList: [String: [String]] = [:]  
// Add node relationship
adjacencyList["A"] = ["B", "C"]  
adjacencyList["B"] = ["A"]  
```  


## 4. Common errors and evasion strategies

### 4.1 Recursive class references as struct
It is legal to use optional references to classes in `struct`, and you need to pay attention to distinguishing the semantics of value types from reference types.

**Legal scenario: struct contains weak references to the class**
```typescript  
struct Controller {  
weak var view: View? // View is of class type, optional reference is legal
}  
class View {  
  var controller: Controller?  
}  
```  

### 4.2 Special handling of mutual recursive enumeration
If the enumeration member is a value type, it still needs to comply with the prohibited mutual recursion rules; if it is a reference type, it is allowed.

**Error: Mutual recursive value type enumeration**
```typescript  
enum A { case a(B) }  
enum B { case b(A) } // Error: A and B are recursive, both of which are value types
```  

**Legal: Mutual recursive reference type enum**
```typescript  
enum RefA { case a(RefB) }  
class RefB { var a: RefA? }  
```  

### 4.3 Memory optimization for performance-sensitive scenarios
When using classes to implement recursive structures, you need to pay attention to the heap allocation overhead, which can be optimized through object pooling or multiplexing mechanism.

**Object pool example**
```typescript  
class NodePool {  
  private var reusableNodes = [ListNode]()  
  func getNode(value: Int64) -> ListNode {  
    if let node = reusableNodes.popLast() {  
      node.value = value  
      node.next = nil  
      return node  
    }  
    return ListNode(value: value)  
  }  
  func release(node: ListNode) { reusableNodes.append(node) }  
}  
```  


## 5. Architectural design principles

### 5.1 Separation of data and behavior
Encapsulate recursive logic in a class or module, `struct` is only responsible for data storage and follows the principle of single responsibility.

```typescript  
// struct is responsible for data
struct TreeData {  
  let value: Int64  
  let leftData: TreeData?  
  let rightData: TreeData?  
}  
// Classes are responsible for operations
class TreeOperator {  
  func traverse(data: TreeData) {  
// Iterative traversal logic
  }  
}  
```  

### 5.2 Priority to the use of mature data structures
Avoid implementing complex recursive structures by yourself, and give priority to using the collection types provided by the Hongmeng framework (such as `Array/Map`) or open source libraries.

**Recommended: Use Array to simulate stack structure**
```typescript  
var stack = [Int64]()  
stack.append(10)  
let top = stack.popLast()  
```  

### 5.3 Compilation period verification utilization
With the compiler's error message for recursive definitions, we can quickly locate design defects and avoid runtime problems.


## Conclusion
`struct` prohibits the restriction of recursive definition, which is essentially an inevitable requirement of the value type memory model.In HarmonyOS Next development, the following strategies are required:
1. **The type selection is clear**: Recursive structures are implemented with class or enumeration + reference types first;
2. **Design pattern adaptation**: Use iterative, flattened or external reference pattern instead of recursion;
3. **Performance and security balance**: On the premise of ensuring type safety, optimize the performance overhead of reference types through object pooling and other technologies.

By reasonably avoiding recursive restrictions, developers can build efficient and secure complex data structures in Hongmeng applications, especially in scenarios such as configuration management of IoT devices, graphics rendering engines, etc., to give full play to the synergistic advantages of value types and reference types.
