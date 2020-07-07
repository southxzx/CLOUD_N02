#include <ESPDateTime.h>
#include <TimeElapsed.h>
#include <BearSSLHelpers.h>
#include <CertStoreBearSSL.h>
#include <ESP8266WiFi.h>
#include <ESP8266WiFiAP.h>
#include <ESP8266WiFiGeneric.h>
#include <ESP8266WiFiGratuitous.h>
#include <ESP8266WiFiMulti.h>
#include <ESP8266WiFiScan.h>
#include <ESP8266WiFiSTA.h>
#include <ESP8266WiFiType.h>
#include <WiFiClient.h>
#include <WiFiClientSecure.h>
#include <WiFiClientSecureAxTLS.h>
#include <WiFiClientSecureBearSSL.h>
#include <WiFiServer.h>
#include <WiFiServerSecure.h>
#include <WiFiServerSecureAxTLS.h>
#include <WiFiServerSecureBearSSL.h>
#include <WiFiUdp.h>
#include <DateTime.h>
#include <ESP8266wifi.h>
#include <FirebaseArduino.h>
#include <DHT.h>
#define FIREBASE_HOST "cloud-8b97d.firebaseio.com"
#define FIREBASE_AUTH "5HQCYRWXEifXjYTBiZBOFV2uD6iCSm3L2PhRPRDg"
#define WIFI_SSID "P11 DKTD"
#define WIFI_PASSWORD "spkt12345"
#define DHTPIN D4                                                           
#define DHTTYPE DHT11                                                   
DHT dht(DHTPIN, DHTTYPE);                                                     
void setup() {
  Serial.begin(9600);
  delay(1000);                
  WiFi.begin(WIFI_SSID, WIFI_PASSWORD);                                    
  Serial.print("Connecting to ");
  Serial.print(WIFI_SSID);
  while (WiFi.status() != WL_CONNECTED) {
    Serial.print(".");
    delay(500);
  }
  Serial.println();
  Serial.print("Connected to ");
  Serial.println(WIFI_SSID);
  Serial.print("IP Address is : ");
  Serial.println(WiFi.localIP());                                           
  Firebase.begin(FIREBASE_HOST, FIREBASE_AUTH);                              
  dht.begin();                                                              
}

void loop() { 
  float h = dht.readHumidity();                                              
  float t = dht.readTemperature();                                 
  if (isnan(h) || isnan(t)) {                                            
    Serial.println(F("Failed to read from DHT sensor!"));
    return;
  }
  else
  {
  Serial.print("Humidity: ");  Serial.print(h);
  String fireHumid = String(h) ;                                         
  Serial.print("Temperature: ");  Serial.println(t);
  String fireTemp = String(t) ;                                         
StaticJsonBuffer<50> jsonBuffer;
JsonObject& timeStampObject = jsonBuffer.createObject();
timeStampObject[".sv"] = "timestamp";
Firebase.push("/DHT11/Time", timeStampObject);
Firebase.pushString("/DHT11/Humidity", fireHumid);                                 
Firebase.pushString("/DHT11/Temperature", fireTemp); 
delay(2000);
  }

}
