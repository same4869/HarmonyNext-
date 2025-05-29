# HarmonyOS Next Expression Full Solution: From Arithmetic Operations to Control Flow
In HarmonyOS Next development, expressions of the Cangjie language are key elements in building program logic.As a technician who has been deeply engaged in this field, I will combine practical experience to analyze in-depth various characteristics of expressions from arithmetic operations to control flow, so as to help everyone fully master their application skills.

## 1. Expression classification
### (I) Comparison of arithmetic/conditional/loop expression types (table induction)
Cangjie language has a variety of expressions, among which arithmetic, conditional and cyclic expressions are the most commonly used types. They have different functions, evaluation methods and usage scenarios. For example, the specific examples are as follows:
|Expression type|Function description|Evaluation method|Usage scenario|Example|
|---|---|---|---|---|
|Arithmetic expressions|Mathematical operations are composed of operands and operators|calculate the operands based on the operators, and obtain the results|mathematical calculations, assignment operations and other scenarios|`let result = 3 + 5;`, and the calculation result `result` is 8|
|Condition expression|Select different code branches to execute according to the conditional judgment result|calculate the value of the conditional expression (Bolean type), and decide which branch to execute based on the truth or false|Scenario where different operations are performed according to different conditions|`if (num > 10) { println("greater than 10"); } else { println("less than or equal to 10"); }`|
|Loop expression|Repeat a piece of code until a specific condition is met|Discribing whether to continue executing the loop body based on the loop condition|Scenario where the same operation needs to be repeated|`for (i in 1..10) { sum += i; }`, realize the accumulation of 1 to 10|

Through table comparison, you can clearly see the characteristics of different types of expressions, and you can choose accurately according to your needs in actual programming.

## 2. Code block evaluation rules
### (I) Unit type verification experiment
In Cangjie language, code blocks are surrounded by a pair of braces "{}", and their evaluation rules affect the program's running logic.The type of the empty code block is Unit and the value is `()`, and this rule can be verified experimentally.For example:
```cj
main() {
    let blockValue = {
// Empty code block
    };
    println(typeOf(blockValue));
}
```
Run the above code and the output result is "Unit", proving that the type of the empty code block is indeed Unit.When there is an expression in a code block, its value and type depend on the last expression.like:
```cj
main() {
    let result = {
        let a = 5;
        a + 3;
    };
    println(result);
}
```
The value of the code block here is 8 and type Int, because the result of the last expression `a + 3` is 8 and type Int.Understanding the code block evaluation rules is crucial to accurately grasping the program's running results and type inference.

## 3. Control transfer expressions
### (I) Practical application of break/continue in Monte Carlo algorithm
In Monte Carlo algorithm, the break and continue control transfer expressions play an important role.Monte Carlo algorithms are often used to estimate numerical values ​​through random simulations.Take the estimation of pi as an example:
```cj
import std.random.*
main() {
    let random = Random()
    var totalPoints = 0
    var hitPoints = 0
    while (true) {
        let x = random.nextFloat64()
        let y = random.nextFloat64()
        if ((x - 0.5) ** 2 + (y - 0.5) ** 2 < 0.25) {
            hitPoints++
        }
        totalPoints++
        if (totalPoints >= 1000000) {
            break;
        }
    }
    let pi = 4.0 * Float64(hitPoints) / Float64(totalPoints)
println("P approximate value is: ${pi}")
}
```
In the above code, `break` is used to terminate the loop when the simulated points reach 1000000, avoid infinite loops, and improve program operation efficiency.If you only want to count odd points falling within the circle, you can use `continue`:
```cj
import std.random.*
main() {
    let random = Random()
    var totalPoints = 0
    var hitPoints = 0
    while (true) {
        let x = random.nextFloat64()
        let y = random.nextFloat64()
        let pointIndex = totalPoints + 1;
        if (pointIndex % 2 == 0) {
            continue;
        }
        if ((x - 0.5) ** 2 + (y - 0.5) ** 2 < 0.25) {
            hitPoints++
        }
        totalPoints++
        if (totalPoints >= 1000000) {
            break;
        }
    }
    let pi = 4.0 * Float64(hitPoints) / Float64(totalPoints)
println("P approximate value is: ${pi}")
}
```
`continue` makes the program skip the judgment of even points and directly enter the next round of loop, reducing unnecessary calculations and optimizing algorithm performance.Reasonable use of `break` and `continue` in complex algorithms can accurately control program flow and improve algorithm efficiency.
