# Performance first: Compilation optimization and runtime innovation of HarmonyOS Next Cangjie language
Performance has always been one of the key indicators that system-level application developers are extremely concerned about.In a system like HarmonyOS Next, which emphasizes multi-device collaboration, end-edge cloud collaboration, and needs to be adapted to resource-sensitive environments, each CPU resource and every megame of memory play an important role.

To meet these challenges, Cangjie language (Cangjie) integrates performance optimization into the entire language system from the beginning of design.From the compiler to the runtime, all links have been carefully designed to pursue excellent execution efficiency while ensuring a good development experience.Next, I will combine practical experience to take you into the in-depth understanding of Cangjie's innovative ideas and practical achievements in compilation optimization and runtime design.

## Cangjie compiler optimization system: full stack acceleration, ultimate performance
Cangjie Language uses a hierarchical compilation optimization system, which meticulously divides the optimization logic into different stages, and each level has specific optimization goals.
### 1. High-level IR (CHIR) optimization
The Cangjie compiler will first convert the source code into an intermediate representation called CHIR (Cangjie High-level IR), and at this level it will carry out a series of advanced semantic optimizations:
|Optimization means | Description |
|--|--|
|Semantic-aware loop optimization | Identify parallel and expandable loop structures to improve operation speed |
|Intelligent inline|Automatically inline small functions to reduce call overhead|
|Dead code elimination | Remove invalid code branches to reduce the volume of the final generated binary file|
|Type inference accelerates optimization |Improving the efficiency of generic expansion and specialization |

Practical experience: When dealing with complex business code, the compiler's construction time is extremely short, and the generated target files are not only small in size, but also perform very well.

### 2. Backend instruction-level optimization
After completing CHIR optimization, Cangjie compiler will also implement a series of underlying instruction-level optimizations on the backend:
|Technology|Instructions|
|--|--|
|SLP vectorization|Automatically identify data parallel code and achieve acceleration with the help of SIMD instructions|
|Intrinsic optimization | Directly call the underlying instructions for key algorithms (such as encryption and compression algorithms) |
|InlineCache optimization | Cache the hot paths of dynamic distribution scenarios to speed up function calls |
|Interprocess pointer optimization (IPA) | Optimize pointer access across modules to reduce the overhead of indirect addressing |

These optimizations have fully tapped the potential of hardware and have particularly significant advantages in multi-core and heterogeneous computing platforms.

### 3. Runtime dynamic optimization (combination of JIT/AOT)
Cangjie runtime supports runtime optimization (Runtime Optimization), including the following aspects:
1. Lightweight Lock: replaces the system's relock mechanism and reduces the overhead caused by thread blocking.
2. Concurrent Tracing GC (Concurrent Tracing GC): implements garbage collection and program execution concurrent operation to minimize program pause time.
3. Distributed Marking: Complete object survival marking in parallel in a multi-core system.
4. On-demand activation optimization: only load and activate modules when there is actual demand to avoid redundant resource usage.

|Levels |Optimization Technology |Main Benefits |
|--|--|--|
|Compilation-time optimization |CHIR, backend SLP, etc. |Reduce CPU running cycle and improve peak performance |
|Runtime Optimization |GC, lock optimization, module activation, etc. |Reduce latency and improve system responsiveness |

## Cangjie runtime architecture: modular, lightweight, elastic expansion
Cangjie Runtime is committed to achieving extreme lightweight in architectural design, especially optimized for the needs of HarmonyOS Next in multi-device and resource-sensitive scenarios.
### Core features
|Properties | Description |
|--|--|
|Modular layered design | Separate kernel components from high-level functional modules, and can be streamlined according to actual needs |
|Public Object Model (POM) | Unified memory management, exception handling and type system construction |
|Package loading on demand |Module loading only when it is actually used, reducing initial memory footprint |
|Lightweight memory management |Special optimizations are made for IoT devices and lightweight terminals |

### Example: On-demand module loading scenario
Suppose a device only needs basic UI components when it is started, and when the user enters augmented reality mode, the AR-related modules will be dynamically loaded.
1. This method makes the initial memory usage of the device extremely low.
2. There is no need to restart the device or switch processes when loading the module.
3. By loading and unloading modules on demand, the flexibility of the system is greatly improved.

Practical experience: In actual projects, the same set of Cangjie applications can achieve dynamic adaptation of resource occupation when they run on different devices such as flagship mobile phones, IoT small-screen devices, smart screens, etc., and the user experience is very smooth.

## Cangjie Development Tool Chain: Good Helper for Performance Tuning
In addition to the optimization of the language itself and runtime, Cangjie also provides a complete development tool chain to provide strong support for performance tuning:
|Tools |Functions |
|--|--|
|Static checking tools | Potential performance problems can be found during compilation (such as invalid loops, redundant branches, etc.) |
|Profiler |Can accurately capture the time-consuming situation of functions and the hot spots of memory allocation |
|Mock Tools | Can quickly build a lightweight test environment |
|Intelligent auxiliary tools (AI Code Completion) | Improve efficient programming experience |

### Performance Analyzer Sample Output
|Function name |Number of calls |Average time (ms) |
|--|--|--|
|processData|5000|0.2|
|renderUI|1000|0.5|
|fetchRemote|300|1.2|

Practical experience: When positioning performance bottlenecks, Cangjie tool chain combines the performance characteristics of the language itself, greatly shortens the performance tuning cycle, and truly achieves the development process, that is, the optimization process.

## Summary
Cangjie Language has built a first-class performance system in the HarmonyOS Next environment. From compiler to runtime, from syntax design to toolchain support, every detail revolves around improving the final application experience.
|Advantages |Cangjie's innovations |
|--|--|
|Compiled-time performance optimization |Combination of multi-level IR optimization with instruction optimization |
|Runtime performance optimization |Using technologies such as lightweight threading, concurrent GC and modular runtime |
|Development experience|Have rich tool chain and intelligent performance analysis functions|
|Flexible deployment across devices |Resource adaptation with dynamic module management |

In the HarmonyOS Next project practice I participated in, Cangjie's performance even surpassed the previous hybrid development solutions using C++/Kotlin, and truly achieved the goal of easy to get started, efficiently run and easy to maintain.In the future, with the continuous unlocking of more features, Cangjie will surely become the mainstream choice for terminal-edge-cloud collaborative application development.
