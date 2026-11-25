/*
========================================
4 FLOW + 4 PRESSURE + LEAK DETECTION
========================================

FLOW 1 = GPIO18
FLOW 2 = GPIO19
FLOW 3 = GPIO21
FLOW 4 = GPIO22

PRESSURE 1 = GPIO32
PRESSURE 2 = GPIO33
PRESSURE 3 = GPIO34
PRESSURE 4 = GPIO35

PUMP RELAY = GPIO23

Serial Commands:
ON  -> Pump ON
OFF -> Pump OFF
========================================
*/

#define FLOW1_PIN 18
#define FLOW2_PIN 19
#define FLOW3_PIN 21
#define FLOW4_PIN 22

#define PRESSURE1_PIN 32
#define PRESSURE2_PIN 33
#define PRESSURE3_PIN 34
#define PRESSURE4_PIN 35

#define PUMP_RELAY_PIN 23

volatile int pulseCount1 = 0;
volatile int pulseCount2 = 0;
volatile int pulseCount3 = 0;
volatile int pulseCount4 = 0;

unsigned long previousMillis = 0;
bool pumpState = false;

// Leak thresholds
const float FLOW_DIFF_THRESHOLD = 1.0;
const int PRESSURE_DROP_THRESHOLD = 300;

// Interrupts
void IRAM_ATTR pulseCounter1()
{
    pulseCount1++;
}

void IRAM_ATTR pulseCounter2()
{
    pulseCount2++;
}

void IRAM_ATTR pulseCounter3()
{
    pulseCount3++;
}

void IRAM_ATTR pulseCounter4()
{
    pulseCount4++;
}

void setup()
{
    Serial.begin(115200);

    pinMode(FLOW1_PIN, INPUT_PULLUP);
    pinMode(FLOW2_PIN, INPUT_PULLUP);
    pinMode(FLOW3_PIN, INPUT_PULLUP);
    pinMode(FLOW4_PIN, INPUT_PULLUP);

    pinMode(PUMP_RELAY_PIN, OUTPUT);

    // ACTIVE HIGH RELAY
    digitalWrite(PUMP_RELAY_PIN, LOW);

    attachInterrupt(
        digitalPinToInterrupt(FLOW1_PIN),
        pulseCounter1,
        FALLING);

    attachInterrupt(
        digitalPinToInterrupt(FLOW2_PIN),
        pulseCounter2,
        FALLING);

    attachInterrupt(
        digitalPinToInterrupt(FLOW3_PIN),
        pulseCounter3,
        FALLING);

    attachInterrupt(
        digitalPinToInterrupt(FLOW4_PIN),
        pulseCounter4,
        FALLING);

    Serial.println("=================================");
    Serial.println("Leak Detection System Started");
    Serial.println("Type ON or OFF in Serial Monitor");
    Serial.println("=================================");
}

void loop()
{
    // Manual Pump Control
    if (Serial.available())
    {
        String command = Serial.readStringUntil('\n');
        command.trim();
        command.toUpperCase();

        if (command == "ON")
        {
            digitalWrite(PUMP_RELAY_PIN, HIGH);
            pumpState = true;
            Serial.println("PUMP ON");
        }
        else if (command == "OFF")
        {
            digitalWrite(PUMP_RELAY_PIN, LOW);
            pumpState = false;
            Serial.println("PUMP OFF");
        }
    }

    if (millis() - previousMillis >= 1000)
    {
        previousMillis = millis();

        noInterrupts();

        int flow1Pulses = pulseCount1;
        int flow2Pulses = pulseCount2;
        int flow3Pulses = pulseCount3;
        int flow4Pulses = pulseCount4;

        pulseCount1 = 0;
        pulseCount2 = 0;
        pulseCount3 = 0;
        pulseCount4 = 0;

        interrupts();

        float flow1 = flow1Pulses / 7.5;
        float flow2 = flow2Pulses / 7.5;
        float flow3 = flow3Pulses / 7.5;
        float flow4 = flow4Pulses / 7.5;

        int pressure1 = analogRead(PRESSURE1_PIN);
        int pressure2 = analogRead(PRESSURE2_PIN);
        int pressure3 = analogRead(PRESSURE3_PIN);
        int pressure4 = analogRead(PRESSURE4_PIN);

        bool leakDetected = false;

        Serial.println();
        Serial.println("=================================");
        Serial.print("Pump: ");
        Serial.println(pumpState ? "ON" : "OFF");
        Serial.println("=================================");

        Serial.print("Flow1: ");
        Serial.print(flow1);
        Serial.print(" L/min | Pressure1: ");
        Serial.println(pressure1);

        Serial.print("Flow2: ");
        Serial.print(flow2);
        Serial.print(" L/min | Pressure2: ");
        Serial.println(pressure2);

        Serial.print("Flow3: ");
        Serial.print(flow3);
        Serial.print(" L/min | Pressure3: ");
        Serial.println(pressure3);

        Serial.print("Flow4: ");
        Serial.print(flow4);
        Serial.print(" L/min | Pressure4: ");
        Serial.println(pressure4);

        Serial.println("---------------------------------");
        Serial.println("Leak Analysis");
        Serial.println("---------------------------------");

        // Flow-based leak detection
        if ((flow1 - flow2) > FLOW_DIFF_THRESHOLD)
        {
            leakDetected = true;
            Serial.println("LEAK BETWEEN SENSOR 1 AND SENSOR 2");
        }

        if ((flow2 - flow3) > FLOW_DIFF_THRESHOLD)
        {
            leakDetected = true;
            Serial.println("LEAK BETWEEN SENSOR 2 AND SENSOR 3");
        }

        if ((flow3 - flow4) > FLOW_DIFF_THRESHOLD)
        {
            leakDetected = true;
            Serial.println("LEAK BETWEEN SENSOR 3 AND SENSOR 4");
        }

        // Pressure-based leak detection
        if ((pressure1 - pressure2) > PRESSURE_DROP_THRESHOLD)
        {
            leakDetected = true;
            Serial.println("PRESSURE DROP AFTER SENSOR 1");
        }

        if ((pressure2 - pressure3) > PRESSURE_DROP_THRESHOLD)
        {
            leakDetected = true;
            Serial.println("PRESSURE DROP AFTER SENSOR 2");
        }

        if ((pressure3 - pressure4) > PRESSURE_DROP_THRESHOLD)
        {
            leakDetected = true;
            Serial.println("PRESSURE DROP AFTER SENSOR 3");
        }

        if (leakDetected)
        {
            Serial.println();
            Serial.println("***** LEAK DETECTED *****");
        }
        else
        {
            Serial.println();
            Serial.println("NO LEAK DETECTED");
        }

        Serial.println("=================================");
    }
}