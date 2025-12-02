#include<Wire.h>
#include<dht11.h>
#include<Adafruit_BMP280.h>
#include<Adafruit_LiquidCrystal.h>

#define RAIN_SENSOR A0
#define BMP_PIN A1
#define DHT11_PIN A2

dht11 DHT11;
Adafruit_BMP280 bmp;
Adafruit_LiquidCrystal lcd(0);

// time 
unsigned long lastSend = 0;
const usigned long interval = 60000;

void setup() {
  //Serial setup
  Serial.begin(115200);
  Serial.println("temperature,humidity,pressure,rain");

  //LCD setup
  lcd.begin(16, 2);
  lcd.print("Hello, World!");

  //raindrop sensor setup
  pinMode(RAIN_SENSOR, INPUT);
}

void loop() {
  unsigned long now = millis();
  
  if(now - lastSend >= interval){
    lastSend = now;

    int rainsensorValue = analogRead(RAIN_SENSOR);
    int chk = DHT11.read(); 
    
    //Print temperature
    Serial.print((float)DHT11.temperature, 2);
    Serial.print(',');
    
    //Print humidity
    Serial.print((float)DHT11.humidity, 2);
    Serial.print(',');

    //Print pressure
    Serial.print((float)bmp.readPressure()/100.0);
    serial.print(',');

    //Print raindrop
    if(rainsensorValue < 102){
      serial.print(0);
    }else{
      serial.print(1);
    }

    serial.println();
  }
  
}
