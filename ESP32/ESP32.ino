#include <WiFi.h>
#include <PubSubClient.h>

char msg[25]="";
long count =0;
char temperatura[6]="";
char air[6]="";
char humedad[6]="";

//*********  WIFI CONFIG ***********
char* ssid = "Claro_TORRES0014683573";
char* password = "ITSMEN55604582387457";

//**********  MQTT CONFIG ************
const char* mqtt_server = "ioticos.org";
#define mqtt_port 1883
#define MQTT_USER "o6kn8eIMmK53Yxt"
#define MQTT_PASSWORD "31823SKRAXgFxf5"
#define ROOT_TOPIC_SUBSCRIBE "lKlhsHxr6zKCwBr/input"
#define ROOT_TOPIC_PUBLISH_TEMP "lKlhsHxr6zKCwBr/temperatura"
#define ROOT_TOPIC_PUBLISH_AIR "lKlhsHxr6zKCwBr/Calidad_aire"
#define ROOT_TOPIC_PUBLISH "lKlhsHxr6zKCwBr/humedad"

WiFiClient wifiClient;

PubSubClient client(wifiClient);

//******* SETUP WIFI *****************
void setup_wifi() {
    delay(10);
    // We start by connecting to a WiFi network
    Serial.println();
    Serial.print("Connecting to ");
    Serial.println(ssid);
    WiFi.begin(ssid, password);
    while (WiFi.status() != WL_CONNECTED) {
      delay(500);
      Serial.print(".");
    }
    randomSeed(micros());
    Serial.println("");
    Serial.println("WiFi connected");
    Serial.println("IP address: ");
    Serial.println(WiFi.localIP());
}

void reconnect() {
  // Loop until we're reconnected
  while (!client.connected()) {
    Serial.print("Attempting MQTT connection...");
    // Create a random client ID
    String clientId = "Client";
    clientId += String(random(0xffff),HEX);
    // try to reconect
    if (client.connect(clientId.c_str(),MQTT_USER,MQTT_PASSWORD)) {
      Serial.println("connected");
    if(client.subscribe(ROOT_TOPIC_SUBSCRIBE)){
      Serial.println("Subscribed OK");
      }else{
        Serial.println("failed subscription");
        }
    } else {
      Serial.print("failed, rc=");
      Serial.print(client.state());
      Serial.println(" try again in 5 seconds");
      // Wait 5 seconds before retrying
      delay(5000);
    }
  }
}

// ***** CALLBACK *****
void callback(char* topic, byte *payload, unsigned int length) {
    Serial.println("-------new message from broker-----");
    Serial.print("channel:");
    Serial.println(topic);
    Serial.print("data:");  
    Serial.write(payload, length);
    Serial.println();
}
/*
void publishSerialData(char *serialData){
  if (!client.connected()) {
    reconnect();
  }
  client.publish(MQTT_SERIAL_PUBLISH_CH, serialData);
*/
void setup() {
  Serial.begin(115200);
  Serial.setTimeout(500);// Set time out for 
  setup_wifi();
  client.setServer(mqtt_server, mqtt_port);
  client.setCallback(callback);
}


void loop() {
  if (!client.connected()) {
    reconnect();
  }
   if(client.connected()){  
      float a=random(4000,6000);
      a=a/100;
     String sensor_hum= String(a,2);
    //Serial.println(sensor_hum);
    sensor_hum.toCharArray(humedad,6);
    client.publish(ROOT_TOPIC_PUBLISH,humedad);
    //Serial.println(sensor_hum);
    
   delay(500);
    float b =random(1200,2300);
    b=b/100;
    String sensor_temp= String(b,2);
    sensor_temp.toCharArray(temperatura,6);
    client.publish(ROOT_TOPIC_PUBLISH_TEMP,temperatura);
    delay(500);

    float c=random(0,5000);
    c=c/100;
    String sensor_air= String(c,2);
    sensor_air.toCharArray(air,6);
    client.publish(ROOT_TOPIC_PUBLISH_AIR,air);
    delay(500);    
    }
   client.loop();
   }
 
