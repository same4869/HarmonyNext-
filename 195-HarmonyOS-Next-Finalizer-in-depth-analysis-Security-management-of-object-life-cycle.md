
# HarmonyOS Next Finalizer in-depth analysis: Security management of object life cycle

In HarmonyOS Next development, a finalizer is an important mechanism for managing the life cycle of an object, which is used to perform resource release and other cleaning operations when an object is garbage collected.This article is based on the "Cangjie Programming Language Development Guide", which analyzes the characteristics, usage scenarios and best practices of resource management.


## 1. Basic definition and syntax of the terminator
The terminator is declared through the `~init` keyword, with no parameters or return values, and is automatically called before object memory is recycled.

### 1. Basic usage examples
```cj
class FileHandle {
private var fd: CInt // emulate file descriptor

    init(path: String) {
fd = open(path, O_RDONLY) // Open the file (simplified example)
println("File Open:\(path)")
    }

    ~init() {
        if fd != -1 {
close(fd) // Close the file descriptor
println("File Close:\(fd)")
        }
    }
}

//Usage scenario: automatically release resources after the scope is over
func processFile() {
let handle = FileHandle(path: "/data.txt") // Open the file during initialization
// Use handle to process files...
// After the function is executed, the handle is recycled and the terminator is automatically called
}
```  

### 2. Terminator restrictions
- **No explicit call**: The terminator is automatically triggered by the garbage collector, and manual calls are prohibited from being called `handle.~init()`;
- **Non-open class**: Classes containing terminators cannot be modified with `open` to prevent resource leakage due to subclass rewriting;
- **Thread Safety**: The finalizer may be executed on any thread to avoid accessing thread-sensitive resources.


## 2. Terminator and resource management scenarios

### 1. Unmanaged resources are released
The most common purpose of a terminator is to free unmanaged resources (such as C memory, file handles, network connections):
```cj
class NativeMemory {
    private var ptr: UnsafeMutablePointer<Void>?

    init(size: Int) {
ptr = malloc(size) // Allocate native memory
    }

    ~init() {
ptr?.deallocate() // Free memory
        ptr = nil
    }
}
```  

### 2. Event Listener Cleanup
When registering a global event listener, the finalizer ensures that the object is automatically unbined when it is destroyed:
```cj
class EventListener {
    init() {
EventBus.register(self) // Register event listening
    }

    ~init() {
EventBus.unregister(self) // Anti-registration event listening
    }

func onEvent(event: Event) { /* Handle events */ }
}
```  

### 3. Log and debug information logging
The terminator can be used to record object life cycle information and assist in debugging:
```cj
class DebugObject {
    private let id: String = UUID().toString()

    init() {
println("Object creation:\(id)")
    }

    ~init() {
println("Object Destruction:\(id)")
    }
}
```  


## 3. Endorsement mechanism and traps

### 1. Uncertainty of execution timing
- The terminal triggering time depends on the garbage collector scheduling, which may be executed at any time after the object is unreachable;
- Avoid relying on the finalizer to perform operations requiring high real-time requirements (such as network requests).

**Example: Unreliable Real-time Logic**
```cj
class RealTimeTimer {
    ~init() {
sendHeartbeat() // logic may fail due to delayed execution
    }
}
```  

### 2. Circular reference and terminator failure
A circular reference will cause the object to be recycled and the finalizer may never execute:
```cj
class A {
    var ref: B?
~init() { println("A Destruction") }
}

class B {
    var ref: A?
~init() { println("B destroy") }
}

func createCycle() {
    let a = A()
    let b = B()
a.ref = b // Circular reference: A→B→A
    b.ref = a
// Neither a and b can be recycled, the terminator will not execute
}
```  

**Solution**: Break the loop with weak references (`weak`):
```cj
class A {
weak var ref: B? // Weak reference, does not prevent recycling
}
```  

### 3. Inheritance and Terminator Call Order
The subclass finalizer will be executed after the parent class finalizer:
```cj
open class Parent {
~init() { println("parent class destroyed") }
}

class Child <: Parent {
~init() { println("subclass destruction") } // Call the subclass terminal first, then call the parent class
}

let child = Child() // Output: Subclass destruction → Parent class destruction
```  


## IV. Alternatives and Best Practices

### 1. Priority to RAII mode
Manage resources through `use` statement or custom scope, which is more controllable than the finalizer:
```cj
func processResource() {
let resource = Resource() // Initialization
defer { resource.release() } // Release the resource at the end of the scope
// Use resource...
} // Automatically call release() without relying on the finalizer
```  

### 2. The terminator is combined with `try-finally`
In scenarios where exceptions may be thrown, ensure resource release:
```cj
class DatabaseConnection {
    func query() throws {
        do {
// Execute query
throw Error("Query failed")
        } finally {
close() // Clean up regardless of whether an exception is thrown or not
        }
    }

~init() { close() } // as an additional guarantee
}
```  

### 3. Avoid complex logic
The terminator should only perform lightweight cleaning, avoiding:
- Call a function that may throw an exception;
- Access other objects that may have been recycled;
- Perform time-consuming operations (such as disk writing).


## V. Summary: Applicable boundaries of the terminator
HarmonyOS Next's finalizer plays a "safety net" role in resource management, and its design principles are as follows:
- **Last line of defense**: As a supplement to RAII mode, deal with resources that cannot be managed through scope;
- **Lightweight operation**: Only perform necessary cleaning logic to avoid affecting system performance;
- **Limited Cognition**: Do not rely on the finalizer to implement key business logic, and priority is given to the use of explicit release mechanisms.
