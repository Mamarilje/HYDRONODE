#include <WiFi.h>
#include <HTTPClient.h>

const char* ssid = "hmm";
const char* password = "karil0329";

const char* serverUrl = "http://192.168.100.111:5000/sensor";

#define FLOW_SENSOR_PIN 18

volatile int pulseCount = 0;

void IRAM_ATTR pulseCounter()
{
    pulseCount++;
}

void setup()
{
    Serial.begin(115200);

    pinMode(FLOW_SENSOR_PIN, INPUT_PULLUP);

    attachInterrupt(
        digitalPinToInterrupt(FLOW_SENSOR_PIN),
        pulseCounter,
        FALLING
    );

    WiFi.begin(ssid, password);

    while (WiFi.status() != WL_CONNECTED)
    {
        delay(500);
        Serial.print(".");
    }

    Serial.println("\nWiFi Connected");
}

void loop()
{
    delay(3000);

    noInterrupts();
    int count = pulseCount;
    pulseCount = 0;
    interrupts();

    Serial.print("Pulses: ");
    Serial.println(count);

    if (WiFi.status() == WL_CONNECTED)
    {
        HTTPClient http;
        http.begin(serverUrl);
        http.addHeader("Content-Type", "application/json");

        String json =
"{\"flow_rate\":" + String(count) +
",\"pressure\":42" +
",\"vibration\":0.15}";

        int responseCode = http.POST(json);

        Serial.print("HTTP Response: ");
        Serial.println(responseCode);

        http.end();
    }
}