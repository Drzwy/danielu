// Código Arduino para leer datos de un sensor analógico y enviarlos por el puerto serie

const int sensorPin = A0;

void setup() {
  Serial.begin(115200);  // Configura la velocidad de la conexión serial
}

void loop() {
  int sensorValue = analogRead(sensorPin);
  Serial.println(sensorValue);  // Envía el valor del sensor por el puerto serie
  delay(1000);  // Puedes ajustar el tiempo de espera según sea necesario
}