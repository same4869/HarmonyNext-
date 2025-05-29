# HarmonyOS Next Smart Home System Development Practical Battle
> This article aims to deeply explore the technical details of Huawei HarmonyOS Next system in the development of smart home systems and summarize them based on actual development practices.
It is mainly used as a carrier of technology sharing and communication, and it is inevitable to miss mistakes. All colleagues are welcome to put forward valuable opinions and questions in order to make common progress.
This article is original content, and any form of reprinting must indicate the source and original author.

Smart home systems are becoming more and more popular in current technological life. They are like a smart butler, making our lives more convenient and comfortable.Today, let’s use HarmonyOS Next and Cangjie language to create a smart home system and experience the charm brought by cutting-edge technology.

## Project requirements and technical selection
### Analysis of the functional requirements of smart home system
Before starting development, we must clarify what functions this smart home system needs to implement.The most basic thing is that you must be able to control various equipment at home, such as smart light bulbs, smart sockets, smart curtains, etc., which can be switched easily through mobile phones or other smart devices.Moreover, we also hope to monitor the status of the equipment in real time, such as the brightness of the light bulb, the power consumption of the socket, the opening and closing of the curtains, etc.In addition, it is best to set up some automated scenes, such as when you wake up in the morning, you will automatically turn on the curtains and light up the soft lights, and when you go home at night, you will automatically turn on the lights and air conditioners in the living room.

### Reasons for choosing Cangjie language and related tools
There are many technical solutions for developing smart home systems on the market, such as those based on Android or other traditional Internet of Things frameworks.But we chose HarmonyOS Next and Cangjie languages, which was carefully considered.HarmonyOS Next's distributed capabilities are simply too powerful, and it allows seamless collaboration between different devices, which is crucial for smart home systems.Cangjie Language has concise and efficient grammar, high development efficiency, and also provides many features for distributed scenarios.For example, its Actor model is particularly suitable for communication and collaborative work between devices.

Let’s take a look at the relevant tools of Cangjie language. The package manager cjpm can automatically manage project dependencies without us manually dealing with those cumbersome dependencies, avoiding the hassle of version conflicts.The debugger cjdb supports cross-language debugging and thread debugging. If you encounter problems during the development process, it can help us quickly locate and solve them.There is also a testing framework, including unit testing, Mocking testing and benchmark testing frameworks, which can ensure the quality of the code in all aspects.

## System Architecture Design
### Overall architecture overview
The overall architecture of the smart home system we designed is divided into device, cloud and user.The device side is various smart devices at home, which are responsible for collecting data and executing control instructions.The cloud is like a data hub, storing and processing data uploaded by the device, and can also make logical judgments based on user settings.The user side is our smart devices such as mobile phones or tablets. Through it, we can control the device and check the device status anytime, anywhere.

Data interaction is carried out between the device and the cloud and the user through the distributed communication mechanism of HarmonyOS Next.Such an architectural design can ensure the scalability and stability of the system, and it is also very convenient if you want to add new devices or functions in the future.

### Use Cangjie Language Actor model to realize inter-device communication
In this system, the Cangjie language Actor model plays a big role.Each smart device can be regarded as an Actor, and they communicate and work together through messaging.For example, when the smart light bulb actor receives a light-on command message from the user, it will perform the light-on operation, and then feed its status message back to the user and the cloud.

```cj
actor SmartBulb {
    private var isOn: Bool = false;

// Receive the light-on message
    func receiveTurnOnMessage() {
        isOn = true;
// Execute the light turn on operation, here can be the code that actually controls the hardware
print("Light bulb is on");
// Feedback status message
        sendStatusMessage();
    }

// Receive the light turn off message
    func receiveTurnOffMessage() {
        isOn = false;
// Perform the lights off operation
print("Light bulb is off");
        sendStatusMessage();
    }

// Send status message
    func sendStatusMessage() {
let status = if (isOn) "on" else "off";
// Here you can implement the logic of sending status messages to the cloud and the user side
print("Light bulb status: \(status)");
    }
}
```

In this way, communication between various devices becomes simple and orderly, greatly improving the reliability and maintainability of the system.

## Development implementation and optimization
### Use cjpm to manage project dependencies
During project development, we use cjpm to manage project dependencies.For example, our smart home system may use some third-party libraries, such as libraries for device communication, data processing, etc.By simply declaring dependencies in the project's configuration file, cjpm can automatically download and install these libraries for us, and handle the version relationship between them.

```json
{
    "dependencies": {
        "device-communication-lib": "^1.0.0",
        "data-processing-lib": "^2.0.0"
    }
}
```

In this way, we no longer have to worry about dependency issues, and we can focus more on the development of core functions.

### Use cjdb to debug multi-threaded concurrent code
Smart home systems involve many concurrent operations, such as reporting data at the same time by multiple devices and issuing multiple control instructions at the same time.During the development process, it is inevitable to encounter some multi-threaded concurrency problems, and cjdb comes in handy.

We can set breakpoints in the code to observe the variable values ​​and state changes of different threads during execution.For example, when multiple devices send data to the cloud at the same time, we can check the data transmission status of each thread through cjdb to see if there are any problems with data loss or conflict.In this way, we can quickly locate and solve the problems caused by multi-threaded concurrency and ensure the stability of the system.

### Use the test framework for functional and performance testing
In order to ensure the quality of the smart home system, we used the Cangjie language testing framework for comprehensive testing.The unit testing framework can conduct separate tests on each functional module, such as testing the control function of smart light bulbs, the power monitoring function of smart sockets, etc.

```cj
// Test the smart light bulb turn on function
func testSmartBulbTurnOn() {
    let bulb = SmartBulb();
    bulb.receiveTurnOnMessage();
    assert(bulb.isOn == true);
}
```

The Mocking test framework can simulate some external environments and dependencies, such as simulating the response of cloud servers and testing the response of devices under different circumstances.The benchmark testing framework can help us evaluate the performance of the system, such as the response time of the test equipment control instructions, the speed of data transmission, etc.Based on the test results, we can optimize the system in a targeted manner to improve the user experience.

Through the above development process, we have successfully created a smart home system based on HarmonyOS Next and Cangjie languages.I hope this article can provide you with some reference and help when developing similar projects. If you have any questions or experiences during the development process, please feel free to share them together!
