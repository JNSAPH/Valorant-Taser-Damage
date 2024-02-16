#define RELAY_PIN 2
#define OTHER_RELAY_PIN 4

void setup() {
  Serial.begin(9600); // Initialize serial communication
  pinMode(RELAY_PIN, OUTPUT);
  pinMode(OTHER_RELAY_PIN, OUTPUT);
  digitalWrite(RELAY_PIN, HIGH);
  digitalWrite(OTHER_RELAY_PIN, HIGH);
}

void loop() {
  if (Serial.available() > 0) {
    char command = Serial.read(); // Read incoming command
    if (command == '1') {
      digitalWrite(RELAY_PIN, HIGH); // Turn relay ON
      digitalWrite(OTHER_RELAY_PIN, HIGH); // Turn relay ON
    } else if (command == '0') {
      digitalWrite(RELAY_PIN, LOW); // Turn relay OFF
      digitalWrite(OTHER_RELAY_PIN, LOW); // Turn relay OFF
    }
  }
}
