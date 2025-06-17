
# HarmonyOS Next Collaboration between Custom Enumeration and Standard Library: Option and Result

In HarmonyOS Next development, the collaborative use of custom enumerations with standard library types (such as Option, Result,) is the key to building type-safe and maintainable code.Cangjie Language complements the generic enumerations of the standard library through the algebraic data type characteristics of enumerations, and can efficiently handle scenarios such as missing values ​​and failures.This article combines document knowledge points to analyze how to extend the standard library capabilities through custom enumerations to achieve more robust business logic.


## 1. The essence of Option type and custom extension
### 1. Core semantics of Option type
`Option<T>` is a generic enum provided by the standard library to represent "possible values":
```cj
enum Option<T> {
    | Some(T)
    | None
}
```  
- **`Some(T)`**: indicates that the value exists and carries an instance of type `T`.
- **`None`**: indicates missing value, equivalent to null` in other languages, but is safer.

### 2. Custom enumeration adapts Option semantics
When more specific value missing scenarios are needed, the Option semantics can be inherited through custom enumerations:
```cj
// Business scenario: User permissions may not be initialized
enum UserPermission {
| Granted(String) // Authorized (Permission Scope)
| Denied // Reject authorization
| Uninitialized // Uninitialized (equivalent to None of Option)
}

// Convert to Option type
func toOption(perm: UserPermission) -> Option<String> {
    match (perm) {
        case .Granted(scope) => Some(scope)
        case .Denied | .Uninitialized => None
    }
}
```  

### 3. Used in conjunction with if-let/while-let
Use the standard library's deconstructed syntax to process custom enums:
```cj
let permission = UserPermission.Granted("read")
if (let Some(scope) <- toOption(perm: permission)) {
println("Permissions:\(scope)") // Output: Permissions: read
}
```  


## 2. Result type: the enumeration paradigm for handling operation failures
### 1. Standard definition of Result type
`Result<T, E>` is used to represent possible operational results and is another generic enum provided by the standard library:
```cj
enum Result<T, E> {
| Ok(T) // The operation is successful, carrying the result value
| Err(E) // The operation failed, carrying error message
}
```  
- **Application Scenario**: Operations that may fail in file reading and writing, network requests, data analysis, etc.

### 2. Combining custom error enumeration with Result
Define business-specific error types and fail to deal with `Result` in conjunction with:
```cj
// Custom error enumeration
enum FileError {
    | NotFound(String)
    | PermissionDenied
    | CorruptedData
}

// Returns the function example of Result
func readConfigFile(path: String) -> Result<String, FileError> {
    if !fileExists(path) {
        return Err(.NotFound(path))
    } else if !hasReadPermission(path) {
        return Err(.PermissionDenied)
    } else {
        let content = readFile(path)
        return content.isCorrupted ? Err(.CorruptedData) : Ok(content)
    }
}
```  

### 3. Pattern matching processing Result results
```cj
func processConfig() {
    let result = readConfigFile(path: "/config.json")
    match (result) {
case Ok(content) => println("Configuration content: \(content)")
        case Err(error) => handleFileError(error)
    }
}

func handleFileError(error: FileError) {
    match (error) {
case .NotFound(path) => println("File not found: \(path)")
case .PermissionDenied => println("Insufficient Permission")
case .CorruptedData => println("Data corruption")
    }
}
```  


## 3. Mixed use of custom enumeration and standard library
### 1. Multi-level error handling: from custom to standard library
Convert the errors of the custom enum to the standard library `Error` type, adapt to the common interface:
```cj
extension FileError : Error { } // Make FileError compliant with the standard library Error protocol

func loadData() throws {
    let result = readConfigFile(path: "/data.txt")
// Convert Results to Throws-style interface
    if let Err(e) = result {
        throw e
    }
}
```  

### 2. Combination mode of Option and Result
Handle the dual uncertainty of "possible missing values ​​+ possible failed operations":
```cj
func fetchOptionalData() -> Result<Option<String>, NetworkError> {
    if isNetworkAvailable() {
let data = networkRequest() // May return None
        return Ok(data)
    } else {
        return Err(.NoConnection)
    }
}

// Deconstruct combination type
match (fetchOptionalData()) {
case Ok(Some(data)) => println("Successfully obtained data: \(data)")
case Ok(None) => println("Data does not exist")
case Err(error) => println("Network Error: \(error)")
}
```  

### 3. Generic abstraction for custom enums
Define reusable enumeration structures through generics, consistent with the standard library:
```cj
enum Either<L, R> {
    | Left(L)
    | Right(R)
}

// Example: Convert Result to Either
func resultToEither<T, E>(result: Result<T, E>) -> Either<E, T> {
    match (result) {
        case Ok(t) => .Right(t)
        case Err(e) => .Left(e)
    }
}
```  


## 4. Best practices: Avoid over-design and type abuse
### 1. Priority to using standard library types
- **Counterexample**: Repeat implementation of enums like Option
  ```cj
// Avoid customizing Option-like enums
  enum Maybe<T> {
      | Just(T)
      | Nothing
  }
  ```  
- **Positive example**: Use `Option<T>` directly, and increase business logic by extending if necessary.

### 2. Granularity control of error enumeration
- Refine error types: distinguish temporary errors (such as `.Timeout`) from permanent errors (such as `.InvalidData`), for easy processing of upper-level logic.
- Avoid enumeration explosion: Reuse error types by generic parameters, such as `Result<Int, MyError>` instead of defining independent enums for each type.

### 3. Coordination principle for pattern matching
- Use `match` instead of `if-else` to handle enumerations to ensure exhaustive checks;
- Complex enumeration deconstruction can be split into independent functions to improve readability:
  ```cj
  func decode(data: Data) -> Result<Config, DecodeError> {
// Complex parsing logic
  }

  func handleDecodeResult(result: Result<Config, DecodeError>) {
      match (result) {
          case .Ok(config) => applyConfig(config)
          case .Err(error) => logDecodeError(error)
      }
  }
  ```  


## Summarize
The collaboration between custom enumeration and HarmonyOS Next standard library is essentially to build a unified error handling and value management system through algebraic data types:
1. **`Option`** handles the existence of values, replacing the unsafe null;
2. **`Result`**Processing operation failed, providing type-safe error information;
3. **Custom Enumeration**Extend the standard library semantics to adapt to specific business scenarios.
