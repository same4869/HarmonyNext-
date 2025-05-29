# HarmonyOS Next Cangjie Language Introduction: Identifiers and Unicode Specification Analysis
In the development environment of HarmonyOS Next, Cangjie Language, as the core development language, mastering its basic concepts is crucial.Among them, identifiers and Unicode specifications are the cornerstones for writing correct and efficient code.As a technician with rich practical experience in this field, I will analyze these key knowledge points in depth based on my experience in actual projects.

## 1. Basic concepts of identifiers
### (I) Comparison of regular identifiers vs original identifier rules (attached legality comparison table)
In Cangjie language, identifiers are divided into ordinary identifiers and original identifiers, and their rules vary significantly.Ordinary identifiers follow strict naming specifications and cannot be the same as Cangjie keywords.Its naming can begin with the XID_Start character in the Unicode standard, followed by the XID_Continue character of any length; or start with a single underscore "_", followed by at least one XID_Continue character.For example, "abc", "_abc", "a1b2c3" are all legal ordinary identifiers."ab&c" ("&" is not an XID_Continue character), "3abc" (number cannot be used as a starting character), "_" (at least one XID_Continue character must be included after underscore) and "while" (which is the Cangjie keyword) are illegal.

The original identifier provides a solution to special needs, which is to add a pair of backticks to the beginning and end of the normal identifier or Cangjie keyword.This allows Cangjie keywords to be used as identifiers, such as "`if`" and "`while`" and so on are all legal original identifiers.However, if the part in the backtick does not comply with the rules of ordinary identifiers, then the entire original identifier is also illegal, such as "`ab&c`" and "`3abc`".For a more intuitive understanding, the following is a comparison through the table:
|Identifier type|Rules|Example (legal)|Example (injury)|
|---|---|---|---|
|Normal identifier|1. Start with XID_Start character, followed by XID_Continue character of any length<br>2. Start with "_" and followed by at least one XID_Continue character<br>3. Cannot be the same as Cangjie keyword|abc, _abc, a1b2c3|ab&c, 3abc, while|
|Original identifier |Put backticks at the beginning and end of normal identifier or Cangjie keyword |`abc`, `if`, `while`|`ab&c`, `3abc`|

### (II) Detailed explanation of Unicode XID_Start/XID_Continue specification
The XID_Start and XID_Continue attributes in the Unicode standard play a key role in naming Cangjie language identifiers.XID_Start contains Chinese, English and other characters, which are allowed as the starting character of the identifier.For example, "Cangjie" is legal as the beginning of an identifier, which reflects the Cangjie language's support for multilingual programming, making it convenient for developers to name it in Chinese with semantic meanings and improve the readability of the code.

In addition to Chinese and English, XID_Continue also covers characters such as Arabic numerals.This means that in the subsequent characters of the identifier, the naming can be enriched with numbers.For identifiers such as "a1b2c3", the addition of numbers can express the meaning more accurately, for example, very practical when denoting a series of variables with numbered properties.A deep understanding of these two specifications will help developers write identifiers that are consistent with the specification and are semantically clear, and avoid compilation errors caused by improper naming.

## 2. NFC standardization practice
### (I) Example of multilingual identifier processing (Chinese/Japanese/Arabic numeral mixing case)
Cangjie Language recognizes all identifiers as the form after Normalization Form C (NFC).This feature is particularly important when dealing with multilingual identifiers.For example, in a project involving internationalization, identifiers containing Chinese, Japanese, and Arabic numerals may be used.Suppose we define an identifier that represents product information "Commodity_No. 1_こんにちは", which will be normalized by NFC in Cangjie language.This ensures consistency and correctness of identifiers in different system environments or encoding methods.

In actual development, different developers may encounter situations where different forms of input the same semantic identifier.For example, someone may enter "Product_No. 1_________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________Through NFC normalization, Cangjie language can accurately identify the consistency of these identifiers, avoid errors caused by subtle character differences, and enhance the robustness and maintainability of the code.

## 3. Keyword avoidance skills
### (I) Scene demonstration of backtick wrapping keywords (while legalization example)
During the programming process, sometimes we do need to use the Cangjie keyword as an identifier, and the original identifier comes in handy.Taking the "while" keyword as an example, using "while" in a normal identifier will cause compilation errors because it conflicts with the loop control keywords of the Cangjie language.But in some special cases, for example, we are developing a module that parses a specific text format, where the word "while" exists as a specific identifier in the text, and we need to reference it in the code.

At this time, you can use the original identifier and wrap "while" in backticks, that is, "`while`".In this way, this string that was originally a keyword can be used as an identifier in the code.For example:
```cj
func processText(text: String) {
    let `while`Index = text.indexOf("while");
    if (`while`Index!= -1) {
// Handle text logic containing "while"
    }
}
```
In this way, we cleverly avoid the naming conflicts caused by keywords, making the code more flexible and easy to understand.In actual projects, this technique is often used in scenarios such as interaction with external data, language analysis in specific fields, etc., and can effectively solve development problems caused by keyword restrictions.

Mastering the identifiers and Unicode specifications of the Cangjie language is an important step in deeply learning and developing HarmonyOS Next applications.Whether it is writing clear and easy-to-understand code in daily development, or solving naming conflicts and other issues when dealing with complex business logic, these basics play a key role.I hope that through the analysis of this article, we can help everyone better understand and apply these concepts and be more skillful in the development path of HarmonyOS Next.
