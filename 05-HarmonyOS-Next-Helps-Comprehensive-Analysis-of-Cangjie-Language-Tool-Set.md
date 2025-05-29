# HarmonyOS Next Helps: Comprehensive Analysis of Cangjie Language Tool Set
> This article aims to deeply explore the technical details of Huawei HarmonyOS Next system and summarize them based on actual development practices.
It is mainly used as a carrier of technology sharing and communication, and it is inevitable to miss mistakes. All colleagues are welcome to put forward valuable opinions and questions in order to make common progress.
This article is original content, and any form of reprinting must indicate the source and original author.

In the development field of HarmonyOS Next, it is like being in a tense and exciting battle, and the Cangjie language tool set is the "secret weapon" in our hands.With it, the development process will be as smooth as a cheat.Today, let’s take a deeper analysis of this powerful tool set.

## Toolset Overview
Imagine that the development of HarmonyOS Next is a magnificent construction project, and the various tools provided by Cangjie Language around the development process are like various professional equipment on the construction site.The package manager cjpm is like a material deployer, responsible for managing the various dependency packages required by the project, ensuring that the "materials" required by the project are in place accurately; the debugger cjdb is like an engineering quality inspector, which can accurately identify problems during the code operation; the test framework is like an engineering acceptor, which conducts comprehensive inspection of the quality of the code; the IDE plug-in is like a multi-function toolbox for construction workers, providing developers with a convenient development environment.

In Android and iOS development, we often need to switch between different tools, just like borrowing different devices at different construction sites, which are inefficient and error-prone.In the development of HarmonyOS Next, the Cangjie Language Tools Collection integrates these functions together to form a complete ecosystem, allowing developers to complete development, debugging, testing and other tasks in one-stop, greatly improving development efficiency.

## Interpretation of core functions of each tool
### Package Manager cjpm
One of the core functions of cjpm is automatic dependency management.In traditional development, dependency management is like finding something in a chaotic repository, and version conflict issues are often a headache.cjpm can automatically analyze dependencies in the project, just like a smart warehouse administrator, rationally configuring dependencies from different versions.For example, when a project depends on both the 1.0 version of module A and the 2.0 version of module B, and module B depends on the 1.1 version of module A, cjpm will automatically calculate the final dependency and merge similar items to ensure that the project can be compiled smoothly.

```json
{
    "dependencies": {
        "moduleA": "^1.0",
        "moduleB": "^2.0"
    }
}
```

The above code shows the project's dependency configuration, and cjpm will automatically handle the dependency relationship based on this configuration.

### Debugger cjdb
The cross-language debugging function of cjdb is unique.In HarmonyOS Next development, we may use Cangjie language to call C functions, which involves cross-language debugging issues.cjdb is like a translator who is proficient in multiple languages, allowing us to freely shuttle between codes in different languages.For example, when we are debugging a Cangjie code that calls a C function, cjdb can let us step into the C function, view its execution process, and filter out the glue code, allowing us to focus on debugging the core code.

### Test framework
The test framework includes the unit testing framework, the Mocking testing framework and the benchmarking framework.The unit testing framework is like a strict quality inspector, carefully checking every small unit of the code.For example, we can write a simple unit test case to test the function of a function:

```cj
func testFunction() {
    let result = someFunction();
    assert(result == expectedValue);
}
```

The Mocking test framework can simulate various external environments, allowing us to test the code in different scenarios.The benchmarking framework can help us evaluate the performance of our code and find performance bottlenecks.

### IDE plugin
IDE plug-in provides developers with a convenient development environment.It is like a considerate assistant, which can automatically complete code completion, syntax check and other tasks.On VSCode and Huawei DevEco Studio docks, plug-ins allow developers to use out of the box and improve development efficiency.

## Summary of tool usage scenarios and advantages
The synergy of these tools is fully utilized in the actual HarmonyOS Next project development.For example, when developing a smart home application, we can use cjpm to manage project dependencies to ensure the normal operation of each module; use cjdb to debug the code, quickly locate and solve problems; use the test framework to conduct comprehensive testing of the code to ensure the stability and performance of the application; use the IDE plug-in to improve development efficiency.

Compared with development technologies such as Android and iOS, the advantages of Cangjie language tool set are very obvious.Its integrated design allows developers to avoid frequent switching between multiple tools, reducing development costs and time.At the same time, it has been optimized for the characteristics of HarmonyOS Next, which can better adapt to new needs such as distributed development.

In short, Cangjie Language Toolset is an indispensable tool in the development of HarmonyOS Next.It provides developers with comprehensive and efficient development support, allowing us to create excellent HarmonyOS Next applications more easily.Developers must make good use of these tools in actual development to make the development road smoother!If we encounter any problems during use, we can discuss them together, and maybe we can create more development inspiration!
