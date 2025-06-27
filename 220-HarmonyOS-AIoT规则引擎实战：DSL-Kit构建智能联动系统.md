# HarmonyOS AIoT规则引擎实战：DSL Kit构建智能联动系统  

> As a developer who has struck a trap with DSL Kit in the Hongmeng IoT project, the air conditioner has automatically cooled in winter due to rule syntax errors.This article shares how to use the Cangjie language DSL Kit to build an intelligent rule engine to achieve a simple trigger from "temperature > 30 to turn on the air conditioner" to intelligent linkage of AI dynamic parameter adjustment.


## 1. Rule Engine Core: Practical Design of DSL Syntax

### 1.1 Minimalist definition of BNF syntax
Use DSL Kit to define the syntax of air conditioning linkage rules (40% simplified than the original solution):
```bnf
rule = "when" condition "then" action
condition = sensor operator value
action = device operation [param]

sensor = "temp_sensor" | "humidity_sensor"
device = "aircon" | "fan"
operator = ">" | "<" | "=="
operation = "on" | "off" | "set_temp"
param = number
```  

**Practical rules example**:
```text
When temp_sensor > 28 then aircon set_temp 24 // The temperature exceeds 28℃ and set to 24℃
When humidity_sensor < 30 then fan on // Moisture is lower than 30%
```  

### 1.2 Pits and solutions for syntax analysis
**Training case**: Unprocessed parameter type leads to rule error
```cj
// Correct parser implementation (the key is type verification)
func parseRule(ruleStr: String) -> Rule? {
    let parts = ruleStr.split(" ")
    if parts.size < 5 { return nil }
    
// Type verification (such as temperature value must be 16-30)
    if parts[4] is Number && parts[4].toInt() in 16..30 {
        return Rule(
            sensor: parts[1],
            operator: parts[2],
            value: parts[3].toInt(),
            device: parts[5],
            operation: parts[6],
            param: parts.size > 7 ? parts[7].toInt() : nil
        )
    }
    return nil
}
```  


## 2. AI integration: Dynamic tuning of Agent DSL

### 2.1 Implementation of intelligent parameter adjustment
Define climate agents (30% less code than the original plan):
```cj
@agent ClimateAgent {
// Intelligent temperature regulation logic (adjust according to personnel activities dynamics)
    func optimizeTemp(sensorData: SensorData) -> Int {
        let baseTemp = 26
        if sensorData.personCount > 3 {
return baseTemp - 2 // Reduce 2℃ when multiple people
        } else if sensorData.lightIntensity > 800 {
return baseTemp + 1 // Increase by 1℃ during strong light
        }
        return baseTemp
    }
}

// Called in the rules engine
let agent = spawn(ClimateAgent())
let targetTemp = agent.ask(optimizeTemp(sensorData))
```  

### 2.2 Optimization techniques for real-time linkage
**Practical Strategy**:
1. **Cached recent parameters**: Avoid frequent AI calculations
2. **Threshold anti-shake**: Adjustment will not be triggered when the temperature fluctuates ±1℃
3. **Time Strategy**: Automatically increase the temperature setting value at night

```cj
// Temperature adjustment with anti-shake
func adjustWithDebounce(current: Int, target: Int) {
if abs(current - target) > 1 { // Adjust if it exceeds 1℃
        setAirconTemp(target)
    }
}
```  


## 3. Compilation optimization: Early intercept rule errors

### 3.1 Testing of attribute syntax
Embed check logic in BNF (compile-intercept error):
```bnf
rule = "when" condition "then" action {
checkTempAction(action) // Check the temperature parameter range
}

action = "aircon" "set_temp" temp {
temp >= 16 && temp <= 30 // The temperature must be between 16-30
}
```  

**Error Example Intercept**:
```text
When temp_sensor > 30 then aircon set_temp 35 // Compile error: Temperature 35 is out of range
```  

### 3.2 Three-pronged approaches to performance optimization
1. **Rules precompilation**: Compile DSL rules into bytecode at startup
2. **Conditional Short Circuit**: Multi-conditional rules are sorted by hit rate
3. **Hot rule cache**: High frequency rule resident memory

```cj
// Rule precompilation example
let rules = compileRules([
    "when temp>28 then aircon set_temp 24",
    "when humidity<30 then fan on"
])
```  


## 4. Practical results and guide to avoid pits

### 4.1 Project implementation effect
- Improved development efficiency: The rule configuration time is shortened from 2 days to 4 hours
- Failure rate drops: 85% reduction in runtime rule errors
- Energy-saving effect: AI adjusts reference fixed rules to save energy by 12%

### 4.2 Pit avoidance list
1. **Parameter boundary**: All numerical parameters must define upper and lower limit verification
2. **Concurrency Control**: Add an execution queue when multiple rules are triggered
3. **Downgrade policy**: Automatically switch to basic rules when AI module fails
