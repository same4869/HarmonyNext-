# HarmonyOS Actor model practical: from concurrent security to distributed scaling

> As a development veteran who struggled in the Hongmeng distributed system, the Actor model once confused me - until it was used to solve the distributed lock problem in the order system.This article combines practical experience and shares the core principles and implementation skills of the Actor model to help you avoid the pitfalls of concurrent programming.


## 1. Actor model core: message-driven concurrency philosophy

### 1.1 Shared memory vs Message driver (compare the essence)
| Dimensions | Shared Memory Model | Actor Model (Message Driven) |
|--------------|---------------------------|-----------------------------|  
| **Data security** | Need to manually add locks, which is prone to competition | Status isolation, naturally avoiding data competition |
| **Programming complexity** | Lock mechanism increases mental burden | Focus on messaging, clearer logic |
| **Distributed Scaling** | High cost of sharing memory across nodes | Message Queues naturally support distributed |

**Practical case**: Bank transfer scenario
- Shared memory: Need to lock the account balance, it may be deadlocked
- Actor model: Each account is an independent actor, and the transfer is passed through message and is lock-free.


## 2. Cangjie Actor Programming: Implementation of State Isolation

### 2.1 The core role of receiver func
```cj
actor Account {
private var balance: Int64 // Complete status isolation
    
    init(initial: Int64) {
        balance = initial
    }
    
// The core function for receiving messages
    receiver func transfer(amount: Int64, to: ActorRef<Account>) {
        if balance >= amount {
            balance -= amount
to.send(message: Deposit(amount: amount)) // Send a message to the target account
        }
    }
    
    receiver func deposit(amount: Int64) {
        balance += amount
    }
}

// Call method
let from = spawn(Account(initial: 1000))
let to = spawn(Account(initial: 500))
from.send(message: Transfer(amount: 200, to: to))
```  

**Key Features**:
- The status is managed by the actor itself, and external operations can only be operated through messages.
- `receiver func` ensures sequential processing of messages without the need for additional synchronization mechanisms


## 3. Distributed expansion: Smooth migration from stand-alone to cluster

### 3.1 Three core components of distributed actors
1. **Actor Registration Center**
- Maintain global Actor address mapping table
- Support cross-node Actor reference parsing

2. **Distributed Message Queue**
- Cross-node message delivery based on DDS
- Ensure order and reliability of messages

3. **Actor migration mechanism**
   ```cj
// Migrate the Actor on Node A to Node B
   actorMigrator.migrate(
       actorId: "orderActor",
       targetNode: "nodeB",
       state: actorStateSnapshot
   )
   ```  

### 3.2 Practical architecture: e-commerce order system
```  
┌─────────────┐    ┌─────────────┐    ┌─────────────┐  
│ Order Actor │────→│ Payment Actor │───→│ Inventory Actor │
│ (Node A) │ │ (Node B) │ │ (Node C) │
└─────────────┘    └─────────────┘    └─────────────┘  
        ↑                ↑                ↑  
        └────────────────┼────────────────┘  
                 ┌──────────────────────┐  
│ Distributed Message Queue (based on DDS) │
                 └──────────────────────┘  
```  

** Advantages**:
- When the order volume increases suddenly, the Actor node can be expanded dynamically
- Single Actor failure does not affect overall system operation


## 4. Guide to performance optimization and pit avoidance

### 4.1 Message processing optimization
- **Batch processing**: Merge small messages to reduce communication overhead
- **Async reply**: Avoid synchronous waiting blocking Actor

### 4.2 Common Traps
1. **Newstorm**:
- Control the frequency of message between actors to avoid flooding
2. **Status expansion**:
- Regularly clean the useless state of the Actor to prevent memory leaks
3. **Network Partition**:
   - 实现Actor断线重连机制，保证最终一致性  
