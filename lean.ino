#include <SPI.h>
#include <MFRC522.h>
#include <Servo.h>
#include <WiFiNINA.h>
#include <BlynkSimpleWiFiNINA.h>

const int greenLed = 3;
const int redLed = 4;
const int trigPin = 5;
const int echoPin = 2;

long duration;
int distance;

int initDist; 

bool started = false;

const int threshold = 5;

void setup() {
  Serial.begin(9600);   // Initiate a serial communication
  Serial.println("Setting up");
  pinMode(greenLed, OUTPUT);
  pinMode(redLed, OUTPUT);
  pinMode(trigPin, OUTPUT); // Sets the trigPin as an Output
  pinMode(echoPin, INPUT); // Sets the echoPin as an Input
}

void loop() {
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
  delayMicroseconds(5000);

  if (distance <= threshold) {
    startTimer();
  };

  if (started) {
    digitalWrite(greenLed, HIGH);

    if (distance > threshold) {
      started = false;
      digitalWrite(greenLed, LOW);
      blinkRed();
    } else {
      digitalWrite(redLed, LOW);
    }
  } else {
    digitalWrite(greenLed, LOW);
  }
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


