
# HarmonyOS Next match expression depth analysis: match with value and without value

In HarmonyOS Next development, the `match` expression is the core control structure for implementing pattern matching.Cangjie Language supports match expressions with match values** and match expressions without match values**. There are significant differences in the syntax structure and application scenarios.This article combines document knowledge points to analyze the core usage, matching logic and best practices of these two types of expressions.


## 1. Match expression with matching values: accurate value-driven branch control
The `match` expression with matching values ​​realizes conditional branch logic through the comparison of the values ​​to be matched one by one, which is suitable for scenarios such as enumeration value judgment, numerical range matching, etc.

### 1. Basic syntax structure
```cj
match (match value) {
case pattern 1 => expression or statement block
case pattern 2 | pattern 3 => expression or statement block
// Other case branches
}
```  
- **Match value**: Can be any expression (such as variables, function return values).
- **Mode**: Supports various types such as constant mode, enumeration mode, tuple mode, etc.

### 2. Execution process and matching rules
1. Match the pattern of the `case` branch one by one in order;
2. Once the match is successful (including the `pattern guard` condition is true), execute the corresponding branch code and exit `match`;
3. If all patterns do not match, a compilation error will be triggered (unless the wildcard character `_` is used to guarantee the problem).

**Example: Enumeration value matching**
```cj
enum Color { | Red | Green | Blue }
let c = Color.Green

match (c) {
case Red => println("red")
case Green => println("green") // The match is successful, and the output is "green"
case Blue => println("blue")
}
```  

### 3. Advanced Filtering for Pattern Guard
Add extra conditions through the `where` clause to achieve more granular matching logic:
```cj
enum Number { | Odd(Int) | Even(Int) }
let num = Number.Odd(7)

match (num) {
case Odd(n) where n > 5 => println("\(n) is an odd number greater than 5") // Match successfully
case Odd(n) => println("\(n) is an odd number")
case Even(n) => println("\(n) is an even number")
}
```  


## 2. Match expression without matching values: conditionally driven logical branch
The `match` expression without a matching value realizes logic similar to multi-condition `if-else` by judging the Boolean expression after `case`, which is suitable for complex condition combination scenarios.

### 1. Basic syntax structure
```cj
match {
case boolean expression 1 => expression or statement block
case boolean expression 2 => expression or statement block
// Other case branches
}
```  
- **Bool expression**: It can be an expression that returns `Bool` by variable comparison, function calls, etc.
- **Special Syntax**: `case _` is equivalent to `case true`, as the default branch.

### 2. Execution process and matching rules
1. Calculate the boolean expressions after each `case` in order;
2. The first branch with the result of `true` is executed and then exits `match`;
3. If all expressions are `false` and there is no `case_`, an error is reported in the compilation.

**Example: Numerical range judgment**
```cj
let x = 25

match {
case x < 0 => println("negative")
case x >= 0 && x < 10 => println("bet 0-9")
case x >= 10 && x < 20 => println("bet 10-19")
case _ => println("20 and above") // The matching is successful, and the output is "20 and above"
}
```  

### 3. Performance comparison with `if-else if`
The conditional judgment order of the `match` expression is consistent with `if-else if`, but the syntax is more concise, especially suitable for multi-conditional hierarchical scenarios:
```cj
// match expression
match {
    case isNetworkAvailable() && hasPermission() => fetchData()
case isNetworkAvailable() => showError("Insufficient permissions")
case _ => showError("no network")
}

// Equivalent if-else if structure
if (isNetworkAvailable() && hasPermission()) {
    fetchData()
} else if (isNetworkAvailable()) {
showError("Insufficient permission")
} else {
showError("No network")
}
```  


## 3. Mixed scenarios: the collaborative application of two match expressions
In actual development, two types of `match` expressions can be combined to process complex business logic.

### 1. Type matching first, then conditional filtering
```cj
let value: Any = 105

// First determine whether it is Int through the type mode
match (value) {
    case n: Int => {
// Then judge the range by match without value
        match {
case n < 0 => println("negative integer")
case n < 100 => println("Integer less than 100")
case _ => println("Integer greater than or equal to 100") // Output "Integer greater than or equal to 100"
        }
    }
case _ => println("non integer type")
}
```  

### 2. Combining enum values ​​with boolean conditions
```cj
enum UserStatus { | Active | Inactive(Int) }
let status = UserStatus.Inactive(30)

match (status) {
case Active => println("User Active")
    case Inactive(days) => {
        match {
case days < 7 => println("Not active less than 7 days")
case days < 30 => println("Not active for 7-30 days")
case _ => println("not active for more than 30 days") // Output "not active for more than 30 days"
        }
    }
}
```  


## 4. Common traps and best practices
### 1. Exhaustion requirements for value matching
Enumerate all constructors or use wildcards, otherwise the compiler will be errored:
```cj
enum E { | A | B | C }
func f(e: E) {
    match (e) {
        case A => ()
        case B => ()
// Missing C branch, compilation error: "Non-exhaustive patterns"
    }
}
```  

### 2. Condition order without value matching
Ensure that conditions are from specific to general and avoid logical overwriting:
```cj
let x = 50
match {
case x == 50 => println("equal to 50") // Preferentially match specific conditions
case x > 30 => println("greater than 30")
case _ => println("Other")
}
```  

### 3. Avoid redundant pattern matching
For a single condition, use `if` instead of `match` to improve readability:
```cj
// Counterexample: Overuse of match
let isLogin = true
match {
case isLogin => println("Login")
case _ => println("Not logged in")
}

// Affirmative example: use if-else
if (isLogin) {
println("Logined")
} else {
println("Not logged in")
}
```  


## Summarize
HarmonyOS Next's `match` expression provides flexible logical control capabilities through two types of patterns:
- **Value matching** is suitable for precise branches based on specific values ​​(such as enumerations, numerical values);
- **Match without value** is suitable for conditional combination judgments (such as Boolean logic, range check).
