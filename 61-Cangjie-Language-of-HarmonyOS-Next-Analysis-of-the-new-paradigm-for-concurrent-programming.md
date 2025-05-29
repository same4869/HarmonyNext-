# Cangjie Language of HarmonyOS Next: Analysis of the new paradigm for concurrent programming
In the development field of HarmonyOS Next, the concurrent programming paradigm of Cangjie language has brought new ideas and methods to developers.It not only solves many problems in traditional concurrent programming, but also provides powerful tools and features to make concurrent programming more efficient and safe.As a technician with rich practical experience in this field, I will combine my experience in the actual development process to deeply analyze the concurrent programming paradigm of Cangjie language.

## 1. Concurrency Model Basics
### (I) Cangjie language parallel/concurrent design concept
When designing concurrent models, Cangjie Language adheres to the concept of efficiency, safety and ease of use.It aims to provide developers with a simple and powerful way to write concurrent programs, avoiding common pitfalls in traditional concurrent programming, such as data race and deadlocks.Unlike other languages, Cangjie Language regards concurrency as a first-class citizen and provides native support from the language level, allowing developers to write concurrent code more naturally.

### (II) Comparison of the differences between traditional thread model (Java/Kotlin) and Cangjie
In traditional Java and Kotlin development, although the threading model is powerful, it is more complicated to use.Developers need to manually manage thread creation, destruction and synchronization, which often easily leads to various problems.For example, when accessing shared resources through multiple threads, lock mechanisms are needed to ensure data consistency, but improper use of locks may lead to performance bottlenecks and deadlocks.

Cangjie language adopts a more concise and safer way.It automatically handles many details in concurrent programming through built-in concurrent primitives and type systems.For example, in Cangjie language, the problem of data competition is effectively avoided because its Actor model communicates through message delivery rather than shared memory, thus fundamentally eliminating the risk of data competition.

Here is a simple example to compare:
In Java, it is possible to implement the operation of two threads on shared variables as follows:
```java
public class SharedVariableExample {
    private static int sharedVariable = 0;

    public static void main(String[] args) {
        Thread thread1 = new Thread(() -> {
            for (int i = 0; i < 1000; i++) {
                sharedVariable++;
            }
        });

        Thread thread2 = new Thread(() -> {
            for (int i = 0; i < 1000; i++) {
                sharedVariable--;
            }
        });

        thread1.start();
        thread2.start();

        try {
            thread1.join();
            thread2.join();
        } catch (InterruptedException e) {
            e.printStackTrace();
        }

        System.out.println("Final value of shared variable: " + sharedVariable);
    }
}
```
In this example, data inconsistency may occur due to the two threads accessing and modifying the shared variable `sharedVariable` at the same time.

In Cangjie language, using the Actor model can be implemented like this:
```cj
actor SharedVariableActor {
    instance var value: Int64 = 0;

    receiver func increment(): Unit {
        value += 1;
    }

    receiver func decrement(): Unit {
        value -= 1;
    }

    receiver func getValue(): Int64 {
        return value;
    }
}
```
Through the Actor model, different actors communicate through message delivery, avoiding the data competition problem caused by shared memory.

## 2. Visual tuning tool
### (I) Task scheduling statistics and Measure lane practical demonstration
In the development of Cangjie language, visual tuning tools are a very powerful function.Among them, the Measure lane provides statistical information for Task scheduling in different concurrency modes.For example, in a multi-threaded application, we can view the number of Running Tasks at different moments through the Measure lane.

For specific operations, you only need to select the corresponding concurrency mode in the Measure lane of the visualization tool, and then scatter to the corresponding time point to see the exact number of Running Tasks.This is very helpful for analyzing the performance bottlenecks of the system.For example, when we find that there are too many Running Tasks in a certain period of time, it may mean that the system resources are over-occupied and further optimization of task scheduling strategies is needed.

### (II) Pseudo-parallel problem positioning techniques (with performance comparison table)
In concurrent programming, pseudo-parallelism is a common problem.Pseudo-parallelism refers to tasks that appear to be executed in parallel on the surface, but in fact, it does not really take advantage of the advantages of multi-core processors, resulting in less obvious performance improvements.

With visual tuning tools, we can easily locate pseudo-parallel problems.For example, we can judge whether there is a pseudo-parallel problem by comparing performance indicators in different concurrency modes, such as task execution time, CPU utilization, etc.Here is a simple performance comparison table:
|Concurrent mode |Task execution time (ms) |CPU utilization (%) |Is there pseudo-parallelism |
|---|---|---|---|
|Mode A|1000|50|Yes|
|Mode B|500|80|No|

As can be seen from the table, the task execution time of mode A is long and the CPU utilization is low, and there is a very likely pseudo-parallel problem.By further analyzing the data provided by the visualization tool, we can find out the reasons for pseudo-parallelism, such as the dependencies between tasks being too complex, or the thread synchronization mechanism is unreasonable, etc., and carry out targeted optimization.

## 3. A preliminary study on the Actor model
### (I) `actor` keyword and message delivery sample code
In Cangjie language, the `actor` keyword is the key to implementing the Actor model.With the `actor` keyword, we can define an Actor type and define various receiver functions in it to process the received messages.

For example, here is a simple Actor example:
```cj
actor MessageReceiver {
    receiver func receiveMessage(message: String): Unit {
        print("Received message: \(message)");
    }
}
```
In this example, `MessageReceiver` is an Actor type that defines a receiver function `receiveMessage` to process received string messages.When an instance of `MessageReceiver` receives a message, the receiver function will be called and the received message will be printed.

### (II) Advantages of distributed and concurrent unified programming
An important advantage of the Cangjie language Actor model is that it implements distributed and concurrent unified programming.This means that developers can use the same programming method to write concurrent and distributed programs and then easily deploy them to distributed environments.

In traditional development, writing concurrent and distributed programs often requires different technologies and frameworks, which increases the complexity of development.In Cangjie language, through the Actor model, developers can focus on the implementation of business logic without paying too much attention to the underlying distributed details.For example, in a distributed system, actors on different nodes can communicate via messaging, just like in a local concurrent environment, which greatly simplifies the development process of distributed systems.

To sum up, the concurrent programming paradigm of Cangjie language has brought many advantages to the development of HarmonyOS Next.Through its unique design philosophy, powerful visual tuning tools and Actor models, developers can write concurrent programs more efficiently and safely.In the actual development process, we should make full use of these features, continuously optimize our code, and improve the performance and reliability of the system.
