#define BLYNK_TEMPLATE_ID "TMPL218Ty8Oq4"
#define BLYNK_TEMPLATE_NAME "rfid"
#define BLYNK_AUTH_TOKEN "QftorMWxl0LbMD91aep7DUraakIdR9i4"
#define SS_PIN 6
#define RST_PIN 7

#include <SPI.h>
#include <MFRC522.h>
#include <Servo.h>
#include <WiFiNINA.h>
#include <BlynkSimpleWiFiNINA.h>

//the time when the sensor outputs a low impulse
long unsigned int lowIn;         

//the amount of milliseconds the sensor has to be low 
//before we assume all motion has stopped
long unsigned int pause = 5000;  

bool lockLow = true;
bool takeLowTime; 
bool cardScanned = false; //checks if card has been scanned

//pin constants
const int greenLed = 3;
const int redLed = 4;
const int pirPin = 5;   

MFRC522 mfrc522(SS_PIN, RST_PIN);   // Create MFRC522 instance.

//wifi info
char ssid[] = "Ketterer IOT";
char pass[] = "theCl0ud";

//initialing vars
int time = 0;
bool started = false;
int start;

void setup() {
  Serial.begin(9600);   // Initiate a serial communication
  Serial.println("Setting up");
  pinMode(greenLed, OUTPUT);
  pinMode(redLed, OUTPUT);
  digitalWrite(pirPin, LOW);
  SPI.begin();      // Initiate  SPI bus
  mfrc522.PCD_Init();   // Initiate MFRC522
  //give the sensor some time to calibrate
  Serial.print("calibrating sensor ");
  for(int i = 0; i < 10; i++){
    Serial.print(".");
    delay(1000);
    }
  Serial.println(" done");
  Serial.println("SENSOR ACTIVE");
  delay(50);
  //Blynk.begin(BLYNK_AUTH_TOKEN, ssid, pass);
  //Blynk.virtualWrite(V0, "rfid number");
}

void loop() {
  if (! cardScanned) {
    Serial.println("Approximate your card to the reader...");
    // Look for new cards
    if (!mfrc522.PICC_IsNewCardPresent()) {
      delay(1000);
      return;
    }
    // Select one of the cards
    if (!mfrc522.PICC_ReadCardSerial()) {
      delay(1000);
      return;
    }
    cardScanned = true;
    Serial.println("card scanned!");
    handWash();
  }
  /*String content= "";
  for (byte i = 0; i < mfrc522.uid.size; i++) {
    //Serial.print(mfrc522.uid.uidByte[i] < 0x10 ? " 0" : " ");
    //Serial.print(mfrc522.uid.uidByte[i], HEX);
    content.concat(String(mfrc522.uid.uidByte[i] < 0x10 ? " 0" : " "));
    content.concat(String(mfrc522.uid.uidByte[i], HEX));
  }
  //Serial.println();
  content.toUpperCase();
  Serial.println("Welcome Michael! Start washing hands");*/
}

void handWash() {
  Serial.println("checking for motion...");
  if(digitalRead(pirPin) == HIGH){
    //digitalWrite(greenLed, HIGH);   //the led visualizes the sensors output pin state
    if(lockLow){  
      //makes sure we wait for a transition to LOW before any further output is made:
      lockLow = false;            
      Serial.println("---");
      Serial.print("motion detected at ");
      Serial.print(millis()/1000);
      start = millis()/1000;
      Serial.println(" sec"); 
      Serial.println("Youve started washing your hands!");
      delay(50);
      }         
      takeLowTime = true;
      handWash();
    }
  if(digitalRead(pirPin) == LOW){       
    //digitalWrite(greenLed, LOW);  //the led visualizes the sensors output pin state
    if(takeLowTime){
      lowIn = millis();          //save the time of the transition from high to LOW
      takeLowTime = false;       //make sure this is only done at the start of a LOW phase
    }
    //if the sensor is low for more than the given pause, 
    //we assume that no more motion is going to happen
    if(!lockLow && millis() - lowIn > pause){  
        //makes sure this block of code is only executed again after 
        //a new motion sequence has been detected
        lockLow = true;                        
        Serial.print("motion ended at ");      //output
        Serial.print((millis() - pause)/1000);
        Serial.println(" sec");
        Serial.print("Youve washed your hands for ");
        int time = (millis() - pause) / 1000 - start;
        Serial.print(time);
        Serial.println("sec");
        if (time >= 20) {
          Serial.println("Good job! You've washed your hands for 20 sec");
          digitalWrite(greenLed, HIGH);
          delay(5000);
          digitalWrite(greenLed, LOW);
        }
        else {
          Serial.println("You didn't wash your hands for 20 sec! Wash them again");
          digitalWrite(redLed, HIGH);
          delay(5000);
          digitalWrite(redLed, LOW);
        }
        delay(50);
        }
    }
    else {
      delay(1000);
      handWash();
    }
}



