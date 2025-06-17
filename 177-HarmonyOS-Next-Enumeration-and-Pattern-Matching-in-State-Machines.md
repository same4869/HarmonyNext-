
# HarmonyOS Next Enumeration and Pattern Matching in State Machines

In HarmonyOS Next development, state machines are an effective tool for managing complex business logic.Combining enum types (`enum`) and pattern matching (`match`), states can be clearly defined, standardized state migration, and ensure type safety.This article takes scenarios such as smart home device control and network request process as examples to analyze how to build a robust state machine through enumeration and pattern matching.


## 1. State machine basics: enumeration definition and state modeling
### 1. Enumeration defines the status collection
Using enumeration to enumerate all possible states of a state machine, the constructor can carry parameters to represent state properties.
```cj
// Smart home equipment state machine
enum DeviceState {
| Off // Shutdown status
| On(Int) // Power-on status (carrying the current brightness)
| Error(String) // Error status (carrying error message)
| Update(progress: Int) // Update status (carrying progress percentage)
}
```  

### 2. State migration rule definition
Encapsulate the state change logic through functions to ensure that state migration complies with business rules.
```cj
func toggleState(currentState: DeviceState) -> DeviceState {
    match (currentState) {
case .Off => .On(100) // Shut down → power on (default brightness 100)
case .On(_) => .Off // Turn on → shut down
case .Error(_) => .Off // Error status → Shutdown
case .Updating(_) => currentState // No response to switching during update
    }
}
```  


## 2. Pattern matching implements state processing logic
### 1. Status branch processing
Use the `match` expression to define processing logic for each state, ensuring that all states are overwritten.
```cj
func handleState(state: DeviceState) {
    match (state) {
        case .Off:
println("Device shutdown")
// Execute shutdown logic (such as disconnecting the power supply)

        case .On(brightness):
println("The device is powered on, current brightness:\(brightness)%")
// Adjust the brightness logic

        case .Error(msg):
println("Error: \(msg), try to restart...")
// Error recovery logic

        case .Updating(progress):
println("Update progress:\(progress)%")
// Update progress display
    }
}
```  

### 2. Destruction with parameter state
For the state that carries parameters (such as `.On(Int)`), the parameters are extracted through pattern matching and participate in the logic.
```cj
func adjustBrightness(state: DeviceState, delta: Int) -> DeviceState {
    match (state) {
        case .On(brightness) where brightness + delta >= 0 && brightness + delta <= 100:
return .On(brightness + delta) // Legal brightness adjustment
        case .On(_):
return state // Out of range, keep in original state
        default:
return state // Non-powered state does not respond
    }
}
```  


## 3. Practical scenario: Network request status machine
### 1. Enumeration defines network request status
```cj
enum NetworkState {
| Idle // Idle status
| Loading // Loading
| Success(data: String) // Success (carry response data)
| Failed(error: Int) // Failed (carrying error code)
}
```  

### 2. Status migration and UI update
```cj
var networkState: NetworkState = .Idle

func fetchData() {
networkState = .Loading // Switch to loading when initiating a request
// Simulate asynchronous requests
let mockResult = random() % 2 == 0 ? .Success("Data") : .Failed(404)
networkState = mockResult // Update to successful or failed state
}

func updateUI() {
    match (networkState) {
        case .Idle:
showButton("Stamp request")

        case .Loading:
            showSpinner()

        case .Success(data):
            showData(data)

        case .Failed(error):
showError("Error code: \(error)")
    }
}
```  

### 3. Compound state processing
Combining the `where` clause to achieve more complex conditional judgment:
```cj
func retryFailedRequest() {
    match (networkState) {
case .Failed(error) where error == 404: // Only handle 404 errors
            fetchData()
case .Failed(_): // Other errors will not be retryed
println("Unsupported error type")
        default:
println("Current status cannot be retryed")
    }
}
```  


## 4. The robustness design of state machine
### 1. Exhaustion check
The compiler mandates that `match` overwrites all enum constructors to avoid unprocessed state.
```cj
// Compilation error: Unhandled .Error and .Updating status
func incompleteHandler(state: DeviceState) {
    match (state) {
case .Off: println("Shutdown")
case .On(_): println("Power on")
    }
}
```  

### 2. Secure default state processing
Use the wildcard `_` as the default branch to handle possible new states in the future.
```cj
func futureProofHandler(state: DeviceState) {
    match (state) {
        case .Off: /* ... */
        case .On(_): /* ... */
        case .Error(_): /* ... */
case _: println("handle unknown state") // Make sure to handle new states in the future
    }
}
```  

### 3. State persistence
By pattern matching deconstructing states, serialization/deserialization of state data is realized.
```cj
func saveState(state: DeviceState) -> String {
    match (state) {
        case .Off: return "Off"
        case .On(brightness): return "On:\(brightness)"
        case .Error(msg): return "Error:\(msg)"
        case .Updating(progress): return "Updating:\(progress)"
    }
}

func loadState(from string: String) -> DeviceState {
    match (string.split(":")) {
        case ["Off"] => .Off
        case ["On", brightness] if let b = Int(brightness) => .On(b)
        case ["Error", msg] => .Error(msg)
        case ["Updating", progress] if let p = Int(progress) => .Updating(progress: p)
default => .Error("Invalid status data")
    }
}
```  


## 5. Summary
The combination of enumeration and pattern matching provides the following advantages for HarmonyOS Next state machine development:
1. **Type safety**: Enumeration ensures that the status value is legal and pattern matching forces all states to be covered;
2. **Logic clear**: The processing logic of each state is concentrated in independent branches, which is easy to maintain;
3. **Super scalability**: When adding a new status, the compiler prompts that the matching logic needs to be updated to avoid omissions.
