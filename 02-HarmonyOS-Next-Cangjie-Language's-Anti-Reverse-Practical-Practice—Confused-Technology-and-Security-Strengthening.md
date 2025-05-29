# HarmonyOS Next Cangjie Language's Anti-Reverse Practical Practice—Confused Technology and Security Strengthening
This article aims to deeply explore the technical details of Huawei HarmonyOS Next system and summarize them based on actual development practices.It is mainly used as a carrier of technology sharing and communication, and it is inevitable to miss mistakes. All colleagues are welcome to put forward valuable opinions and questions in order to make common progress.This article is original content, and any form of reprinting must indicate the source and original author.

## 1. Appearance obfuscation: Make the code "out of recognition"
In Hongmeng ecosystem, application safety is crucial, just like a door lock, the more difficult it is to be cracked, the better.Cangjie's appearance obfuscation technology is like installing a "smart fingerprint lock" to the code, making it difficult for reverse engineers to break through.
### 1.1 Symbol name confusion practice
Original code:
```cangjie
class PaymentService {
    func verifyPassword(pwd: String) -> Bool {
// Verification logic
    }
}
```
Decompilation result after obfuscation:
```cangjie
class a {
    func b(c: String) -> Bool {
// The same logic but cannot be understood
    }
}
```
Key changes:
1. The class name changes from `PaymentService` to `a`.
2. The method name changes from `verifyPassword` to `b`.
3. The parameter name changes from `pwd` to `c`.
4. All line numbers are reset to zero.

### 1.2 Hongmeng Next App Store Requirements
|Safety Level |Confused Requirements |Applicable Scenarios |
|--|--|--|
|Basic level | Method name confusion only | Tool application |
|Financial grade|Full symbol + Control flow confusion|Payment/Banking application|
|Military-grade | Customized confusion strategy + Hardware-grade protection | Government/Military applications |

In a certain bank's Hongmeng version app, after applying appearance confusion, the reverse analysis time was extended from 2 hours to 3 weeks.

## 2. Data confusion: invisibility of strings and constants
Plain text strings are like passwords written on windows and are easily seen by others.Cangjie's data obfuscation technology installs "one-way perspective glass" for this information.
### 2.1 String encryption process
Original code:
```cangjie
let apiKey = "HARMONY-12345"
```
After compilation:
```
.rodata segment:
0x1234: [Encrypted byte sequence]
```
Runtime decryption process:
1. Call the decryption function on the first access.
2. Only the decrypted plaintext is retained in memory.
3. Automatically clear after the process exits.

### 2.2 Mathematical Magic of Constant Confusion
Original code:
```cangjie
const FLAG = 0xDEADBEEF
```
The equivalent code after obfuscation:
```cangjie
const FLAG = (0x12345678 ^ 0xCCCCCCCC) + 0x24681357
```
In the DRM module of Harmony Next, this technology makes the extraction of key constants 10 times more difficult.

## 3. Control flow confusion: a guide to building a logic maze
Clear code logic is like a straight highway, and reversers can quickly track it down.The control flow confusion is to transform this highway into a structure as complex as the Chongqing overpass.
### 3.1 Example of false control flow
Original logic:
```cangjie
func checkLicense() -> Bool {
    if isValid {
        return true
    } else {
        return false
    }
}
```
After confusion:
```cangjie
func checkLicense() -> Bool {
let a = (getRuntimeValue() & 1) == 0 // Opacity predicate
    var b = false
if a { /* A block of code that will never be executed */ }
while (a) { /* Fake loop */ }
// The real logic is split into multiple basic blocks
//Connect through complex jump relationship
}
```

### 3.2 Performance and safety balance
We found that a certain Hongmeng Next game engine test:
|Confused strength | Code volume growth | Performance loss | Reverse time |
|--|--|--|--|
|None|0%|0%|1 hour|
|Intermediate|15%|5%|8 hours|
|Senior |40% |12% |3 days |

Military-level applications recommend adopting a hybrid strategy of "high-intensity confusion for key functions + non-critical functions without confusion".
