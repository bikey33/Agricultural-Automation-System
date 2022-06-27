
#include <ESP8266WiFi.h>
#include <FirebaseESP8266.h>
                          
#define FIREBASE_HOST "https://agricultural-automation-f4b41-default-rtdb.firebaseio.com"                     //Your Firebase Project URL goes here without "http:" , "\" and "/"
#define FIREBASE_AUTH "uFDYrXK8F8vrJ79KMgntCWATogwzmZKjuSFoUFed" //Your Firebase Database Secret goes here

#define WIFI_SSID "UNfamily"                                               //your WiFi SSID for which yout NodeMCU connects
#define WIFI_PASSWORD "*Tenis2057"                                      //Password of your wifi network 
 

// Declare the Firebase Data object in the global scope
FirebaseData firebaseData;
int ReadMotorStatus();
 void UploadMoistureData(int);
 int i;
 int msensor=A0;//analog sensor attached to A0 Pin of NodeMCU
 int moisture=0;
 int relay=D0;//Connect Relay pin to the D2 pin
 

// Declare global variable to store value
int val=0;
bool flag=0;

void setup() {

pinMode(msensor, INPUT);
pinMode(relay,OUTPUT);

  Serial.begin(115200);
  // Select the same baud rate if you want to see the datas on Serial Monitor

  Serial.println("Serial communication started\n\n");  
           
  WiFi.begin(WIFI_SSID, WIFI_PASSWORD);                                     //try to connect with wifi
  Serial.print("Connecting to");
  Serial.print(WIFI_SSID);


  
  while (WiFi.status() != WL_CONNECTED) {
    Serial.print(".");
    delay(500);
  }

  
  Serial.println();
  Serial.print("Connected to ");
  Serial.println(WIFI_SSID);
  Serial.print("IP Address is : ");
  Serial.println(WiFi.localIP());                                            //print local IP address
  Firebase.begin(FIREBASE_HOST, FIREBASE_AUTH);   // connect to firebase

  Firebase.reconnectWiFi(true);
  delay(1000);
}

void loop() {
Serial.println("The obtained sensor value is:");
moisture=analogRead(msensor);
UploadMoistureData(moisture);
i=ReadMotorStatus();
  if(i==1){
    //ValveOn()
    digitalWrite(relay,HIGH);
    Serial.println("The Valve is ON");
    }
    else{
      digitalWrite(relay,LOW);
      Serial.println("The Valve is OFF");
  }

 }
 int ReadMotorStatus(){
  // Firebase Error Handling And Reading Data From Specified Path ************************************************

if (Firebase.getInt(firebaseData, "/motor_status")) {                           // On successful Read operation, function returns 1  

    if (firebaseData.dataType() == "int") {                            // print read data if it is integer

      val = firebaseData.intData();
      Serial.println(val);
      return val;
      Serial.println("\n Change value at firebase console to see changes here."); 
      delay(10000);
      
    }

  } else {
    Serial.println(firebaseData.errorReason());
  }
  }
 void UploadMoistureData(int moisture){
 if (Firebase.setInt(firebaseData, "/moisture content", moisture)) { 
               Serial.println("Value Uploaded Successfully");
               Serial.print("Moisture = ");
               Serial.println(moisture);
               Serial.println("\n");
               delay(1000);

     }

else {        
    Serial.println(firebaseData.errorReason());
  }
    }
