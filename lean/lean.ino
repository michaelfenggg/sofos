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

//pin constants
const int greenLed = 3;
const int redLed = 4;
const int trigPin = 5;
const int echoPin = 2;

MFRC522 mfrc522(SS_PIN, RST_PIN);   // Create MFRC522 instance.

//wifi info
char ssid[] = "Michael's iPhone";
char pass[] = "pogpog21";

//initialing vars
long duration;
int distance;
int initDist; 
int time = 0;
bool started = false;
const int threshold = 50;

void setup() {
  Serial.begin(9600);   // Initiate a serial communication
  Serial.println("Setting up");
  pinMode(greenLed, OUTPUT);
  pinMode(redLed, OUTPUT);
  pinMode(trigPin, OUTPUT); // Sets the trigPin as an Output
  pinMode(echoPin, INPUT); // Sets the echoPin as an Input
  SPI.begin();      // Initiate  SPI bus
  mfrc522.PCD_Init();   // Initiate MFRC522
  //Blynk.begin(BLYNK_AUTH_TOKEN, ssid, pass);
  //Blynk.virtualWrite(V0, "rfid number");
}

void loop() {
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
  String content= "";
  for (byte i = 0; i < mfrc522.uid.size; i++) {
    Serial.print(mfrc522.uid.uidByte[i] < 0x10 ? " 0" : " ");
    Serial.print(mfrc522.uid.uidByte[i], HEX);
    content.concat(String(mfrc522.uid.uidByte[i] < 0x10 ? " 0" : " "));
    content.concat(String(mfrc522.uid.uidByte[i], HEX));
  }
  Serial.println();
  Serial.print("Message : ");
  content.toUpperCase();
  //Blynk.virtualWrite(V0, content);
  if (content.substring(1) == "22 04 9F 22") {
    handWash();
  }
}

int calcDist() {
  // Clears the trigPin
  digitalWrite(trigPin, LOW);
  delayMicroseconds(2);
  // Sets the trigPin on HIGH state for 10 micro seconds
  digitalWrite(trigPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin, LOW);
  // Reads the echoPin, returns the sound wave travel time in microseconds
  duration = pulseIn(echoPin, HIGH);
  // Calculating the distance
  distance = duration / 74 / 2;
  // Prints the distance on the Serial Monitor
  Serial.print("Distance (cm): ");
  Serial.println(distance);
  return distance;
}

void handWash() {
  //Show UID on serial monitor
  Serial.println("Welcome Michael! Start washing hands");
  while (calcDist() > threshold) {
    continue;
  };
  startTimer();
  Serial.println("You've started washing your hands!");
  time = 0;
  if (started) {
    digitalWrite(greenLed, HIGH);
    if (calcDist() > threshold) {
      Serial.println("Keep washing your hands!");
      started = false;
      digitalWrite(greenLed, LOW);
      digitalWrite(redLed, HIGH);
      //blinkRed();
      delay(50000);
    } else {
      delay(1000);
      time++;
      calcDist();
      Serial.println(time);
      digitalWrite(redLed, LOW);
      while (calcDist() < threshold) {
        cont();
      }
      Serial.println("You didn't wash your hands for 20 sec!");
      started = false;
      digitalWrite(greenLed, LOW);
      digitalWrite(redLed, HIGH);
      //blinkRed();
      delay(50000);
    }
  } else {
    digitalWrite(greenLed, LOW);
  }
}

void cont() {
  delay(1000);
  time++;
  Serial.println(time);
}

void startTimer() {
  started = true;
}

void blinkRed() {
  for (int i = 0; i < 3; i++) {
    digitalWrite(redLed, HIGH);
    delay(100);
    digitalWrite(redLed, LOW);
    delay(100);
  }
}


