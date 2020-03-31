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
import random 
Connected =False
####################### CALLBACKS ########################################

def conexion():
    global Connected  
    print(conectar.configure('text'))
    broker_address= host.get()  #Broker address
    port = port1.get()                    #Broker port
    user = user1.get()                    #Connection username
    password = passw.get()            #Connection password
    topic_temperatura =topic_t.get()
    topic_humedad = topic_h.get()
    topic_air=topic_a.get()
    print(type(conectar.configure('text')))
######################## SETTING MQTT ################################
    client = mqttClient.Client("Python"+str(random.randint(1,101)))               #create new instance
    client.username_pw_set(user, password=password)    #set username and password
    client.on_connect= on_connect 
    client.on_message=on_message                     #attach function to callback
    client.on_disconnect=on_disconnect
    if Connected!=True:
        client.connect(broker_address, port=int(port))          #connect to broker
        client.message_callback_add(topic_temperatura, on_message_temperature)
        client.message_callback_add(topic_humedad, on_message_humedad)
        client.message_callback_add(topic_air, on_message_calidad)
        client.loop_start()
        time.sleep(0.6)
        print(Connected)

    if conectar.configure('text')[4]== 'Conectar':
        Pagina_inicio.principal()
        #canvas = FigureCanvasTkAgg(fig, master=window,)
        canvas.get_tk_widget().place(x=10,y=10)
        canvas.draw()
        canvas1.get_tk_widget().place(x=10,y=10)
        canvas1.draw()
        canvas2.get_tk_widget().place(x=10,y=10)
        canvas2.draw()
        count=1
        if Connected==True and client.is_connected()==True:
            conectar.configure(text="Desconectar")
    else:
        conectar.configure(text="Conectar")
        tk.messagebox.showinfo("Conexion MQTT", "Desconexion") 

def conexion_inicio():
    print("INICIO")
    Pagina_inicio.principal()
    canvas.get_tk_widget().config(width=640, height=190)
    canvas1.get_tk_widget().config(width=640, height=190)
    canvas2.get_tk_widget().config(width=640, height=190)

def conexion_t():
    print("ABRIR TEMPERATURA")
    Pagina_inicio.pagina_temperatura()
    canvas.get_tk_widget().config(width=640, height=580)

def conexion_h():
    print("ABRIR TEMPERATURA")
    Pagina_inicio.pagina_humedad()
    canvas1.get_tk_widget().config(width=640, height=580)
def conexion_a():
    print("ABRIR TEMPERATURA")    
    Pagina_inicio.pagina_aire()
    canvas2.get_tk_widget().config(width=640, height=580)

def on_connect(client, userdata, flags, rc):
    
    if rc == 0:
        global Connected                #Use global variable
        client.connected_flag=True #set flag       
        Connected=client.connected_flag
        #client.subscribe(root_topic)
        client.subscribe(topic_temperatura, qos=1)
        client.subscribe(topic_humedad, qos=1)
        client.subscribe(topic_air, qos=1)
        print("conexion exitosa")
        tk.messagebox.showinfo("Conexion MQTT", "Conexion exitosa") 
    else:
        print("Connection failed")

def on_disconnect(client, userdata, rc):
    global Connected
    client.connected_flag=False
    client.disconnect_flag=True
    Connected=client.connected_flag
    #tk.messagebox.showinfo("Conexion MQTT", "Desconexion exitosa") 
    print("entre")
############### ON MESSAGE CALLBACK #######################
def on_message(client, userdata, message):
    time.sleep(0.01)
    a=str(message.payload.decode("utf-8"))
    #time.sleep(2) 
    print("on mesage")
    #plot_data.plot(data)
    
def on_message_temperature(client, userdata, message):
    a=str(message.payload.decode("utf-8"))
    Pagina_inicio.box_cur_temp.configure(text=a)
    print("temperatura =",str(message.payload.decode("utf-8")))   
    #data.addt(search_number_string(a))
    data.addt(float(a))
    plot_data_t.plot(data.axis_t,data.axis_tt)
    Pagina_inicio.box_ave_temp.configure(text=promediarLista(data.axis_t))  

def on_message_humedad(client, userdata, message):
    global Connected
    b=str(message.payload.decode("utf-8"))
    Pagina_inicio.box_cur_humd.configure(text=b)
    data.addh(float(b))
    plot_data_h.plot(data.axis_h,data.axis_th)
    time.sleep(2)
    print("humedad =",str(message.payload.decode("utf-8")))
    Pagina_inicio.box_ave_humd.configure(text=promediarLista(data.axis_h)) 
    if conectar.configure('text')[4]== 'Conectar':
        #client.loop_stop()
        client.disconnect()

