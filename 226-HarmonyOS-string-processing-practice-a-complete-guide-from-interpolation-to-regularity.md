# HarmonyOS string processing practice: a complete guide from interpolation to regularity

> As an old developer who has processed massive text in Hongmeng development, he has used garbled code in international applications due to string encoding problems, and has also been pitted by regular performance.This article combines practical experience and shares the core skills of string processing in Cangjie language to help you avoid common traps.


## 1. Three forms of string literal quantity

### 1.1 Literal type and escape rules
| Type | Definition Method | Escape Rules | Typical Scenarios |
|----------------|-------------------|---------------------------|---------------------------|  
| Single-line string | `""` or `''` | Support `\n`, `\"`, etc. | Short text, label |
| Multi-line string | `"""` or `'''` | Keep original line breaks | SQL statements, HTML fragments |
| Original string | `#"..."#` | No escape characters | Regular expressions, path strings |

### 1.2 Practical Selection Guide
```cj
// Single line string (short text)
let title = "HarmonyOS"

// Multi-line string (SQL statement)
let sql = """
SELECT * FROM users 
WHERE age > 18
"""

// Original string (regular expression)
let regex = #"\d{4}-\d{2}-\d{2}"# // Match date
```  


## 2. The art of string interpolation

### 2.1 Basic Interpolation Syntax
```cj
let name = "Zhang San"
let age = 28
let info = "User \(name) Age \(age) Year" // "User Zhang San Age 28"

// Expression interpolation
let result = "Calculation result: \(10 * 2 + 5)" // "Calculation result: 25"
```  

### 2.2 Format interpolation
```cj
let price = 19.99
let date = Date()

// Digital formatting
let priceStr = "Price: ¥\(price, .fixed(2))" // "Price: ¥19.99"

// Date formatting
let dateStr = "Date: \(date, .dateTime.short)" // "Date: 2023/10/15"
```  

### 2.3 Multi-line interpolation skills
```cj
let user = User(name: "Li Si", email: "lisi@example.com")

let profile = """
User Information:
Name: \(user.name)
Email: \(user.email)
"""
```  


## 3. Core skills of Unicode processing

### 3.1 Character and encoding processing
```cj
let str = "Hello, Hello!"

// UTF-8 byte traversal
for byte in str.utf8 {
print("\(byte) ") // Output UTF-8 byte sequence
}

// UTF-16 code unit traversal
for unit in str.utf16 {
print("\(unit) ") // Output UTF-16 code unit
}

// Get Unicode scalar
for scalar in str.unicodeScalars {
print("\(scalar.value) ") // Output Unicode code point
}
```  

### 3.2 International text processing
```cj
// String normalization
let normalized = "Café".normalized(to: .nfkd) // Handle diacritic notes

// Language sensitivity comparison
let compareOptions = CompareOptions()
compareOptions.locale = "fr" // French comparison rules
let result = "Château".compare("Chateau", options: compareOptions)
```  


## 4. Regular expression practice

### 4.1 Basic matching syntax
```cj
import std.regex.*

// Match email address
let emailRegex = Regex("[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\\.[A-Za-z]{2,}")
let email = "user@example.com"
if emailRegex.match(email) {
print("Valid Email")
}

// Match mobile phone number (China)
let phoneRegex = Regex("1[3-9]\\d{9}")
```  

### 4.2 Capture Groups and Grouping
```cj
// Extract the domain name in the URL
let urlRegex = Regex("https?://(\\w+\\.\\w+)/.*")
let url = "https://harmonyos.com/docs"
if let match = urlRegex.match(url) {
    let domain = match.group(1)  // "harmonyos.com"
}

// Match HTML tags
let htmlRegex = Regex("<(\\w+)>(.*?)</\\1>")
let html = "<div>content</div>"
let matches = htmlRegex.findAll(html)
```  

### 4.3 Regular performance optimization
```cj
// Precompiled regularity (improve multiple matching performance)
let regex = Regex.compile("#\\d+") // Precompile tags matching form #123

// Lazy matching (avoid greedy matching)
let lazyRegex = Regex("<div.*?>.*?</div>") // Non-greedy match
```  


## 5. Practical pit avoidance guide

### 5.1 String operation trap
1. **Immutability Note**:
```cj
let str = "Hello"
// str += " World" // Error: String is immutable
let newStr = str + "World" // Correct: Create a new string
```  

2. **Coding conversion risk**:
```cj
// Counterexample: Unspecified encoding causes garbled code
let data = "Chinese".toByteArray()
let str = String(data: data) // It may be garbled

// Formal example: Specify UTF-8 encoding
let str = String(data: data, encoding: .utf8)
```  

### 5.2 Regular Expression Trap
1. **Greedy Matching Problem**:
```cj
// Counterexample: Greedy match leads to error
let regex = Regex("<div>.*</div>") // Match the first <div> to the last</div>

// Positive example: lazy matching
let regex = Regex("<div>.*?</div>") // Match the most recent </div>
```  

2. **Performance Optimization**:
```cj
// Counterexample: Repeat compilation rules
for item in list {
Regex("pattern").match(item) // Compile every time
}

// Formal example: precompiled regular
let regex = Regex("pattern")
for item in list {
    regex.match(item)
}
```  


## 6. Summary: Best practices for string processing

1. **Literal selection**: Use single line for short text, use three quotation marks for multiple lines, and use original string for regular text
2. **Interpolation skills**: Complex expressions are wrapped in brackets, and formatted with modifiers such as `.fixed`, `.scientific`, etc.
3. **Unicode processing**: Use `unicodeScalars` to traverse, and use `CompareOptions` to internationalize
4. **Regular optimization**: Precompiling common rules, using lazy matching to avoid performance problems
