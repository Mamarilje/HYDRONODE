#define PUMP_PIN 27

void setup() {
  Serial.begin(115200);
  pinMode(PUMP_PIN, OUTPUT);
}

void loop() {
  if (Serial.available()) {
    String cmd = Serial.readStringUntil('\n');
    cmd.trim();

    Serial.print("Received: ");
    Serial.println(cmd);

    if (cmd == "ON") {
      digitalWrite(PUMP_PIN, HIGH);
      Serial.println("GPIO27 HIGH");
    }

    if (cmd == "OFF") {
      digitalWrite(PUMP_PIN, LOW);
      Serial.println("GPIO27 LOW");
    }
  }
}