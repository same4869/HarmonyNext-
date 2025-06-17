
# HarmonyOS Next atomic service development: Design and practice of lightweight applications

In the HarmonyOS Next ecosystem, **atomized service** is a lightweight application form and has become the core carrier for connecting users and services with the characteristics of "use and go without installation".It breaks the heaviness of traditional APPs and provides users with a more convenient way to obtain services through card interaction, cross-device deployment and scene-based triggering.This article will deeply analyze the development architecture, design principles and practical points of atomized services.


## 1. Core features and architectural design of atomized services
### 1. Lightweight and installation-free features
- **Size limit**: Single atomized service package is usually less than 10MB, supporting fast loading and second-level startup.
- **Operation Mechanism**: Built based on **AbilitySlice** lightweight components, no need for complete application lifecycle management, and resources are loaded on demand at startup.

### 2. Cross-device adaptation and elastic layout
- **Multi-terminal unified development**: Use the **ETS/JS UI framework to write code once, and automatically render different terminal interfaces through device capabilities adaptation (such as screen size, input method).
- **Elastic layout example** (ETS language):
  ```ets
  @Component
  struct ResponsiveCard {
    @Builder
    build() {
      Column() {
Text("Weather Service")
          .fontSize(20)
          .fontWeight(FontWeight.Bold)
if (DeviceInfo.screenWidth > 600) { // Adapt to tablet/large screen devices
          Row() {
Text("Temperature: 25℃").fontSize(18)
Text("Wind: Breeze").fontSize(18)
          }
} else { // Adapt to mobile phone/small screen device
Text("Temperature: 25℃ Breeze").fontSize(16)
          .lineLimit(1)
        }
      }
      .padding(16)
      .backgroundColor(Color.White)
      .cornerRadius(8)
    }
  }
  ```

### 3. Card-style interaction and dynamic updates
- **Service Card**: Supports **static cards** (fixed display information) and **dynamic cards** (refresh data in real time, such as countdown, weather changes).
- **Dynamic update implementation**: Get data regularly through **DataAbility** and notify UI refresh:
  ```java
// Backend service regularly updates data
  public class WeatherService extends Service {
    private Timer dataUpdateTimer;
    @Override
    public void onStart(Intent intent) {
      dataUpdateTimer = new Timer();
      dataUpdateTimer.schedule(new TimerTask() {
        @Override
        public void run() {
// Get the latest weather data
          WeatherData weatherData = WeatherApi.fetchData();
// Notify card update
          DataAbilityHelper helper = DataAbilityHelper.creator(this);
          helper.notifyChange(Uri.parse("dataability://com.example.weather/card_data"));
        }
}, 0, 30 * 1000); // Update every 30 seconds
    }
  }
  ```