def on_message_calidad(client, userdata, message):          
    c=str(message.payload.decode("utf-8")) 
    Pagina_inicio.box_cur_air.configure(text=c)
    data.adda(float(c))
    plot_data_a.plot(data.axis_a,data.axis_ta)
    print("aire =",str(message.payload.decode("utf-8")))    
    Pagina_inicio.box_ave_air.configure(text=promediarLista(data.axis_a))
        
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
    def __init__(self, max_entries = 30):
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
        #self.axis_tiempo.append('a')
        #self.axis_tiempo.append(len(self.axis_t)) 
        self.axis_tt.append(datetime.now().strftime('%H:%M:%S'))
        tim=datetime.now().strftime('%Y %m %d %H:%M:%S')
        Pagina_inicio.list_t.insert(tk.END,"    "+ tim+ "             "+str(round(t,2))) 
        Pagina_inicio.list_t.see(tk.END)
        
    def addh(self, h):
        self.axis_h.append(h)
        self.axis_th.append(datetime.now().strftime('%H:%M:%S')) 
        tim=datetime.now().strftime('%Y %m %d %H:%M:%S')
        Pagina_inicio.list_h.insert(tk.END,"    "+ tim+ "             "+str(round(h,2))) 
        Pagina_inicio.list_h.see(tk.END)
    def adda(self, a):
        self.axis_a.append(a)
        self.axis_ta.append(datetime.now().strftime('%H:%M:%S'))         
        tim=datetime.now().strftime('%Y %m %d %H:%M:%S')
        Pagina_inicio.list_a.insert(tk.END,"    "+ tim+ "             "+str(round(a,2))) 
        Pagina_inicio.list_a.see(tk.END)
        
class RealtimePlot:
    def __init__(self, axes,canvas,fig):
        self.axes = axes
        self.fig = fig
        self.canvas=canvas
        self.lineplot, = axes.plot([],[], "o-")
    def plot(self, data,data1):
        self.axes.set_xticklabels(data1)
        self.axes.autoscale_view(True)
        self.axes.relim()
        self.lineplot.set_data(list(range(len(data))),data)
        self.fig.canvas.draw_idle()

