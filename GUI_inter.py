
import tkinter as tk
from tkinter import DoubleVar, StringVar, ttk
import matplotlib as mtp
mtp.use('TkAgg')
from collections import deque 
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import time
import numpy as np
import threading
import paho.mqtt.client as mqttClient
import time
from datetime import datetime
from statistics import *
####################### CALLBACKS ########################################

def on_connect(client, userdata, flags, rc):
    
    if rc == 0:
 
        print("Connected to broker")
 
        global Connected                #Use global variable
        Connected = True                #Signal connection 
        
        #client.subscribe(root_topic)
        client.subscribe(topic_temperatura, qos=1)
        client.subscribe(topic_humedad, qos=1)
        client.subscribe(topic_air, qos=1)
    else:
 
        print("Connection failed")

############### ON MESSAGE CALLBACK #######################
def on_message(client, userdata, message):
    time.sleep(0.01)
    a=str(message.payload.decode("utf-8"))
    #time.sleep(2) 
    print("on mesage")
    #plot_data.plot(data)
    
def on_message_temperature(client, userdata, message):
    a=str(message.payload.decode("utf-8"))
    box_cur_temp.configure(text=a)
    print("temperatura =",str(message.payload.decode("utf-8")))   
    #data.addt(search_number_string(a))
    data.addt(float(a))
    plot_data_t.plot(data.axis_t,data.axis_tt)
    box_ave_temp.configure(text=promediarLista(data.axis_t))  


def on_message_humedad(client, userdata, message):
    b=str(message.payload.decode("utf-8"))
    box_cur_humd.configure(text=b)
    data.addh(float(b))
    plot_data_h.plot(data.axis_h,data.axis_th)
    time.sleep(2)
    print("humedad =",str(message.payload.decode("utf-8")))
    box_ave_humd.configure(text=promediarLista(data.axis_h)) 

def on_message_calidad(client, userdata, message):          
    c=str(message.payload.decode("utf-8")) 
    box_cur_air.configure(text=c)
    data.adda(float(c))
    plot_data_a.plot(data.axis_a,data.axis_ta)
    print("aire =",str(message.payload.decode("utf-8")))    
    box_ave_air.configure(text=promediarLista(data.axis_a)) 
    
def bytes_to_decimal(i,d):
    xx = i - 127
    dec = (-d if xx < 0 else d)/100
    return xx + dec    
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
    i=0
    while i<len(lista):
        sum=lista[i]+sum
        i+=1
    return float("{0:.2f}".format(sum / len(lista)))

def request_data_received():
    global window
    window.after_cancel(cancel_id)

# Request data from node
def request_data():
    global cancel_id
    global window
    cancel_id = window.after(5000, request_data)

def guardar(ind, data):
    i=10
    while i>0:
        data[i]=data[i-1]
        i
    return data
class DataPlot:
    def __init__(self, max_entries = 20):
        self.axis_t = deque(maxlen=max_entries)
        self.axis_h = deque(maxlen=max_entries)
        self.axis_a = deque(maxlen=max_entries)
        self.axis_tt = deque(maxlen=max_entries)
        self.axis_th = deque(maxlen=max_entries)
        self.axis_ta = deque(maxlen=max_entries)
        self.max_entries = max_entries
        #self.axis_t.append(0)
    def addt(self, t):
        self.axis_t.append(t)
        
        self.axis_t[0]=t
        #self.axis_tiempo.append('a')
        #self.axis_tiempo.append(len(self.axis_t)) 
        self.axis_tt.append(datetime.now().strftime('%H:%M:%S')) 
        
    def addh(self, h):
        self.axis_h.append(h)
        self.axis_th.append(datetime.now().strftime('%H:%M:%S')) 
        
    def adda(self, a):
        self.axis_a.append(a)
        self.axis_ta.append(datetime.now().strftime('%H:%M:%S')) 
        

        
        
class RealtimePlot:
    def __init__(self, axes,canvas,fig):
     
        self.axes = axes
        self.fig = fig
        self.canvas=canvas
        self.lineplot, = axes.plot([],[], "ro-")
    def plot(self, data,data1):
        self.axes.set_xticklabels(data1)
        self.axes.autoscale_view(True)
        self.axes.relim()
        self.lineplot.set_data(list(range(len(data))),data)
        
        #x_min=min(float(sub) for sub in data1) 
        #x_max=max(float(sub) for sub in data1)        
        #y_min=min(float(sub) for sub in data) 
        #y_max=max(float(sub) for sub in data)        
        #self.axes.set_xlim(x_min, x_max)
        #self.axes.set_ylim(y_min, y_max)
        self.fig.canvas.draw_idle()
        #self.canvas.draw_idle()
        #self.canvas.draw()

Connected = False   #global variable for the state of the connection

    

