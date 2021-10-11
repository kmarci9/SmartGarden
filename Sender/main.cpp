#include <OneWire.h> 
#include <DallasTemperature.h>
#include <OneWire.h>
#include <SoftwareSerial.h>
#include "EBYTE.h"
#include <iostream>
#include <Smoothed.h>


#define ONE_WIRE_BUS 0

#define PIN_RX 5   //D5 on the board (Connect this to the EBYTE TX pin)
#define PIN_TX 4   //D6 on the board (connect this to the EBYTE RX pin)




#define PIN_M0 15    //D8 on the board (connect this to the EBYTE M0 pin)
#define PIN_M1 13    //D7 on the board (connect this to the EBYTE M1 pin)
#define PIN_AX 16   //D0 on the board (connect this to the EBYTE AUX pin)

Smoothed <float> tempSensor;
Smoothed <float> soilSensor;

OneWire oneWire(ONE_WIRE_BUS); 

DallasTemperature sensors(&oneWire);

int moisture;
float temperature;
int valmap;
int Chan;
String tobesent;

SoftwareSerial ESerial(PIN_RX, PIN_TX);

// create the transceiver object, passing in the serial and pins
EBYTE Transceiver(&ESerial, PIN_M0, PIN_M1, PIN_AX);

void setup(void) 
{

  // start serial port 
  Serial.begin(9600); 
  //Serial.println("Dallas Temperature IC Control Library Demo"); 
  // Start up the library 
  sensors.begin(); 

  ESerial.begin(9600);

  Serial.println("Starting Sender");

  // this init will set the pinModes for you
  Serial.println(Transceiver.init());

  // Serial.println(Transceiver.GetAirDataRate());
  // Serial.println(Transceiver.GetChannel());
  Transceiver.SetAddressH(0);
  Transceiver.SetAddressL(0);
  Chan = 6;
  Transceiver.SetChannel(Chan);
  // save the parameters to the unit,
  Transceiver.SaveParameters(PERMANENT);

  // you can print all parameters and is good for debugging
  // if your units will not communicate, print the parameters
  // for both sender and receiver and make sure air rates, channel
  // and address is the same
  Transceiver.PrintParameters();

  tempSensor.begin(SMOOTHED_EXPONENTIAL,10);
  soilSensor.begin(SMOOTHED_EXPONENTIAL,10);


      for (int i = 0; i < 10; i++) {
      Serial.print("****************  " ) + Serial.print(i) + Serial.println("  *********************");
      Serial.println();
      Serial.print(" Requesting temperatures..."); 
      sensors.requestTemperatures(); // Send the command to get temperature readings 
      Serial.println("DONE"); 
      /********************************************************************/
      Serial.print("Temperature is: ");
      temperature = sensors.getTempCByIndex(0);
      Serial.print(temperature); // Why "byIndex"?  
    // You can have more than one DS18B20 on the same bus.  
    // 0 refers to the first IC on the wire 

      moisture = analogRead(A0); // analog input  300 -->full in water 700 ->dry
      Serial.print(" Moisture: "); 
      Serial.println(moisture);

      soilSensor.add(moisture);
      tempSensor.add(temperature);
      delay(100);
      Serial.println("******************************************");
    }
    
    valmap = map(soilSensor.get(),290,710,100,0);

    Serial.print(" Moisture%: ");
    Serial.println(valmap);
    Serial.print("%");

    tobesent = "temperature=" + String(tempSensor.get()) + ":moisture=" + String(valmap) + ";";
    Serial.println(tobesent);




    for (size_t i = 0; i < tobesent.length(); i++)
    {
      byte b = (byte)tobesent[i];
      Transceiver.SendByte(b);
    }

    ESerial.flush();
    delay(5000);
    Serial.println("I'm awake, but I'm going into deep sleep mode for 10 min");
    ESP.deepSleep(30e6 * 2 * 10);


}


void loop(void)
{
    
}