#define VIBRATION_PIN 35

void setup()
{
    Serial.begin(115200);
}

void loop()
{
    int vibrationValue =
        analogRead(VIBRATION_PIN);

    Serial.print(
        "Vibration Raw: "
    );

    Serial.println(
        vibrationValue
    );

    delay(500);
}