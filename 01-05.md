# Easily handle concurrency: Concurrency programming model of Cangjie language under HarmonyOS Next
In scenarios such as smart terminals, Internet of Things, edge computing, etc., concurrency capabilities have become a key element of modern application development.Especially in a new ecosystem of HarmonyOS Next, which emphasizes multi-device collaboration and real-time response, how to write secure and scalable concurrent programs in a simple and efficient way has become an important challenge for developers.

Fortunately, Cangjie has created an elegant and efficient model for concurrent programming, which significantly reduces the difficulty of development.As an engineer who has been involved in the HarmonyOS Next project for a long time, I will combine practical operations to take you into the depth of the power of Cangjie's concurrency model.

## Lightweight user-state threads: the basis of efficient concurrency
Cangjie Language abandons the heavyweight design of traditional system threads and adopts lightweight user-mode threads (User - Mode Threads), which have the following characteristics:
- **Extremely lightweight**: Each thread requires very few resources, much smaller than the system thread.
- **User state management**: The creation, scheduling and destruction of threads are controlled by Cangjie's runtime.
- **Shared memory space**: Data can be shared between threads for easy communication.
- **Compatible with traditional API**: The usage method is consistent with system threads, easy to get started.

### Why choose a user-state thread?
There are many problems with traditional system threads (such as Pthread):
- Creation and destruction cost a lot.
- Context switching is expensive when scheduling.
- There are limits on the number of threads, usually only a few thousand are created.

Cangjie's user-state threading has obvious advantages:
- Create only takes tens of bytes of memory and a few microseconds.
- Easily manage tens of thousands of threads on a stand-alone basis.
- Scheduling is completed at the language layer, fast and controllable.

### Example: Start multiple Cangjie threads
```
import runtime.thread

main() {
    for (let i in 0..10) {
        thread.start {
            println("Hello from thread ${i}")
        }
    }
}
```
The output is similar:
```
Hello from thread 0
Hello from thread 1
Hello from thread 2
...
```
- `thread.start` is used to start a new lightweight thread.
- Anonymous code block is the thread execution body.
- The writing experience is similar to ordinary function calls, which is simple and convenient.

## Concurrent Object Library: Thread Safety has never been easier
In traditional concurrent programming, data race and deadlock are difficult problems.Cangjie greatly reduces the burden on developers to handle concurrency through the built-in Concurrent Object Library. The specific mechanism is as follows:
- **Concurrent Object**: Internal methods automatically achieve thread safety, and developers do not need to manually add locks.
- **Lock-free/fine-grained lock**: Some core libraries adopt lock-free design, pursuing ultimate performance.
- **Consistent API Experience**: Concurrent calls and serial calls are written exactly the same.

### Example: Using thread-safe concurrent objects
```import runtime.concurrent

mut class Counter {
    private var count = 0

    public func inc(): Unit {
        count += 1
    }

    public func get(): Int {
        return count
    }
}

main() {
    let counter = concurrent(Counter())

    for (let i in 0..1000) {
        thread.start {
            counter.inc()
        }
    }

    sleep(1 * Duration.Second)
    println("Final count: ${counter.get()}")
}
```
- `concurrent(obj)` converts normal objects into thread-safe objects.
- There is no need to manually add locks when calling `inc()` in concurrently.
- `sleep` is used to ensure that all threads have completed execution.

Practical experience: In the past, when writing concurrent logic, you had to carefully manage locks. Now, with the help of the concurrent object library, you can perform concurrent operations almost without burden, greatly improving the development speed and code accuracy.

## Lock-free and fine-grained locks: protect the ultimate performance
Although the default concurrent object can meet most scenarios, the overhead of locks cannot be ignored in some scenarios with extremely high performance requirements (such as high-frequency trading, real-time sensor processing).To this end, Cangjie's concurrency library uses the **Lock-Free or Fine-grained Lock technology for some core structures (such as lock-free queues and CAS variables). Their respective advantages are as follows:
- **Lock-Free**: Avoid thread blocking and improve system throughput capabilities.
- **Fine-grained lock**: Reduce lock competition and improve the degree of concurrent processing.
- **Spinlock**: Suitable for scenes with high frequency operations in a short time.

### Practical Examples (from Cangjie Standard Library)
```import runtime.concurrent

let queue = concurrent.Queue()

thread.start {
    for (let i in 0..100) {
        queue.enqueue(i)
    }
}

thread.start {
    for (let i in 0..100) {
        if (queue.dequeue() != null) {
            println("Got item")
        }
    }
}
```
- Queue is implemented internally with lock-free algorithm, with excellent performance.
- Suitable for producers with high concurrency - consumer scenarios.

### A summary of the concurrency characteristics of Cangjie
|Properties |Description |Practical Meaning |
|--|--|--|
|User-state threads |Lightweight, efficient, support massive threads |Implement fast response and high concurrency processing |
|Concurrent object library | Automatic thread-safe encapsulation | Simplify development process and reduce code vulnerabilities |
|Lock-free/fine-grained lock optimization | Implement high-performance concurrent processing | Meet extreme performance requirements scenarios |

## Summary
Cangjie achieved an excellent balance in concurrent design:
- **Simple and easy to use**: Newbie can easily write the correct concurrent program.
- **Extreme Performance**: Advanced users can perform deep tuning to give full play to their hardware performance.
- **Safe and reliable**: Effectively avoids most common concurrency problems.

I personally admire Cangjie's design style that is concurrency friendly and has good control.This efficient concurrency capability is crucial when developing HarmonyOS Next multi-device collaborative applications.With the continuous enrichment of the ecosystem, I believe that Cangjie's concurrent programming capabilities will play a key role in more complex projects.
