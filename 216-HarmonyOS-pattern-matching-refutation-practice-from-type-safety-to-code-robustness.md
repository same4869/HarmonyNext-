# HarmonyOS pattern matching refutation practice: from type safety to code robustness

In Hongmeng development, the refutability of the pattern is the key to avoiding runtime errors.When I first came into contact, I had compiled errors because I didn’t understand the refutation pattern. Later, I fell into a trap in the project and truly understood it: this is not a theoretical concept, but a necessary skill for writing robust code.The following is a combination of practical experience to share how to build a safe matching logic using refutable and irrefutable patterns.


## 1. Refutation mode: "Possible failure" scenarios that must be handled

### 1. Which modes may fail?
This type of model is like a trapped intersection, and if it is not handled, there will be problems:

| Pattern Type | Example | Failure Scenario |
|----------------|---------------------|---------------------------|  
| Constant mode | `case 10` | Match failed when the value is 20 |
| Enumeration partial match | `case Add(n)` | Failed when it is actually a Sub constructor |
| Type pattern | `case dog: Dog` | Failed when it is actually Cat type |
| Tuple does not match exactly | `case (1, x)` | Failed when the first element of the tuple is not 1 |

### 2. The pitfalls of forced processing during compilation
```cj
enum Color { | Red | Green | Blue }

func printColor(c: Color) {
    match c {
case Red => print("red")
// Compile error: Missing patterns for Green and Blue
    }
}
```  
**Solution**:
- or overwrite all constructors
- Or use the wildcard `case _` to guarantee the bottom

### 3. The correct way to open the refutation mode
When dealing with Option types, the None case must be considered:
```cj
let maybeNum: Option<Int> = None

// Correct way: Use if-let to handle the refuted Some(n) mode
if let Some(n) = maybeNum {
    print(n)
} else {
print("No value") // None scenario must be handled
}
```  


## 2. Unrefutable mode: a surely successful "safe channel"

### 1. These models are always reliable
Just like a check-free channel, no need to worry about matching failure:

| Pattern type | Example | Reasons for sure success |
|----------------|---------------------|-------------------------|  
| Wildcard pattern | `case _` | Match any value |
| Bind Mode | `case x` | Capture values ​​and bind to variables |
| Single constructor enum | `case Data(n)` | Enumeration has only one constructor |
| Complete tuple matching | `case (a, b)` | The number of tuple elements is exactly the same |

### 2. Safe usage of variable destruction
```cj
// Tuple deconstruction (not refuted)
let (x, y) = (10, 20) // Get x=10, y=20 directly

// Single constructor enumeration destruction
enum OnlyOne { | Value(String) }
let Value(str) = OnlyOne.Value("ok") // Get str="ok" directly
```  

### 3. Safe traversal of for-in loop
```cj
let nums = [1, 2, 3]
for num in nums { // Unrefutable binding mode
    print(num)
}

// Single constructor enumeration collection
enum Item { | Data(String) }
let items = [Item.Data("a"), Item.Data("b")]
for Item(str) in items { // Get str directly
    print(str)
}
```  


## 3. How does the compiler check the rebutability?

### 1. Strict inspection of refutation mode
```cj
enum Three { | A | B | C }

func check(e: Three) {
    match e {
        case A => ()
// Compile error: Missing patterns for B and C
    }
}
```  
**Compiler Logic**: Refutation mode must cover all possibilities, otherwise it will not be allowed to pass

### 2. A loose policy of irrefutable mode
```cj
func anyValue(x: Int) {
    match x {
case _ => () // No refutation, no other branches are needed
    }
}
```  
**Reason**: Wildcard pattern must match, no additional processing is required

### 3. Matching order of mixed patterns
```cj
enum Mix { | Num(Int) | Other }

func process(m: Mix) {
    match m {
case Num(n) => print(n) // The refutation pattern can be matched first
case _ => print("other") // Cannot be refuted
    }
}
```  
**Principle**: You can place the refutation mode in front, but you can not place the refutation behind.


## 4. Refutable application in actual combat

### 1. Secure parsing nullable data
```cj
let maybeStr: ?String = "test"

match maybeStr {
case Some(s) => print(s) // Refute mode to handle Some situation
case None => print("no data") // None must be processed
}
```  

### 2. Forced deconstruction of non-null values
```cj
let sureStr = "hello"
let Some(s) = sureStr // Not refuted, equivalent to let s = sureStr
print(s) // Direct output
```  

### 3. Safe traversal of recursive enumeration
```cj
enum List {
| Empty // The irrefutable basic situation
| Node(Int, List) // Refuted recursive situation
}

func traverse(l: List) {
    match l {
case Empty => print("empty") // Termination condition
case Node(n, rest) => { // Handle recursive cases
            print(n)
            traverse(rest)
        }
    }
}

traverse(List.Node(1, List.Node(2, List.Empty))) // Output 1 2
```  


## 5. Pit avoidance guide: From stepping on a pit to filling a pit

1. **Refutation mode missed handling**:
Develop the habit of writing wildcard characters first when matching enums

2. **Unrefutable mode misuse**:
Do not use irrefutable modes in scenarios that may fail, such as:
   ```cj
   let maybeNil: ?Int = None
let Some(n) = maybeNil // Crashed during runtime, no refutation mode misuse
   ```  

3. **Match order inverse**:
The refutable mode must be placed before the non-refutable mode, otherwise it will never match.


## Conclusion
After understanding the refutation of the pattern, compile-time errors were reduced by 60% when dealing with enumeration and nullable values ​​in the Hongmeng project.This mechanism is like a safety net of code: a refutation mode forces you to deal with all possible situations, while an unrefutation mode makes the determined scenario simpler.Next time you encounter a compilation error "Non-exhaustive patterns", remember that this is the compiler helping you avoid crashing during runtime.
