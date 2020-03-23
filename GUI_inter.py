
import tkinter as tk
from tkinter import DoubleVar, StringVar, ttk
import matplotlib as mtp
mtp.use('TkAgg')
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import time
import numpy as np
import threading
import paho.mqtt.client as mqttClient
import time

mtp.rcParams['xtick.labelsize']=8
mtp.rcParams['ytick.labelsize']=8
broker_address= "ioticos.org"  #Broker address
port = 1883                         #Broker port
user = "o6kn8eIMmK53Yxt"                    #Connection username
password = "31823SKRAXgFxf5"            #Connection password
topic_temperatura ="lKlhsHxr6zKCwBr/temperatura"
topic_humedad ="lKlhsHxr6zKCwBr/humedad"
topic_air="lKlhsHxr6zKCwBr/Calidad_aire"
root_topic="lKlhsHxr6zKCwBr/#"
temperature=[]
humedad=[]
calidad_aire=[]
curr_temp= 0.0
curr_hum= 0.0
curr_air= 0.0

running = True

def update_running():
    global running
    running = False
    window.destroy()

def on_connect(client, userdata, flags, rc):
    
    if rc == 0:
 
        print("Connected to broker")
 
        global Connected                #Use global variable
        Connected = True                #Signal connection 
        
        client.subscribe(root_topic)
    else:
 
        print("Connection failed")
 
############### ON MESSAGE CALLBACK #######################
def on_message(client, userdata, message):
    time.sleep(1)
    a=str(message.payload.decode("utf-8"))
    if(topic_temperatura==message.topic):
        temperature.append(search_number_string(a))           
        window.setvar(name="E1", value = search_number_string(a)) 
        print(temperature)
    if topic_humedad==message.topic:
        humedad.append(search_number_string(a))
        print(humedad)
    if topic_air==message.topic:
        calidad_aire.append(search_number_string(a))
        print(calidad_aire)       
## temperaute
def on_message_temperature(client, userdata, message):
    #time.sleep(1)
    a=str(message.payload.decode("utf-8"))
    temperature.append(search_number_string(a))
    E1.set(search_number_string(a))
    numero=promediarLista(temperature)
    print("temperatura =",str(message.payload.decode("utf-8")))
    #print(temperature)
## Humidity
def on_message_humedad(client, userdata, message):
    #time.sleep(1)
    b=str(message.payload.decode("utf-8"))
    humedad.append(search_number_string(b))
    E2.set(search_number_string(b))
    print("humedad =",str(message.payload.decode("utf-8")))
## Air quality
def on_message_calidad(client, userdata, message):
    #time.sleep(1)
    c=str(message.payload.decode("utf-8"))
    calidad_aire.append(search_number_string(c))
    E3.set(search_number_string(c))
    print("aire =",str(message.payload.decode("utf-8")))
    

 ############### OBTENER NUMERO  Y PROMEDIO #################   

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

def promediarLista(lista):
    sum=0.0
    for i in lista:
        sum+=lista[i]
    return sum/float(len(lista))

def actualizar():
    global aux_actualizar
    while aux_actualizar == True:
        print("actualizar")
        E1.set(temperature(-1))
        time.sleep(2)

Connected = False   #global variable for the state of the connection

######################## SETTING MQTT ################################
client = mqttClient.Client("Python")               #create new instance
client.username_pw_set(user, password=password)    #set username and password
client.connect(broker_address, port=port)          #connect to broker
client.on_connect= on_connect                      #attach function to callback
client.connect(broker_address, port=port)          #connect to broker

## SUBSCRIBING
client.on_message= on_message                      #attach function to callback
client.loop_start()
#client.message_callback_add(topic_temperatura, on_message_temperature)
#client.message_callback_add(topic_humedad, on_message_humedad)
#client.message_callback_add(topic_air, on_message_calidad)

###########################    WINDOWS #############################