## 2. Atomized service development process and key components
### 1. Development process overview
![Atomized Service Development Flowchart](https://example.com/atom-service-flow.png)
* (Note: Visual design and debugging are required through DevEco Studio)*

### 2. Core component analysis
#### (1) ServiceAbility: backend service carrier
- Responsible for business logic processing (such as network requests, data calculations), and supports long-term operation.
- **Example: Pedometer backend service**
  ```java
  public class StepService extends ServiceAbility {
    private StepDetector stepDetector;
    @Override
    public void onStart(Intent intent) {
      super.onStart(intent);
      stepDetector = new StepDetector(this);
      stepDetector.registerStepListener(new StepListener() {
        @Override
        public void onStepCountUpdated(int stepCount) {
// Save step data and notify card updates
          DataStorage.saveStepData(stepCount);
          getAbilityManager().notifyDataChange(Uri.parse("dataability://com.example.pedometer/card"));
        }
      });
    }
  }
  ```

#### (2) DataAbility: Data Sharing and Access
- Provides cross-service data access interface, supports local storage (such as Preferences, File) and distributed synchronization (via DDS).
- **Data access permission configuration** (config.json):
  ```json
  "dataAbility": {
    "name": "com.example.weather.DataAbility",
    "uriPermissions": [
      {
        "uri": "dataability://com.example.weather/card_data",
        "permissions": ["read", "write"]
      }
    ]
  }
  ```

#### (3) AbilitySlice: Lightweight interface vector
- Lighter than traditional activities, supports independent startup and cross-device migration.
- **Card-style interface design** (JS UI framework):
  ```javascript
  @Entry
  @Component
  struct WeatherCard {
@State weatherData: WeatherData = { temperature: "22℃", condition: "Xing" }
    
    build() {
      Stack() {
        Image($r("app.media.weather_bg"))
          .objectFit(ImageFit.Cover)
          .width("100%")
          .height(200)
        Column() {
          Text(this.weatherData.condition)
            .fontSize(24)
            .fontWeight(500)
          Text(this.weatherData.temperature)
            .fontSize(48)
            .fontWeight(700)
        }
        .alignContent(Alignment.Center)
      }
      .onInit(() => {
// Load data during initialization
        DataAbility.request(Uri.parse("dataability://com.example.weather/card_data"))
          .then((data) => this.weatherData = data as WeatherData);
      })
    }
  }
  ```


## 3. Scenario-based triggering and distribution strategies
### 1. System entry trigger
- **Negative One Screen/Service Center**: Users use swipe gesture to evoke the service center, search or subscribe to the atomized service card.
- **Intelligent recommendation**: The system automatically recommends related services (such as recommended subway schedules during commuting periods) based on user behavior (such as geographic location, usage habits).

### 2. Cross-application linkage trigger
- **Deep Link Deep Link**: Directly evoke a specific interface of atomized service through URL (for example, click "Check Logistics" on the e-commerce APP to jump to the logistics tracking service).
  ```java
// Handle Deep Link in the target service
  public class LogisticsAbility extends Ability {
    @Override
    public void onStart(Intent intent) {
      super.onStart(intent);
      Uri uri = intent.getUri();
      if (uri != null && uri.getPath() == "/track") {
        String orderId = uri.getParameter("orderId");
// Load the corresponding order logistics information
        loadLogisticsData(orderId);
      }
    }
  }
  ```

### 3. Device status trigger
- **Hardware incident response**: When the smartwatch detects an abnormal user's heart rate, it will automatically evoke the health consultation service card.
- **Scenario-based combination service**: Smart home devices linkage trigger the "Leave Home Mode" service, turn off electrical appliances with one click, start the security camera and push weather reminders.


## 4. Performance optimization and release points
### 1. Start performance optimization
- **Resource lazy loading**: Non-critical resources (such as high-definition pictures) are loaded asynchronously after being displayed on the interface.
- **Pre-rendering technology**: Pre-rendering of commonly used service cards in the background to shorten the first loading time.

### 2. Optimization of the size of the package
- **Resource compression**: Use WebP format pictures and delete unused font files.
- **Code obfuscation**: Compress JS/ETS code through DevEco Studio's ProGuard tool.

### 3. Publish and Distribution
- **Service market on the shelves**: Create "atomized service" type products in the HarmonyOS application market. When submitting for review, you must provide a preview of cards of different sizes.
- **Phasely released**: Grayscale release function gradually increases the volume, monitor user feedback and then go online.


## 5. Typical scenario practice: smart travel and life services
### 1. Smart travel: real-time bus service
- **Scenario**: When the user is near the bus stop, the negative screen will automatically display the arrival time of the last bus. Click the card to view the real-time track.
- **Technical Implementation**:
- Trigger service card display via Geofencing.
- Use DataAbility to get bus data in real time and update card dynamics.
- Click the card to jump to AbilitySlice to display the complete line information.

### 2. Life Service: Tracking of Fresh Food Delivery Orders
- **Scenario**: After the user places an order, the atomized service card displays the order status (sorting, delivery, delivered) in real time, and supports one-click contact with the rider.
- **Technical Implementation**:
- Backend ServiceAbility listens to order status change events.
- Synchronize multi-device order data through DDS (notifications can be received by mobile phones, tablets, and smart speakers).
- The card provides quick operation buttons (such as "reminder order" and "confirm receipt"), and directly calls the native API to complete the interaction.


## Summarize
Atomized services are the best practice of the concept of "service finding people" in the HarmonyOS Next ecosystem. It uses lightweight forms, scenario-based triggering and cross-device adaptability to lower the threshold for users to obtain services, and at the same time provides developers with a more flexible traffic entrance.By deeply understanding its architecture design and mastering component characteristics and performance optimization strategies, developers can build "on-demand and ready-to-use" services that are more in line with user needs, and open up new growth space in the Hongmeng ecosystem.In the future, with the deep integration of atomized services with AI and Internet of Things technology, their application scenarios will be further extended and become the core link connecting users and everything.