class Start_page():
    def __init__(self,window):
        self.window=window
        self.box_air = tk.Frame(self.window,width=660 ,height=215,bg="#ADD8E6")
        self.box_temp = tk.Frame(self.window,width=660 ,height=215,bg="#ADD8E6")    
        self.box_humd = tk.Frame(self.window,width=660 ,height=215,bg="#ADD8E6")
        ##################### CURRENT  BOX ####################
        self.box_cur_temp = tk.Label(self.window,text='', font=("Helvetica", 50, 'bold'))
        self.box_cur_humd = ttk.Label(self.window,text='', font=("Helvetica", 50, 'bold'))
        self.box_cur_air = ttk.Label(self.window,text='', font=("Helvetica", 50, 'bold'))
        ##################### AVERAGE BOX############################
        self.box_ave_temp = ttk.Label(self.window,text='', font=("Helvetica", 50, 'bold'))
        self.box_ave_humd = ttk.Label(self.window,text='', font=("Helvetica", 50, 'bold'))
        self.box_ave_air = ttk.Label(self.window,text='', font=("Helvetica", 50, 'bold'))
        ################# current title############################
        self.box_1_cur_temp = tk.Label(self.window,text="TEMPERATURA ACTUAL",font=("Helvetica 10 bold"),width=24,height=3,bg="#008B8B")
        self.box_1_cur_humd = tk.Label(self.window,text="HUMEDAD ACTUAL",font=("Helvetica 10 bold"),width=24,height=3,bg="#008B8B")
        self.box_1_cur_air = tk.Label(self.window,text="CALIDAD DE AIRE ACTUAL",font=("Helvetica 10 bold"),width=24 ,height=3,bg="#008B8B")
        ################# average title ###############################
        self.box_1_ave_temp = tk.Label(self.window,text="TEMPERATURA PROMEDIO",font=("Helvetica 10 bold"),width=24,height=3,bg="#ADD8E6")
        self.box_1_ave_humd = tk.Label(self.window,text="HUMEDAD PROMEDIO",font=("Helvetica 10 bold"),width=24,height=3,bg="#ADD8E6")
        self.box_1_ave_air = tk.Label(self.window,text="CALIDAD AIRE PROMEDIO",font=("Helvetica 10 bold"),width=24,height=3,bg="#ADD8E6")

        self.frame=tk.Frame(self.window,width=600, height=500,bg="#ADF8E6")
        self.list_t =tk.Listbox(self.frame,font=("Helvetica 10 "),width=45, height=25,)
        self.list_t.insert(0,"          FECHA                     TEMPERATURA")
        self.list_t.pack(side="left", fill="y")
        self.scroll_t = tk.Scrollbar(self.frame, orient="vertical")
        self.scroll_t.config(command=self.list_t.yview)
        self.scroll_t.pack(side="right", fill="y")

        self.frame1=tk.Frame(self.window,width=600, height=500,bg="#ADF8E6")
        self.list_h =tk.Listbox(self.frame1,font=("Helvetica 10 "),width=45, height=25,)
        self.list_h.insert(0,"          FECHA                     HUMEDAD")
        self.list_h.pack(side="left", fill="y")
        self.scroll_h = tk.Scrollbar(self.frame1, orient="vertical")
        self.scroll_h.config(command=self.list_h.yview)
        self.scroll_h.pack(side="right", fill="y")

        self.frame2=tk.Frame(self.window,width=600, height=500,bg="#ADF8E6")
        self.list_a =tk.Listbox(self.frame2,font=("Helvetica 10 "),width=45, height=25,)
        self.list_a.insert(0,"          FECHA                     CALIDAD AIRE")
        self.list_a.pack(side="left", fill="y")
        self.scroll_a = tk.Scrollbar(self.frame2, orient="vertical")
        self.scroll_a.config(command=self.list_a.yview)
        self.scroll_a.pack(side="right", fill="y")


    def principal(self):
        ###################### CURRENT BOX ##########################
        self.box_cur_temp.place(x=875,y=80)
        self.box_cur_humd.place(x=875,y=305)
        self.box_cur_air.place(x=875,y=530)

        #################### AVERAGE BOX ###########################
        self.box_ave_temp.place(x=1075,y=80)
        self.box_ave_humd.place(x=1075,y=305)
        self.box_ave_air.place(x=1075,y=530)

        ##################### GRAPH  BOX ############################
        self.box_temp.configure(width=660 ,height=215)
        self.box_temp.place(x=200,y=5)
        self.box_humd.configure(width=660 ,height=215)
        self.box_humd.place(x=200,y=230)
        self.box_air.configure(width=660 ,height=215)
        self.box_air.place(x=200,y=455)
    ##################### CURRENT  BOX ############################
        self.box_1_cur_temp = tk.Label(self.window,text="TEMPERATURA ACTUAL",font=("Helvetica 10 bold"),width=24,height=3,bg="#008B8B")
        self.box_1_cur_temp.place(x=875,y=5)
        self.box_1_cur_humd = tk.Label(self.window,text="HUMEDAD ACTUAL",font=("Helvetica 10 bold"),width=24,height=3,bg="#008B8B")
        self.box_1_cur_humd.place(x=875,y=230)
        self.box_1_cur_air = tk.Label(self.window,text="CALIDAD DE AIRE ACTUAL",font=("Helvetica 10 bold"),width=24 ,height=3,bg="#008B8B")
        self.box_1_cur_air.place(x=875,y=455)
    ########################## AVERAGE BOX ############################
        self.box_1_ave_temp = tk.Label(self.window,text="TEMPERATURA PROMEDIO",font=("Helvetica 10 bold"),width=24,height=3,bg="#ADD8E6")
        self.box_1_ave_temp.place(x=1075,y=5)
        self.box_1_ave_humd = tk.Label(self.window,text="HUMEDAD PROMEDIO",font=("Helvetica 10 bold"),width=24,height=3,bg="#ADD8E6")
        self.box_1_ave_humd.place(x=1075,y=230)
        self.box_1_ave_air = tk.Label(self.window,text="CALIDAD AIRE PROMEDIO",font=("Helvetica 10 bold"),width=24,height=3,bg="#ADD8E6")
        self.box_1_ave_air.place(x=1075,y=455)
    #########################   LIST BOX  ##############################
        self.frame.place_forget()
        self.frame1.place_forget()
        self.frame2.place_forget()

    def pagina_temperatura(self):
        self.box_temp.place(x=200,y=5)
        self.box_temp.configure(width=660 ,height=650)
        self.box_ave_temp.place(x=1075,y=80)
        self.box_cur_temp.place(x=875,y=80)
        self.box_1_cur_temp.place(x=875,y=5)
        self.box_1_ave_temp.place(x=1075,y=5)
        self.frame.place(x=925,y=180)

        self.box_humd.place_forget()
        self.box_air.place_forget()
        self.box_cur_humd.place_forget()
        self.box_cur_air.place_forget()
        self.box_ave_humd.place_forget()
        self.box_ave_air.place_forget()
        self.box_1_cur_humd.place_forget()        
        self.box_1_cur_air.place_forget()        
        self.box_1_ave_humd.place_forget()        
        self.box_1_ave_air.place_forget()        
        self.frame1.place_forget()
        self.frame2.place_forget()

    def pagina_humedad(self):
        self.box_humd.configure(width=660 ,height=650)
        self.box_humd.place(x=200,y=5)
        self.box_ave_humd.place(x=1075,y=80)
        self.box_cur_humd.place(x=875,y=80)
        self.box_1_cur_humd.place(x=875,y=5)      
        self.box_1_ave_humd.place(x=1075,y=5)      
        self.frame1.place(x=925,y=180)

        self.box_temp.place_forget()
        self.box_air.place_forget()
        self.box_cur_temp.place_forget()
        self.box_cur_air.place_forget()
        self.box_ave_temp.place_forget()
        self.box_ave_air.place_forget()
        self.box_1_cur_temp.place_forget()        
        self.box_1_cur_air.place_forget()        
        self.box_1_ave_temp.place_forget()        
        self.box_1_ave_air.place_forget()        
        self.frame.place_forget()
        self.frame2.place_forget()
        
    def pagina_aire(self):
        self.box_air.configure(width=660 ,height=650)
        self.box_air.place(x=200,y=5)
        self.box_ave_air.place(x=1075,y=80)
        self.box_cur_air.place(x=875,y=80)
        self.box_1_cur_air.place(x=875,y=5)      
        self.box_1_ave_air.place(x=1075,y=5)      
        self.frame2.place(x=925,y=180)
        
        self.box_temp.place_forget()
        self.box_humd.place_forget()
        self.box_cur_humd.place_forget()
        self.box_cur_temp.place_forget()
        self.box_ave_temp.place_forget()
        self.box_ave_humd.place_forget()
        self.box_1_cur_temp.place_forget()        
        self.box_1_cur_humd.place_forget()        
        self.box_1_ave_temp.place_forget()        
        self.box_1_ave_humd.place_forget()        
        self.frame1.place_forget()
        self.frame.place_forget()
