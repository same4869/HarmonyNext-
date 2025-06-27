# HarmonyOS atomized service development practice: design password for lightweight applications

> As an old development expert who has participated in the implementation of Hongmeng atomization service, I still remember the torment of the packaging from 20MB to 8MB when the first service was launched.This lightweight application form has subverted the traditional APP ideas. Now we share the experience from breaking through pitfalls to landing to help you avoid detours.


## 1. Three major subversive characteristics of atomized services

### 1. Lightweight: "Just Walk" experience within 10MB
- **No installation advantage**: User can use it by pulling down a negative screen, and the actual startup speed is 3 times faster than traditional APP
- **Inclusion body optimization practice**:
  ```bash
# Resource compression command (example)
  harmony-build --compress-images --remove-unused-fonts
  ```  
- **Volume comparison**:
| Type | Traditional APP | Atomized Services |
  |------------|----------|------------|  
| Body size | 50MB+ | <10MB |
| Startup Time | 1.5s | 0.3s |

### 2. Cross-device: A set of codes runs all things
- **Elastic layout core**:
  ```ets
  @Component
  struct WeatherCard {
    build() {
      Column {
Text("Weather")
          .fontSize(if Device.screenType == .large { 24 } else { 20 })
// Different devices display different content
        if Device.abilityType == .wearable {
Text("Lite Data")
        } else {
Text("Detailed Weather Data")
        }
      }
    }
  }
  ```  
- ** Device adaptation tips**: Use relative units (vp) instead of absolute pixels first


## 2. Three ways to develop: components + data + trigger

### 1. Core component practice
#### (1) ServiceAbility: the heart of the background
```java
// Pedometer background service (key logic)
public class StepService extends ServiceAbility {
  private StepDetector detector;
  @Override
  public void onStart(Intent intent) {
    detector = new StepDetector(this);
    detector.registerListener(count -> {
// Notify card updates when data changes
      getAbilityManager().notifyChange(
        Uri.parse("dataability://com.pedometer/steps")
      );
    });
  }
}
```  

#### (2) DataAbility: Data Sharing Hub
```json
// Data permission configuration
{
  "dataAbility": {
    "uriPermissions": [
      {
        "uri": "dataability://com.weather/data",
        "permissions": ["read", "write"]
      }
    ]
  }
}
```  

#### (3) AbilitySlice: Lightweight interface
```javascript
// Card interface (JS UI)
@Entry
@Component
struct Card {
@State data: Weather = { temp: "25℃", status: "Xingle" }
  build() {
    Stack {
      Image("bg.png").width("100%")
      Column {
        Text(data.status).fontSize(20)
        Text(data.temp).fontSize(36)
      }.align(Alignment.Center)
    }.onInit(() => {
// Lazy loading of data
      DataAbility.request("dataability://weather/card")
        .then(d => this.data = d)
    })
  }
}
```  


## 3. Scenario Trigger: Let the service actively find people

### 1. Geo-fence trigger (smart travel case)
```java
// Try the bus card near the bus stop
GeoFenceAPI.addFence(
  new GeoFence(
    "bus_stop", 
    new Location(116.4, 39.9), 
50, // 50 meters radius
    FenceTrigger.ENTER
  ),
  (status) => {
    if (status == FenceStatus.TRIGGERED) {
// Push bus cards
      CardManager.pushCard(
        "bus_card", 
        "com.transport.bus"
      );
    }
  }
);
```  

### 2. Device linkage trigger (smart home scenario)
```java
// Home mode linkage
DeviceManager.addDeviceStateListener(
  DeviceType.SMART_LOCK,
  (deviceId, state) => {
    if (state == DeviceState.LOCKED) {
      // 触发离家服务
      AbilityHelper.startAbility(
        "com.home.away_mode",
        new Intent().putParam("action", "leave")
      );
    }
  }
);
```  


## 四、性能优化的五个必杀技  

1. **Resource Lazy Loading**:
Lazy loading using `LazyForEach` for non-first screen resources

2. **Inclusion Body Compression**:
- Picture to WebP (30% volume reduction)
- Remove unused fonts (reduce 2MB in actual measurement)

3. **Start Optimization**:
   ```java
// Pre-rendered card (background rendering in advance)
   CardPreloader.preload(
     "weather_card", 
     new CardConfig().setPriority(1)
   );
   ```  

4. **Data Cache**:
Commonly used data local cache to reduce network requests

5. **Code obfuscation**:
Compile with the `--obfuscate` parameter, and the code volume is reduced by 15% again


## 5. Pit avoidance guide: From stepping on a pit to filling a pit

1. **Card update frequency**:
Dynamic card update interval is recommended to ≥30 seconds to avoid power consumption problems

2. **Span-device adaptation**:
The interface of the watch needs to be simplified, and the button size is ≥48px to ensure click experience

3. **Authority Application**:
Sensitive permissions (such as location) must be declared in `config.json` and clear instructions for use

4. **Grayscale Release**:
First increase the volume by 10% of users, monitor the Crash rate <0.1% and then the full volume