window = tk.Tk() # initialise a window
window.title("Monitoring IOT")
window.geometry("1300x700+5+5")
E1=DoubleVar()
E2=DoubleVar()
E3=DoubleVar()
E4=DoubleVar()
##################### GRAPH  BOX ############################
box_temp = tk.Label(window,width=90 ,height=13,bg="#ADD8E6")
box_temp.place(x=200,y=5)
box_humd = tk.Label(window,width=90 ,height=13,bg="#ADD8E6")
box_humd.place(x=200,y=230)
box_air = tk.Label(window,width=90 ,height=13,bg="#ADD8E6")
box_air.place(x=200,y=455)
##################### CURRENT  BOX ############################
box_1_cur_temp = tk.Label(window,text="TEMPERATURA ACTUAL",font=("Helvetica 9 bold"),width=25 ,height=3,bg="#008B8B")
box_1_cur_temp.place(x=875,y=5)
box_cur_temp = ttk.Label(window,textvariable=E1, font=("Helvetica", 50, 'bold'))
box_cur_temp.place(x=875,y=80)
box_1_cur_humd = tk.Label(window,text="HUMEDAD ACTUAL",font=("Helvetica 9 bold"),width=25 ,height=3,bg="#008B8B")
box_1_cur_humd.place(x=875,y=230)
box_cur_humd = ttk.Label(window,textvariable=E2, font=("Helvetica", 50, 'bold'))
box_cur_humd.place(x=875,y=305)
box_1_cur_air = tk.Label(window,text="CALIDAD DE AIRE ACTUAL",font=("Helvetica 9 bold"),width=25 ,height=3,bg="#008B8B")
box_1_cur_air.place(x=875,y=455)
box_cur_air = ttk.Label(window,textvariable=E3, font=("Helvetica", 50, 'bold'))
box_cur_air.place(x=875,y=530)
##################### CURRENT  BOX0 ############################
box_1_ave_temp = tk.Label(window,text="TEMPERATURA PROMEDIO",font=("Helvetica 9 bold"),width=25 ,height=3,bg="#ADD8E6")
box_1_ave_temp.place(x=1075,y=5)
box_ave_temp = ttk.Label(window,textvariable=E4, font=("Helvetica", 50, 'bold'))
box_ave_temp.place(x=1075,y=80)
box_1_ave_humd = tk.Label(window,text="HUMEDAD PROMEDIO",font=("Helvetica 9 bold"),width=25 ,height=3,bg="#ADD8E6")
box_1_ave_humd.place(x=1075,y=230)

box_ave_air = tk.Label(window,text="CALIDAD AIRE PROMEDIO",font=("Helvetica 9 bold"),width=25 ,height=3,bg="#ADD8E6")
box_ave_air.place(x=1075,y=455)

x=np.array ([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
v= np.array ([16,16.31925,17.6394,16.003,17.2861,17.3131,19.1259,18.9694,22.0003,22.81226])
p= np.array ([16.23697,     17.31653,     17.22094,     17.68631,     17.73641 ,    18.6368,
            19.32125,     19.31756 ,    21.20247  ,   22.41444   ,  22.11718  ,   22.12453])


fig = Figure(figsize=([6.2, 1.9]))
a = fig.add_subplot(111)
a.scatter(v,x,color='red')
a.plot(p, range(2 +max(x)),color='blue')
a.invert_yaxis()
a.set_ylabel("°C", fontsize=8)
canvas = FigureCanvasTkAgg(fig, master=window,)
canvas.get_tk_widget().place(x=208,y=10)
canvas.draw()

fig1 = Figure(figsize=([6.2, 1.9]))
b = fig1.add_subplot(111)
b.set_ylabel("°%", fontsize=8)
canvas1 = FigureCanvasTkAgg(fig1, master=window,)
canvas1.get_tk_widget().place(x=208,y=235)
canvas1.draw()

fig2 = Figure(figsize=([6.2, 1.9]))
c = fig2.add_subplot(111)
c.scatter(v,x,color='red')
c.plot(p, range(2 +max(x)),color='blue')
c.invert_yaxis()
c.set_ylabel("°% Air", fontsize=8)
canvas2 = FigureCanvasTkAgg(fig2, master=window,)
canvas2.get_tk_widget().place(x=208,y=465)
canvas2.draw()
aux_actualizar=True
hilo1 = threading.Thread(target=actualizar)
hilo1.start()
'''
while 1:
    if running:
        window.update()
        window.update_idletasks()
        client.loop()
        time.sleep(1)
'''    

try:
    while True:
        if running:
            window.update()
            window.update_idletasks()
            client.loop()
            time.sleep(1)
 
except KeyboardInterrupt:
    aux_actualizar=False
    print ("exiting")
    client.disconnect()
    client.loop_stop()
