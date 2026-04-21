#include <Servo.h>

Servo catraca;
int pinoVerde = 12;
int pinoVermelho = 13;

void setup() {
  Serial.begin(9600);
  catraca.attach(9);
  pinMode(pinoVerde, OUTPUT);
  pinMode(pinoVermelho, OUTPUT);
  
  // Estado inicial: Catraca fechada (0 graus) e LED Vermelho aceso
  catraca.write(0); 
  digitalWrite(pinoVermelho, HIGH);
  digitalWrite(pinoVerde, LOW);
}

void loop() {
  if (Serial.available() > 0) {
    char comando = Serial.read();
    
    if (comando == '1') { // COMANDO PARA LIBERAR
      digitalWrite(pinoVermelho, LOW);
      digitalWrite(pinoVerde, HIGH);
      catraca.write(90); // Abre a catraca
      delay(5000);       // Mantém aberta por 5 segundos
      catraca.write(0);  // Fecha
      digitalWrite(pinoVerde, LOW);
      digitalWrite(pinoVermelho, HIGH);
    } 
    else if (comando == '0') { // COMANDO PARA NEGAR
      // Pisca o vermelho 3 vezes
      for(int i=0; i<3; i++){
        digitalWrite(pinoVermelho, LOW);
        delay(200);
        digitalWrite(pinoVermelho, HIGH);
        delay(200);
      }
    }
  }
}