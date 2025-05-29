# HarmonyOS Next Game Development: From Creativity to Online
> This article aims to deeply explore the technical details of Huawei HarmonyOS Next system in game development and summarize it based on actual development practices.
It is mainly used as a carrier of technology sharing and communication, and it is inevitable to miss mistakes. All colleagues are welcome to put forward valuable opinions and questions in order to make common progress.
This article is original content, and any form of reprinting must indicate the source and original author.

Game development is an adventure full of creativity and challenges. In the world of HarmonyOS Next, with the help of Cangjie language, this adventure becomes even more exciting.Next, let’s walk through the entire process from game creative conception to final launch.

## Game creativity and technology selection
### Game Creativity and Game Design
At the starting point of game development, creativity is the key.We envision an adventure game that combines strategy and action elements, where players play heroes in a fantasy world, need to explore mysterious maps, collect resources, fight monsters and solve puzzles.The game adopts an open map design, where players can explore freely, trigger various random events, and increase the fun and replayability of the game.The combat system combines real-time action and strategy elements. Players need to reasonably choose skills and tactics based on the characteristics of the monster and the battlefield environment.

### Technology selection and HarmonyOS Next Advantages
Faced with numerous game development technologies, we chose HarmonyOS Next and Cangjie languages, which bring unique advantages to game development.HarmonyOS Next's distributed capabilities allow games to achieve a seamless cross-device experience, where players can start the game on their phones and then continue on their tablet or smart screen without having to start over.The concise and efficient grammar and powerful type system of Cangjie language make the development process smoother and reduce errors.Moreover, Cangjie's rich libraries and tools, such as libraries for graphics rendering and integrated support for physics engines, provide strong support for game development.

## Game architecture construction and development
### Game Architecture Design
The game architecture is divided into multiple modules, including scene management, character interaction, resource management and combat systems.The scene management module is responsible for loading and rendering game maps, handling scene switching and dynamic elements.The character interaction module handles the interaction logic between players, NPCs, and monsters.The resource management module is responsible for managing various resources in the game, such as props, gold coins, etc.The combat system is the core of the game, dealing with combat logic, skill release and damage calculation.

Communication between modules is carried out through message delivery and event-driven methods to ensure smooth operation of the game.例如，当玩家在场景中触发战斗事件时，场景管理模块会向战斗系统发送消息，战斗系统启动战斗流程，并将战斗结果反馈给角色交互模块和资源管理模块。

### Concurrent programming and multi-threaded operation
In game development, multi-threading is crucial.For example, in terms of special effects rendering, we use the concurrent programming capabilities of Cangjie language to allocate special effects rendering tasks to multiple threads, improve rendering efficiency and make the game picture more gorgeous.Physical simulation can also be performed in independent threads to ensure that real-time calculation of physical effects does not affect the main thread of the game.

```cj
import threading

// Special effect rendering thread function
func renderEffect() {
// Special effect rendering logic
    while (true) {
// Update the special effects status
        updateEffect();
// Rendering effects
        render();
    }
}

// Start the special effect rendering thread
let effectThread = threading.Thread(target=renderEffect);
effectThread.start();
```

By rationally utilizing multi-threading, games can achieve a richer and smoother gaming experience while ensuring performance.

### Application of test framework
To ensure the quality of the game, we make full use of the Cangjie language testing framework.Unit testing is used to test the basic functions of each module, such as testing the role's movement logic, skill release effect, etc.Mocking tests are used to simulate some scenarios that are difficult to reproduce in actual testing environments, such as simulating network delays, special behaviors of monsters, etc.Benchmarks are used to evaluate the performance of the game, such as testing scene loading time, frame rate stability during combat, etc.

```cj
// Test the role movement function
func testCharacterMove() {
    let character = Character();
    character.move(10, 20);
    assert(character.x == 10 && character.y == 20);
}
```

Through comprehensive testing, we can timely discover and fix problems in the game, improving the stability and user experience of the game.

## Game online and optimized
### Online process and precautions
After the game development is completed, it enters the online stage.First, we need to register and submit in the HarmonyOS Next application market.Before submitting, you must ensure that the game complies with the standards and requirements of the application market, including content review, security testing, etc.At the same time, prepare the game's promotional materials, such as screenshots, videos and introduction copy, to attract players to download.

### Optimization and user experience improvement
After going online, based on player feedback and data analysis, we use debuggers and performance analysis tools to locate and optimize problems.If players report that the game is stuttering on some devices, we can use performance analysis tools to view the CPU, memory and GPU usage to find out the performance bottlenecks.For example, if we find that the rendering of a certain scene causes the CPU load to be too high, we can optimize the rendering algorithm to reduce unnecessary computation.

Through continuous optimization and improvement, our games can bring players a smoother and more interesting gaming experience on the HarmonyOS Next platform.I hope that during the game development process, everyone can also make full use of the advantages of HarmonyOS Next and Cangjie languages ​​to create more exciting games!
