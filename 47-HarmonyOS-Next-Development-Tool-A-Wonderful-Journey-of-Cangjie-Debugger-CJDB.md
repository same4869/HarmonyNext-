# HarmonyOS Next Development Tool: A Wonderful Journey of Cangjie Debugger CJDB
> This article aims to deeply explore the technical details of Huawei HarmonyOS Next system and summarize them based on actual development practices.
It is mainly used as a carrier of technology sharing and communication, and it is inevitable to miss mistakes. All colleagues are welcome to put forward valuable opinions and questions in order to make common progress.
This article is original content, and any form of reprinting must indicate the source and original author.

In the world of development, debugging is like a detective game, and developers have to find out the problem in the clues of the code like Sherlock Holmes.In HarmonyOS Next development, Cangjie debugger cjdb is our right-hand assistant, which can help us quickly locate and solve problems.Today, let’s talk about how magical this cjdb is.

## cjdb first impression
In previous Android development, the debugging process was like exploring in the fog. Sometimes a small problem may take a lot of time and energy to investigate.And cjdb is like a beacon in HarmonyOS Next development, illuminating the road of debugging for us.It is a debugger specially designed for Cangjie language, which can provide powerful debugging functions, making us more comfortable in the development process.

Imagine you are developing a complex HarmonyOS Next application, like building a large smart city.During the construction process, some minor failures are inevitable, such as the inability to work properly.At this time, cjdb is like an experienced urban repairman who can quickly find fault points and repair them.

cjdb is also very convenient to use. You only need to enter simple commands in the command line to start the debugging session.For example, `cjdb your_program.cj` will help us load the program and prepare the debugging environment, just like a repairman coming to the failure site with a toolkit.

## Actual analysis of cross-language debugging
In HarmonyOS Next development, we often encounter cross-language programming, such as Cangjie language calling C functions.At this time, debugging becomes more complicated, just like communicating between different countries, language barriers will cause a lot of trouble.The cross-language debugging function of cjdb is like an excellent translator, allowing us to switch between different languages ​​freely.

Take a simple code of Cangjie calling the C function as an example:
```cj
// Assume this is Cangjie code
extern func cFunction(): Int64;

func main(): Int64 {
    let result = cFunction();
    return result;
}
```
```c
// This is the corresponding C code
#include <stdio.h>

int cFunction() {
    return 42;
}
```
When we use cjdb for debugging, it can clearly show the changes in the call stack during the single step.When executing to the `cFunction()` call, we can step into the C function inside to view the execution of the C code.Moreover, cjdb can filter out glue code and only display the core code we care about. This is like extracting only useful parts from a bunch of messy information, greatly improving debugging efficiency.

Just like in international exchanges, the translator will help us filter out some irrelevant language habits and polite words and only convey key messages.During the debugging process, we can use the `step into` command to enter the function, use the `step out` command to jump out of the function, and use the `backtrace` command to view the call stack. These operations can give us a clearer understanding of the code execution process.

## In-depth analysis of Cangjie thread debugging
In multi-threaded programming, debugging is like directing a complex symphony. Each thread is like an instrument that requires coordination and cooperation to play wonderful music.In HarmonyOS Next development, Cangjie threads have their unique characteristics, and cjdb's thread debugging function can help us better direct this "symphony".

When Cangjie threads are executed concurrently, various problems may arise, such as thread deadlock, data competition, etc.When we use cjdb for debugging, we can set breakpoints on the Cangjie thread, just like setting a pause point in a symphony, giving us time to check the state of the thread.Through the break thread command, we can pause when the thread is executed to a specific location, and then use the `thread list` command to view the status of all threads, and use the `thread select` command to select the thread to view.

For example, in a multi-threaded HarmonyOS Next application, multiple threads read and write to a shared resource at the same time.If there is a problem of data inconsistency, we can use cjdb to set breakpoints at the critical code, pause thread execution, view the status and data of each thread, and find out the problem.

Just like when the conductor finds that the sound of an instrument is wrong during the performance, he will pause the performance, check the state of the instrument and make adjustments.cjdb can help us quickly locate and solve problems in multi-threaded programming, making our applications more stable and reliable.

In short, in the development of HarmonyOS Next, the cross-language debugging and thread debugging functions of Cangjie debugger cjdb provide us with powerful debugging capabilities, allowing us to be more confident in the development process.I hope everyone can make good use of cjdb in actual development so that debugging is no longer a headache.If you have any new discoveries during use, you are welcome to share them with me. Maybe we can discover more wonderful things about cjdb together!