class Datos_broker():
    def __init__(self,window):
        self.window=window
        self.box_menu = tk.Label(self.window,width=27 ,height=44,bg="#A9A9A9",relief=tk.RAISED)
        self.box_menu.place(x=0,y=5)
        self.l1=tk.Label(self.window,text="PARAMETROS DEL BROKER",font=("Helvetica 10 bold"),bg="#A9A9A9")
        self.l1.place(x=0,y=40)
        self.host_1 = tk.Label(self.window,text="BROKER",font=("Helvetica 9 bold"),bg="#A9A9A9")
        self.host_1.place(x=5,y=75)
        self.port_1 = tk.Label(self.window,text="PORT",font=("Helvetica 9 bold"),bg="#A9A9A9")
        self.port_1.place(x=5,y=125) 
        self.user_1 = tk.Label(self.window,text="USERID",font=("Helvetica 9 bold"),bg="#A9A9A9")
        self.user_1.place(x=5,y=175) 
        self.pass_1 = tk.Label(self.window,text="PASSWORD",font=("Helvetica 9 bold"),bg="#A9A9A9")
        self.pass_1.place(x=5,y=225) 
        self.topic_1 = tk.Label(self.window,text="TOPIC TEMPERATURA",font=("Helvetica 9 bold"),bg="#A9A9A9")
        self.topic_1.place(x=5,y=275) 
        self.topic_2 = tk.Label(self.window,text="TOPIC HUMEDAD",font=("Helvetica 9 bold"),bg="#A9A9A9")
        self.topic_2.place(x=5,y=325) 
        self.topic_3= tk.Label(self.window,text="TOPIC CALIDA AIRE",font=("Helvetica 9 bold"),bg="#A9A9A9")
        self.topic_3.place(x=5,y=375) 

                
