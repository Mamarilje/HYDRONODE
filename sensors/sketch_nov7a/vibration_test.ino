#define S0 25
#define S1 26
#define S2 27
#define S3 14

#define SIG 34

void selectChannel(int channel) {
  digitalWrite(S0, channel & 1);
  digitalWrite(S1, (channel >> 1) & 1);
  digitalWrite(S2, (channel >> 2) & 1);
  digitalWrite(S3, (channel >> 3) & 1);
}

void setup() {
  Serial.begin(115200);

  pinMode(S0, OUTPUT);
  pinMode(S1, OUTPUT);
  pinMode(S2, OUTPUT);
  pinMode(S3, OUTPUT);
}

void loop() {

  selectChannel(0);  // Vibration sensor on C0
    
  int vibration = analogRead(SIG);

  Serial.print("Vibration: ");
  Serial.println(vibration);

  delay(500);
}