if __name__ == '__main__':
    temperatura=[]
            ################    PARAMETROS ############################
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

    #########################   WINDOWS #########################################
    window = tk.Tk() # initialise a window
    window.title("Monitoring IOT")
    window.geometry("1300x700+5+5")
    
    ######################## SETTING MQTT ################################
    client = mqttClient.Client("Python")               #create new instance
    client.username_pw_set(user, password=password)    #set username and password
    client.on_connect= on_connect 
    client.on_message=on_message                     #attach function to callback
    client.connect(broker_address, port=port)          #connect to broker

    ## SUBSCRIBING
    #client.on_message= on_message                      #attach function to callback
    client.message_callback_add(topic_temperatura, on_message_temperature)
    client.message_callback_add(topic_humedad, on_message_humedad)
    client.message_callback_add(topic_air, on_message_calidad)
    client.loop_start()
    ################### 
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
    box_cur_temp = tk.Label(window,text='', font=("Helvetica", 50, 'bold'))
    box_cur_temp.place(x=875,y=80)
    box_1_cur_humd = tk.Label(window,text="HUMEDAD ACTUAL",font=("Helvetica 9 bold"),width=25 ,height=3,bg="#008B8B")
    box_1_cur_humd.place(x=875,y=230)
    box_cur_humd = ttk.Label(window,text='', font=("Helvetica", 50, 'bold'))
    box_cur_humd.place(x=875,y=305)
    box_1_cur_air = tk.Label(window,text="CALIDAD DE AIRE ACTUAL",font=("Helvetica 9 bold"),width=25 ,height=3,bg="#008B8B")
    box_1_cur_air.place(x=875,y=455)
    box_cur_air = ttk.Label(window,text='', font=("Helvetica", 50, 'bold'))
    box_cur_air.place(x=875,y=530)
    ##################### AVERAGE BOX############################
    box_1_ave_temp = tk.Label(window,text="TEMPERATURA PROMEDIO",font=("Helvetica 9 bold"),width=25 ,height=3,bg="#ADD8E6")
    box_1_ave_temp.place(x=1075,y=5)
    box_ave_temp = ttk.Label(window,text='', font=("Helvetica", 50, 'bold'))
    box_ave_temp.place(x=1075,y=80)
    box_1_ave_humd = tk.Label(window,text="HUMEDAD PROMEDIO",font=("Helvetica 9 bold"),width=25 ,height=3,bg="#ADD8E6")
    box_1_ave_humd.place(x=1075,y=230)
    box_ave_humd = ttk.Label(window,text='', font=("Helvetica", 50, 'bold'))
    box_ave_humd.place(x=1075,y=305)
    box_1_ave_air = tk.Label(window,text="CALIDAD AIRE PROMEDIO",font=("Helvetica 9 bold"),width=25 ,height=3,bg="#ADD8E6")
    box_1_ave_air.place(x=1075,y=455)
    box_ave_air = ttk.Label(window,text='', font=("Helvetica", 50, 'bold'))
    box_ave_air.place(x=1075,y=530)
    
    data = DataPlot()
    #dataploting=RealtimePlot(window)
    
    
    #dataPlotting= RealtimePlot(a1,canvas)
    fig = Figure(figsize=([6.2, 1.9]))
    a = fig.add_subplot(111)
    a.set_ylabel("°C", fontsize=8)
    a.set_ylim(10,25)
    canvas = FigureCanvasTkAgg(fig, master=window,)
    canvas.get_tk_widget().place(x=208,y=10)
    canvas.draw()
    plot_data_t=RealtimePlot(a,canvas,fig)
    
    fig1 = Figure(figsize=([6.2, 1.9]))
    b = fig1.add_subplot(111)
    b.plot([],[])
    b.set_ylabel("°%", fontsize=8)
    b.set_ylim(30,80)
    canvas1 = FigureCanvasTkAgg(fig1, master=window,)
    canvas1.get_tk_widget().place(x=208,y=235)
    canvas1.draw()
    plot_data_h=RealtimePlot(b,canvas1,fig1)

    fig2 = Figure(figsize=([6.2, 1.9]))
    c = fig2.add_subplot(111)
    b.plot([],[])
    c.set_ylabel("°% Air", fontsize=8)
    c.set_ylim(0,60)
    canvas2 = FigureCanvasTkAgg(fig2, master=window,)
    canvas2.get_tk_widget().place(x=208,y=465)
    canvas2.draw() 
    plot_data_a=RealtimePlot(c,canvas2,fig2)
    
    cancel_id = None
    
    window.mainloop()
    '''
    while 1:
        window.update()
        time.sleep(0.01)
        client.loop()
        time.sleep(0.02)
        xdato=data.axis_t
        if count==5000:
            print(xdato)

        time.sleep(0.05)
        count=count+1
    '''        
