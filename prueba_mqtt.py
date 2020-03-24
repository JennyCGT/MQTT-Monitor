import paho.mqtt.client as paho
import time

broker= "ioticos.org"  #Broker address
port = 1883                         #Broker port
user = "o6kn8eIMmK53Yxt"                    #Connection username
password = "31823SKRAXgFxf5"            #Connection password
topic_temperatura ='lKlhsHxr6zKCwBr/temperatura'
topic_humedad ='lKlhsHxr6zKCwBr/humedad'
topic_air='lKlhsHxr6zKCwBr/Calidad_aire'
root_topic='lKlhsHxr6zKCwBr/#'
temperature =[]
humedad=[]
calidad_aire=[]

def on_message(client, userdata, message):
    time.sleep(1)
    print("received message =",str(message.payload.decode("utf-8")))
    a=str(message.payload.decode("utf-8"))
    if(topic_temperatura==message.topic):
        temperature.append(search_number_string(a))
        print(temperature)
    if topic_humedad==message.topic:
        humedad.append(search_number_string(a))
        print(humedad)
    if topic_air==message.topic:
        calidad_aire.append(search_number_string(a))
        print(calidad_aire)
    #print(type(message.topic))
    #print("temperatura",str(message.payload.decode("utf-8")))

def on_message_temperature(client, userdata, message):
    time.sleep(1)
    a=str(message.payload.decode("utf-8"))
    temperature.append(search_number_string(a))
    print("temperatura =",str(message.payload.decode("utf-8")))
    #print(temperature)

def on_message_humedad(client, userdata, message):
    time.sleep(1)
    b=str(message.payload.decode("utf-8"))
    humedad.append(search_number_string(b))
    print("humedad =",str(message.payload.decode("utf-8")))

def on_message_calidad(client, userdata, message):
    time.sleep(1)
    c=str(message.payload.decode("utf-8"))
    calidad_aire.append(search_number_string(c))
    print("aire =",str(message.payload.decode("utf-8")))
    
def search_number_string(string):
    index_list = []
    del index_list[:]
    for i, x in enumerate(string):
        if x.isdigit() == True:
            index_list.append(i)
    start = index_list[0]
    end = index_list[-1] + 1
    number = string[start:end]
    return number
############### ON CONNECT CALLBACK ######################
def on_connect(client, userdata, flags, rc):
 
    if rc == 0:
 
        print("Connected to broker")
 
        global Connected                #Use global variable
        Connected = True                #Signal connection 
 
    else:
 
        print("Connection failed")
 
Connected = False   #global variable for the state of the connection
 
################# SET BROKER ####################################

client = paho.Client("Python")               #create new instance
client.username_pw_set(user, password=password)    #set username and password
client.on_connect= on_connect                      #attach function to callback
client.on_message= on_message                      #attach function to callback
 
client.connect(broker, port=port)          #connect to broker

################# START LOOP ############################################ 
client.loop_start()        #start the loop
 
while Connected != True:    #Wait for connection
    time.sleep(0.1)
print("subscribe topics")
#client.subscribe(root_topic)
client.subscribe(topic_temperatura, qos=1)
client.subscribe(topic_humedad, qos=1)
client.subscribe(topic_air, qos=1)
client.message_callback_add(topic_temperatura, on_message_temperature)
client.message_callback_add(topic_humedad, on_message_humedad)
client.message_callback_add(topic_air, on_message_calidad)
try:
    while True:
        time.sleep(1)
 
except KeyboardInterrupt:
    print ("exiting")
    client.disconnect()
    client.loop_stop()

