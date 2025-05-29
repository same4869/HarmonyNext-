# HarmonyOS Next development must be done: an in-depth understanding of Cangjie Language Pack Manager cjpm
> This article aims to deeply explore the technical details of Huawei HarmonyOS Next system and summarize them based on actual development practices.
It is mainly used as a carrier of technology sharing and communication, and it is inevitable to miss mistakes. All colleagues are welcome to put forward valuable opinions and questions in order to make common progress.
This article is original content, and any form of reprinting must indicate the source and original author.

Everyone who works in development knows how troublesome the dependency management and construction process is, it’s like looking for threads in a mess, and if you don’t pay attention, you will be confused.However, in the development of HarmonyOS Next, Cangjie language package manager cjpm is like a pair of sharp scissors, helping us easily cut these "messies". Today, let's talk to you about how powerful cjpm is!

## cjpm basic cognition
In the past, when it was Android development, management dependence was like a nightmare.Version conflicts of various libraries often lead to compilation failures, and developers have to spend a lot of time to troubleshoot and resolve them.In HarmonyOS Next development, the emergence of cjpm is simply a savior.It is a package manager specially designed for Cangjie language projects and is responsible for project-level compilation and construction, which is very important.

Imagine you want to build a complex building block castle (project), each building block (dependence module) has different specifications and versions.Without a good management method, these building blocks may be piled up in a mess and cannot be used at all.cjpm is like a caring building block organizer, helping you sort these building blocks out and sorting them out so that you can build a castle smoothly.

In the HarmonyOS Next development environment, we can use cjpm with simple commands.For example, to initialize a new project, just enter `cjpm init` on the command line, and it will help us create the basic structure of the project, just like laying the foundation before building a castle, preparing for subsequent development.

## Automatic dependency management exploration
I believe many developers have encountered conflicts in multiple versions of module dependence.Take a HarmonyOS Next application I developed before for example. Module A and Module B were introduced in the project. Module A depended on version 1.3 of Module C, and Module B depended on version 1.4 of Module C.If it is in Android development, this situation is likely to cause a compilation error, and the developer has to manually coordinate the versions of each module, which is cumbersome and prone to errors.

But with cjpm it’s different!Its automatic dependency management function is like having a pair of "smart eyes" that can automatically analyze all dependencies in the project.Take the example just now, cjpm will analyze different versions of module C, calculate the final dependency, and merge similar items.When compiling and building, developers only need to execute the `cjpm build` command, and it will automatically handle everything without worrying about dependency conflicts.It's like you ask a smart assistant to organize building blocks, which can automatically put the same type of building blocks together, making it easier for you to build a castle.

To make it clearer, let's look at a simple sample code (assuming this is part of the project's dependency configuration file):
```json
{
  "dependencies": {
    "moduleA": "^1.0",
    "moduleB": "^2.0"
  }
}
```
Here, module A and module B may each rely on other modules, and cjpm will silently handle these dependencies behind the scenes, making development extremely smooth.

## The power of custom builds
In actual development, we often have some special needs, such as configuring environment variables before compilation, copying external dependency libraries, or performing some cleaning work after compilation.In Android development, implementing these functions may require the help of a variety of tools, which is more troublesome to operate.But in HarmonyOS Next development, the custom build functionality provided by cjpm makes it all simple.

Taking a project I developed involving CFFI (Foreign Function Interface) as an example, you need to compile C files before compiling.I did this by defining the predecessor task in the `build.cj` file:
```cj
func stagePreBuild(): Int64{
// Customize the processing before compilation, execute the command to compile the C file here
    exec("cd {workspace}/cffi && cmake && make install")
    return 0
}
```
In this way, when executing the `cjpm build` command, cjpm will first execute the command in the `stagePreBuild` function to complete the compilation of the C file.After compilation is complete, I can also define post-tasks to clean temporary files:
```cj
func stagePostBuild():Int64{
// Customize the processing after compilation and delete the CFFI source code
    exec("rm -rf {workspace}/cffi")
    return 0
}
```
In this way, we can add our own custom operations at different stages of the construction to realize one-stop construction management of the project, greatly improving development efficiency.This is like when you build a building block castle, you can not only follow the regular steps, but also prepare special building blocks before building, and clean up the useless building blocks after building, making the whole process more flexible and efficient.

In short, in the development of HarmonyOS Next, the automatic dependency management and custom construction functions of Cangjie language's package manager cjpm saves developers a lot of time and energy, making the development process smoother.I hope everyone can make good use of cjpm in actual development to create better HarmonyOS Next applications!If you have any problems during use, please feel free to communicate and discuss. Maybe you can create more development "small sparks"!