if __name__ == '__main__':
    temperatura=1
    count=1
            ################    PARAMETROS ############################
    desconeccion=False
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
    client = mqttClient.Client("Pyhton")               #create new instance
    client.username_pw_set(user, password=password)    #set username and password
    
    client.on_connect= on_connect 
    client.on_message=on_message                     #attach function to callback
    client.connect(broker_address, port=port)          #connect to broker
    client.on_disconnect=on_disconnect
    """
    ## SUBSCRIBING
    #client.on_message= on_message                      #attach function to callback
    client.message_callback_add(topic_temperatura, on_message_temperature)
    client.message_callback_add(topic_humedad, on_message_humedad)
    client.message_callback_add(topic_air, on_message_calidad)
    client.loop_start()
    """
################ LIST BOX ###############################

    ###################  MENU ##################################
    Datos_broker(window)
    Main_button = tk.Menu(window,title="MENU",relief= tk.RAISED)
    #Main_button.add_checkbutton(label="Temperatura")
    host = tk.Entry(window,font=("Helvetica 9 italic"),width=26)
    host.place(x=5,y=100)
    host.insert(0,broker_address)
    port1= tk.Entry(window,font=("Helvetica 9 italic"),width=26)
    port1.place(x=5,y=150) 
    port1.insert(0,port)
    user1= tk.Entry(window,font=("Helvetica 9 italic"),width=26)
    user1.place(x=5,y=200) 
    user1.insert(0,user)
    passw= tk.Entry(window,font=("Helvetica 9 italic"),width=26)
    passw.place(x=5,y=250) 
    passw.insert(0,password)
    topic_t= tk.Entry(window,font=("Helvetica 9 italic"),width=26)
    topic_t.place(x=5,y=300) 
    topic_t.insert(0,topic_temperatura)
    topic_h= tk.Entry(window,font=("Helvetica 9 italic"),width=26)
    topic_h.place(x=5,y=350) 
    topic_h.insert(0,topic_humedad)
    topic_a= tk.Entry(window,font=("Helvetica 9 italic"),width=26)
    topic_a.place(x=5,y=400) 
    topic_a.insert(0,topic_air)
       
    conectar = tk.Button(window,text="Conectar",height=2, width=10,font=("Helvetica", 9, 'bold'),relief=tk.RAISED,command=conexion)
    conectar.place(x=20,y=450)
    data = DataPlot()
################# PAGINAS ###############################
    Pagina_inicio=Start_page(window)
    submenu = tk.Menu(window)
    submenu.add_command(label="Inicio",command=conexion_inicio)
    submenu.add_command(label="Temperatura",command=conexion_t)
    submenu.add_command(label="Humedad",command=conexion_h)
    submenu.add_command(label="Calidad de Aire",command=conexion_a)
    window.config(menu=submenu)
################ PLOTS ####################################
    fig = Figure(figsize=([6.4, 1.9]))
    a = fig.add_subplot(111)
    a.set_ylabel("°C", fontsize=8)
    a.plot([],[],"ro-")    
    a.set_title("TEMPERATURA")
    a.grid()
    a.set_ylim(10,25)
    canvas = FigureCanvasTkAgg(fig, master=Pagina_inicio.box_temp,)
    plot_data_t=RealtimePlot(a,canvas,fig)
    
    fig1 = Figure(figsize=([6.4, 1.9]))
    b = fig1.add_subplot(111)
    b.plot([],[],"ro-")
    b.set_ylabel("°%", fontsize=8)
    b.set_title("HUMEDAD")
    b.grid()    
    b.set_ylim(30,80)
    canvas1 = FigureCanvasTkAgg(fig1, master=Pagina_inicio.box_humd)
    plot_data_h=RealtimePlot(b,canvas1,fig1)

    fig2 = Figure(figsize=([6.4, 1.9]))
    c = fig2.add_subplot(111)
    b.plot([],[], "go-")
    c.set_ylabel("°% Air", fontsize=8)
    c.set_title("CALIDAD DE AIRE")
    c.grid()    
    c.set_ylim(0,60)
    canvas2 = FigureCanvasTkAgg(fig2, master=Pagina_inicio.box_air)
    plot_data_a=RealtimePlot(c,canvas2,fig2)

############## LAZO #################################    
    cancel_id = None
    window.mainloop()

