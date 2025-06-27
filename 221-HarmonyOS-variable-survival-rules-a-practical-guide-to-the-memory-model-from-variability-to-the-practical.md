# HarmonyOS variable survival rules: a practical guide to the memory model from variability to the practical

> As an old driver who was cheated by variables in Hongmeng development, he once caused equipment data to be confused due to misuse of reference types, and was tortured by the compiler's conservative strategy.This article combines practical experience to analyze the survival rules of the Cangjie language variable system to help you avoid variable-related pitfalls.


## 1. Let/var's philosophy of survival: the principle of immutable priority

### 1.1 Life and death line in concurrent scenarios
Immutable variables are life-saving characters in concurrency, and mutable variables are time bombs:

```cj
// Dangerous variable variables (concurrent scenarios)
var counter = 0
let thread1 = async { counter += 1 }
let thread2 = async { counter += 1 }
awaitAll([thread1, thread2])
println(counter) // Possible output 1 (race condition)
```  

```cj
// Safe immutable variables (functional style)
let initial = 0
let result = awaitAll([
    async { initial + 1 },
    async { initial + 1 }
]).reduce(0, +)
println(result) // Ensure output 2
```  

**Practical principles**:
- Use `let` first to avoid race conditions for sharing data
- When it must be variable, wrap it with `AtomicReference`


## 2. Value type vs reference type: survival form in memory

### 2.1 Memory survival difference between struct and class
The value type is like an independent living body, and the reference type is like an egg twin:

```cj
// Value type struct (Survival independently)
struct Point {
    var x: Int
    var y: Int
}

let p1 = Point(x: 1, y: 2)
let p2 = p1 // Generate independent replica
p2.x = 3
println(p1.x) // Output 1 (not affected)
```  

```mermaid
graph TD
A[stack memory] --> B[p1(x:1,y:2)]
A --> C[p2(x:1,y:2)]
```  

```cj
// Reference type class (shared survival)
class Point {
    var x: Int
    init(x: Int) { this.x = x }
}

let p1 = Point(x: 1)
let p2 = p1 // Share the same object
p2.x = 3
println(p1.x) // Output 3 (affected)
```  

```mermaid
graph TD
A[stack memory] --> B[p1(points to heap object)]
A --> C[p2 (points to the same bunch of objects)]
D[heap memory] --> E[object(x:1, then becomes 3)]
```  

### 2.2 Survival strategy selection
| Scene | Select Type | Survival Advantages |
|--------------|----------|------------------------|  
| Small data independent operation | struct | efficient replication, no sharing risk |
| Big data sharing operation | class | High memory efficiency and convenient sharing |


## 3. The conservative survival strategy of the compiler

### 3.1 Variable survival crisis in try-catch
Compilers like overprotected parents must ensure that the variable "living":

```cj
// Compiler error case
let a: String
try {
    a = "success"
} catch {
// The compiler believes that a may not be initialized
    // Error: Variable 'a' used before being initialized
}
```  

**Survival Plan**:
1. Initialize in advance: `let a: String = ""`
2. Use optional type: `let a: String? = nil`

### 3.2 The rules of variable survival in closures
Closure capture variables are like "parasitic", and you need to pay attention to your life cycle:

```cj
func createTimer() -> () -> Void {
    var count = 0
    return {
        count += 1
        println(count)
    }
}

let timer = createTimer()
timer() // output 1
timer() // Output 2 (count is captured by closure and remains state)
```  


## 4. Variable survival practice: bank account cases

### 4.1 Value Type Account (Safe but Inefficient)
```cj
struct BankAccount {
    let id: String
    var balance: Double
    
    func withdraw(amount: Double) -> BankAccount {
// Return to a copy of the new account
        return BankAccount(id: id, balance: balance - amount)
    }
}

let account = BankAccount(id: "123", balance: 1000)
let newAccount = account.withdraw(amount: 200)
```  

### 4.2 Reference type account (efficient but cautious)
```cj
class BankAccount {
    let id: String
    var balance: Double
    
    init(id: String, balance: Double) {
        self.id = id
        self.balance = balance
    }
    
    func withdraw(amount: Double) {
balance -= amount // directly modify the status
    }
}

let account = BankAccount(id: "123", balance: 1000)
account.withdraw(amount: 200)
```  


## 5. Guide to avoiding variable survival

1. **Immutable priority**: Use `let` first for 90% of variables, and then use `var` when it is necessary to change it.
2. **Value type priority**: Use `struct` for small data, and use `class` for big data.
3. **Closure Trap**: Avoid catching mutable variables in closures, and use immutable + functional style instead.
4. **Compiler-friendly**: Follow the compiler conservative strategy and handle variable initialization in advance
