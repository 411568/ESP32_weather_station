#include <WiFi.h>
#include <WiFiMulti.h>


//WiFiMulti object
WiFiMulti wifiMulti;


//WiFi setup
const char* ssid     = "GONTWIFI_C6E8"; //SSID
const char* password = "0715128612"; //Wifi password

const char* host = "api.thingspeak.com";
String api_key = "KLK85AR8GUKN9HKU"; // API Key provied by thingspeak


void wifi_setup()
{
  Serial.begin(9600);

  //connect to wifi
  wifiMulti.addAP(ssid, password);
  Serial.println("Connecting Wifi...");
  if(wifiMulti.run() == WL_CONNECTED) 
  {
    Serial.println("");
    Serial.println("WiFi connected");
    Serial.println("IP address: ");
    Serial.println(WiFi.localIP());
  }
}


void send_data(float temp, float humidity, float pressure, float altitude, float light, int rain, float wind, int battery)
{
  Serial.begin(9600);

  //send data to thingspeak
  while (WiFi.status() != WL_CONNECTED)
  {
    Serial.println("IP address: ");
    Serial.println(WiFi.localIP());
  }

  // Use WiFiClient class to create TCP connections
  WiFiClient client;
  const int httpPort = 80;

  if (!client.connect(host, httpPort)) 
  {
    Serial.println("connection failed");
    return;
  }
  else
  {
    // add all the data to seperate fields
    String data_to_send = api_key;
    data_to_send += "&field1=";
    data_to_send += String(temp);

    data_to_send += "&field2=";
    data_to_send += String(humidity);

    data_to_send += "&field3=";
    data_to_send += String(pressure);

    data_to_send += "&field4=";
    data_to_send += String(altitude);

    data_to_send += "&field5=";
    data_to_send += String(light);

    data_to_send += "&field6=";
    data_to_send += String(rain);

    data_to_send += "&field7=";
    data_to_send += String(wind);

    data_to_send += "&field8=";
    data_to_send += String(battery);    

    data_to_send += "\r\n\r\n";

    client.print("POST /update HTTP/1.1\n");
    client.print("Host: api.thingspeak.com\n");
    client.print("Connection: close\n");
    client.print("X-THINGSPEAKAPIKEY: " + api_key + "\n");
    client.print("Content-Type: application/x-www-form-urlencoded\n");
    client.print("Content-Length: ");
    client.print(data_to_send.length());
    client.print("\n\n");
    client.print(data_to_send);

    delay(1000);
  }

  client.stop();
}