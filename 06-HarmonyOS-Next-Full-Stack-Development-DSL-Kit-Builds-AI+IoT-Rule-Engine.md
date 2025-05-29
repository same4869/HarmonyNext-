# HarmonyOS Next Full Stack Development: DSL Kit Builds AI+IoT Rule Engine
Under the HarmonyOS Next ecosystem, deep integration of AI and IoT has become an industry trend.In my actual project, I used the DSL Kit of Cangjie language to build an AI+IoT rule engine to realize device automation control and intelligent decision-making. The following is to share the specific development process based on practical experience.

## 1. Engine design
### (I) BNF syntax defines IoT triggering rules (Example: Temperature sensor → Air conditioning control)
The core of the rule engine is to describe the trigger logic between IoT devices through custom DSL.Using the BNF syntax of DSL Kit, we can quickly define rule syntax.Take the scenario of temperature sensor-linked air conditioning as an example:
```bnf
rule ::= "when" condition "then" action
condition ::= sensor " " operator " " value
action ::= device " " operation
sensor ::= "temperature_sensor" | "humidity_sensor"
device ::= "air_conditioner" | "fan"
operator ::= ">" | "<" | "=="
value ::= number
operation ::= "turn_on" | "turn_off" | "set_temperature"
```
With the above syntax definition, developers can easily write rules such as `when temperature_sensor > 30 then air_conditioner turn_on`.DSL Kit will automatically generate a syntax parser, converting rule text into executable code logic, greatly reducing development costs.

## 2. AI integration
### (I) Implementation of Agent DSL real-time adjustment of rule parameters
In order to make the rule engine intelligent decision-making capabilities, we introduced Agent DSL for dynamic parameters adjustment.For example, when the indoor personnel activity frequency is detected to be high, the air conditioner temperature setting value is automatically reduced.Define a `ClimateAgent`:
```cj
@agent class ClimateAgent {
    @prompt[pattern=OptimizeClimate] (
action: "Optimize air conditioning parameters according to environment and personnel conditions",
purpose: "Improving comfort and saving energy",
expectation: "Output adjusted air conditioner operation parameters"
    )
    func optimizeParams(sensorData: SensorData): ClimateParams {
// Calculate parameters based on data such as personnel activity frequency and temperature
        if (sensorData.personActivity > 50 && sensorData.temperature > 28) {
            return ClimateParams(temperature = 24, fanSpeed = "high");
        }
        return ClimateParams(temperature = 26, fanSpeed = "medium");
    }
}
```
In the rules engine, by calling the `optimizeParams` method of `ClimateAgent`, you can get the adjusted parameters in real time, realizing the upgrade from simple triggering rules to intelligent decision-making.

## 3. Compilation and optimization
### (I) Attribute syntax checking avoids runtime errors
The compile-time static optimization function of DSL Kit can effectively avoid runtime errors.Using attribute syntax checking, the legality of the rules can be verified.For example, in the rule of temperature setting, the value range is limited to 16 - 30:
```bnf
rule ::= "when" condition "then" action {
    checkTemperatureRange(action.temperature)
}
condition ::= sensor " " operator " " value
action ::= device " " operation | device " " "set_temperature" " " temperature
temperature ::= number {
    validate: number >= 16 && number <= 30
}
```
When the developer writes rules such as `when temperature_sensor > 30 then air_conditioner set_temperature 35`, the compiler will report an error during the compilation stage, prompting that the temperature setting value is out of range, intercepting the error in advance, and improving the stability of the rule engine.

The AI+IoT rules engine built through DSL Kit fully utilizes the advantages of HarmonyOS Next in cross-device collaboration and native AI development.From rule syntax definition to AI integration, to compilation and optimization, each link reflects the efficiency and flexibility of Cangjie language in domain-specific development, providing a reliable solution for the intelligent application development of IoT scenarios.
