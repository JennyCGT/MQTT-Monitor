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
import csv
client = mqttClient.Client("Pyhton")               #create new instance
Connected =False
Page_name=""
boton=False
####################### CALLBACKS ########################################

def conexion():
    global Connected  
    global client
    global boton
    broker_address= host.get()  #Broker address
    port = port1.get()                    #Broker port
    user = user1.get()                    #Connection username
    password = passw.get()            #Connection password
    topic_temperatura =topic_t.get()
    topic_humedad = topic_h.get()
    topic_air=topic_a.get()
    print(type(conectar.configure('text')))
######################## SETTING MQTT ################################
    client.username_pw_set(user, password=password)    #set username and password
    boton=True
    status= client.is_connected()
    print(status)
    
    if status==False:
        client.connect(broker_address, port=int(port),keepalive=3)
        client.message_callback_add(topic_temperatura, on_message_temperature)
        client.message_callback_add(topic_humedad, on_message_humedad)
        client.message_callback_add(topic_air, on_message_calidad)
        client.loop_start()
        print("COnection") 

    if conectar.configure('text')[4]== 'Connected':
        Pagina_inicio.principal()
        canvas.get_tk_widget().config(width=640, height=190)
        canvas.get_tk_widget().place(x=10,y=10)
        canvas.draw()
        canvas1.get_tk_widget().config(width=640, height=190)
        canvas1.get_tk_widget().place(x=10,y=10)
        canvas1.draw()
        canvas2.get_tk_widget().config(width=640, height=190)      
        canvas2.get_tk_widget().place(x=10,y=10)
        canvas2.draw()
        count=1
        if client.connected_flag==True and Connected==0:
            conectar.configure(text="Disconnected")
        else:
            print("Error Conexion")
    else:
        conectar.configure(text="Connected")
        client.loop_stop()
        client.disconnect()
        tk.messagebox.showinfo("Conexion MQTT", "Successful Disconnection") 
        #tk.messagebox.showinfo("Conexion MQTT", "Desconexion") 

def conexion_inicio():
    print("INICIO")
    global Page_name
    Page_name="Inicio"
    Pagina_inicio.principal()
    canvas.get_tk_widget().config(width=640, height=190)
    canvas1.get_tk_widget().config(width=640, height=190)
    canvas2.get_tk_widget().config(width=640, height=190)

def conexion_t():
    global Page_name
    Page_name="Temperatura"
    print("ABRIR TEMPERATURA")
    Pagina_inicio.pagina_temperatura()
    canvas.get_tk_widget().config(width=640, height=580)

def conexion_h():
    global Page_name
    Page_name="Humedad"
    print("ABRIR TEMPERATURA")
    Pagina_inicio.pagina_humedad()
    canvas1.get_tk_widget().config(width=640, height=580)

def conexion_a():
    global Page_name
    Page_name="Aire"
    print("ABRIR TEMPERATURA")    
    Pagina_inicio.pagina_aire()
    canvas2.get_tk_widget().config(width=640, height=580)

def get_data():
    print("Exportando")
    with open('Output.csv','w', newline='') as result_file:
        wr = csv.writer(result_file,delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        wr.writerows(data.data)
                
############### MQTT CALLBACK #######################
def on_disconnect(client, userdata, rc):
    print("desco")
    client.connected_flag=False
    Connected=client.connected_flag
    #tk.messagebox.showinfo("Conexion MQTT", "Desconexion exitosa") 
   
def on_connect(client, userdata, flags, rc):
    global Connected                #Use global variable
    global boton
    print(rc)    
    if rc == 0:
        client.connected_flag=True #set flag       
        Connected=rc        #client.subscribe("lKlhsHxr6zKCwBr")
        client.subscribe(topic_temperatura, qos=1)
        client.subscribe(topic_humedad, qos=1)
        client.subscribe(topic_air, qos=1)
        print("conexion exitosa")
        if boton:
            tk.messagebox.showinfo("Conexion MQTT", "Successful Connection")
            conectar.configure(text="Disconnected")
            boton=False
    else:
        print("Connection failed")
        if boton:
            tk.messagebox.showinfo("Conexion MQTT", "Connection failed")
            boton=False

def on_message(client, userdata, message):
    a=str(message.payload.decode("utf-8"))
    print(message.topic)
    
def on_message_temperature(client, userdata, message):
    a=str(message.payload.decode("utf-8"))
    save_data_sync(float(a),message.topic)

def on_message_humedad(client, userdata, message):
    global Connected
    b=str(message.payload.decode("utf-8"))
    save_data_sync(float(b),message.topic)
    #if conectar.configure('text')[4]== 'Conectar':
    #    client.loop_stop()
    #    client.disconnect()

def on_message_calidad(client, userdata, message):          
    c=str(message.payload.decode("utf-8")) 
    save_data_sync(float(c),message.topic)
    time.sleep(2)

def save_data_sync(a,topic):
    if(topic==topic_t.get()):
        data.save(a,0)
        #plot_data_t.plot(data.axis_t,data.axis_tt)
    
    if(topic==topic_h.get()):
        data.save(a,1)
        #plot_data_h.plot(data.axis_h,data.axis_tt)
    if(topic==topic_a.get()):
        data.save(a,2)
        #plot_data_a.plot(data.axis_a,data.axis_tt)
        
def bytes_to_decimal(i,d):  
    xx = i - 127
    dec = (-d if xx < 0 else d)/100
    return xx + dec    

def promediarLista(lista):
    sum=0.0
    i=0
    while i<len(lista):
        sum=lista[i]+sum
        i+=1
    return float("{0:.2f}".format(sum / len(lista)))

class DataPlot:
    def __init__(self, max_entries = 30):
        self.axis_t = deque([0.0],maxlen=max_entries)
        self.axis_h = deque([0.0],maxlen=max_entries)
        self.axis_a = deque([0.0],maxlen=max_entries)
        self.axis_tt = deque(maxlen=max_entries)
        self.axis_th = deque(maxlen=max_entries)
        self.axis_ta = deque(maxlen=max_entries)
        self.data_mqtt=[0.0,0.0,0.0]
        self.data = []
        self.max_entries = max_entries
        self.count=0
    def save_all(self,t,h,a):
        tim=datetime.now().strftime('%Y %m %d %H:%M:%S')
        ######## TEMPERATURA ##########################
        self.axis_t.append(t)
        self.axis_tt.append(datetime.now().strftime('%H:%M:%S'))
        Pagina_inicio.list_t.insert("",index=0,text=tim,values=str(t))
        Pagina_inicio.box_cur_temp.configure(text=t)
        Pagina_inicio.box_ave_temp.configure(text=promediarLista(data.axis_t))  
        ######## HUMEDAD ##############
        self.axis_h.append(h)
        Pagina_inicio.list_h.insert("",index=0,text=tim,values=str(h))
        Pagina_inicio.box_cur_humd.configure(text=h)
        Pagina_inicio.box_ave_humd.configure(text=promediarLista(data.axis_h)) 
         
        ########## AIRE ####################
        self.axis_a.append(a)
        Pagina_inicio.list_a.insert("",index=0,text=tim,values=str(a))
        Pagina_inicio.box_cur_air.configure(text=a)
        Pagina_inicio.box_ave_air.configure(text=promediarLista(data.axis_a))
        self.data.append([tim ,str(t),str(h),str(a) ])
        plot_data_t.plot(data.axis_t,data.axis_tt)
        plot_data_h.plot(data.axis_h,data.axis_tt)
        plot_data_a.plot(data.axis_a,data.axis_tt)

    def save (self,a,i):
        self.count=self.count+1
        self.data_mqtt[i]=a
        if(self.count==3):
            print(self.data_mqtt)
            self.save_all(self.data_mqtt[0],self.data_mqtt[1],self.data_mqtt[2])
            self.count=0

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
        self.box_1_cur_temp = tk.Label(self.window,text="CURRENT TEMPERATURE",font=("Helvetica 10 bold"),width=24,height=3,bg="#008B8B")
        self.box_1_cur_humd = tk.Label(self.window,text="CURRENT HUMIDITY",font=("Helvetica 10 bold"),width=24,height=3,bg="#008B8B")
        self.box_1_cur_air = tk.Label(self.window,text="CURRENT AIR QUALITY",font=("Helvetica 10 bold"),width=24 ,height=3,bg="#008B8B")
################# average title ###############################
        self.box_1_ave_temp = tk.Label(self.window,text="AVERAGE TEMPERATURE",font=("Helvetica 10 bold"),width=24,height=3,bg="#ADD8E6")
        self.box_1_ave_humd = tk.Label(self.window,text="AVERAGE HUMIDITY",font=("Helvetica 10 bold"),width=24,height=3,bg="#ADD8E6")
        self.box_1_ave_air = tk.Label(self.window,text="AVERAGE AIR QUALITY",font=("Helvetica 10 bold"),width=24,height=3,bg="#ADD8E6")

############### LISTBOX ##########################################
        self.frame=tk.Frame(self.window,width=600, height=500,bg="#ADF8E6")
        self.list_t =tk.ttk.Treeview(self.frame,columns=("Temperatura"))#,font=("Helvetica 10 "),width=45, height=25,)
        #self.list_t =tk.Listbox(self.frame,font=("Helvetica 10 "),width=45, height=25,)
        self.list_t.heading('#0', text='Date and Time')
        self.list_t.heading('Temperatura', text='Temperature')
        #self.list_t.insert(0,"          FECHA,                     TEMPERATURA \N")
        self.list_t.pack(side="left", fill="y")
        self.scroll_t = tk.Scrollbar(self.frame, orient="vertical")
        self.scroll_t.config(command=self.list_t.yview)
        self.scroll_t.pack(side="right", fill="y")

        self.frame1=tk.Frame(self.window,width=600, height=500,bg="#ADF8E6")
        self.list_h =tk.ttk.Treeview(self.frame1,columns=("Humedad"))#,font=("Helvetica 10 "),width=45, height=25,)
        self.list_h.heading('#0', text='Date and Time')
        self.list_h.heading('Humedad', text='Humidity')        
        #self.list_h =tk.Listbox(self.frame1,font=("Helvetica 10 "),width=45, height=25,)
        #self.list_h.insert(0,"          FECHA                     HUMEDAD")
        self.list_h.pack(side="left", fill="y")
        self.scroll_h = tk.Scrollbar(self.frame1, orient="vertical")
        self.scroll_h.config(command=self.list_h.yview)
        self.scroll_h.pack(side="right", fill="y")

        self.frame2=tk.Frame(self.window,width=600, height=500,bg="#ADF8E6")
        self.list_a =tk.ttk.Treeview(self.frame2,columns=("Aire"))#,font=("Helvetica 10 "),width=45, height=25,)
        self.list_a.heading('#0', text='Date and Time')
        self.list_a.heading('Aire', text='Air Quality')        
        #self.list_a =tk.Listbox(self.frame2,font=("Helvetica 10 "),width=45, height=25,)
        #self.list_a.insert(0,"          FECHA                     CALIDAD AIRE")
        self.list_a.pack(side="left", fill="y")
        self.scroll_a = tk.Scrollbar(self.frame2, orient="vertical")
        self.scroll_a.config(command=self.list_a.yview)
        self.scroll_a.pack(side="right", fill="y")

###################### BOTONES DE DESCARGAR #######################################
        self.exportar = tk.Button(self.window,text="Exportar",height=2, width=10,font=("Helvetica", 9, 'bold'),relief=tk.RAISED,command=get_data)

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
        #self.box_1_cur_temp = tk.Label(self.window,text="TEMPERATURA ACTUAL",font=("Helvetica 10 bold"),width=24,height=3,bg="#008B8B")
        self.box_1_cur_temp.place(x=875,y=5)
        #self.box_1_cur_humd = tk.Label(self.window,text="HUMEDAD ACTUAL",font=("Helvetica 10 bold"),width=24,height=3,bg="#008B8B")
        self.box_1_cur_humd.place(x=875,y=230)
        #self.box_1_cur_air = tk.Label(self.window,text="CALIDAD DE AIRE ACTUAL",font=("Helvetica 10 bold"),width=24 ,height=3,bg="#008B8B")
        self.box_1_cur_air.place(x=875,y=455)
    ########################## AVERAGE BOX ############################
        #self.box_1_ave_temp = tk.Label(self.window,text="TEMPERATURA PROMEDIO",font=("Helvetica 10 bold"),width=24,height=3,bg="#ADD8E6")
        self.box_1_ave_temp.place(x=1075,y=5)
        #self.box_1_ave_humd = tk.Label(self.window,text="HUMEDAD PROMEDIO",font=("Helvetica 10 bold"),width=24,height=3,bg="#ADD8E6")
        self.box_1_ave_humd.place(x=1075,y=230)
        #self.box_1_ave_air = tk.Label(self.window,text="CALIDAD AIRE PROMEDIO",font=("Helvetica 10 bold"),width=24,height=3,bg="#ADD8E6")
        self.box_1_ave_air.place(x=1075,y=455)
    #########################   LIST BOX  ##############################
        self.frame.place_forget()
        self.frame1.place_forget()
        self.frame2.place_forget()
        self.exportar.place_forget()
    def pagina_temperatura(self):
        self.box_temp.place(x=200,y=5)
        self.box_temp.configure(width=660 ,height=650)
        self.box_ave_temp.place(x=1075,y=80)
        self.box_cur_temp.place(x=875,y=80)
        self.box_1_cur_temp.place(x=875,y=5)
        self.box_1_ave_temp.place(x=1075,y=5)
        self.frame.place(x=875,y=180)
        self.exportar.place(x=1025,y=500)

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
        self.frame1.place(x=875,y=180)
        self.exportar.place(x=1025,y=500)

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
        self.frame2.place(x=875,y=180)
        self.exportar.place(x=1025,y=500)
        
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
        self.l1=tk.Label(self.window,text="BROKER PARAMETERS",font=("Helvetica 10 bold"),bg="#A9A9A9")
        self.l1.place(x=0,y=40)
        self.host_1 = tk.Label(self.window,text="BROKER",font=("Helvetica 9 bold"),bg="#A9A9A9")
        self.host_1.place(x=5,y=75)
        self.port_1 = tk.Label(self.window,text="PORT",font=("Helvetica 9 bold"),bg="#A9A9A9")
        self.port_1.place(x=5,y=125) 
        self.user_1 = tk.Label(self.window,text="USERID",font=("Helvetica 9 bold"),bg="#A9A9A9")
        self.user_1.place(x=5,y=175) 
        self.pass_1 = tk.Label(self.window,text="PASSWORD",font=("Helvetica 9 bold"),bg="#A9A9A9")
        self.pass_1.place(x=5,y=225) 
        self.topic_1 = tk.Label(self.window,text="TOPIC TEMPERATURE",font=("Helvetica 9 bold"),bg="#A9A9A9")
        self.topic_1.place(x=5,y=275) 
        self.topic_2 = tk.Label(self.window,text="TOPIC HUMIDITY",font=("Helvetica 9 bold"),bg="#A9A9A9")
        self.topic_2.place(x=5,y=325) 
        self.topic_3= tk.Label(self.window,text="TOPIC AIR QUALITY",font=("Helvetica 9 bold"),bg="#A9A9A9")
        self.topic_3.place(x=5,y=375) 
                
if __name__ == '__main__':
    temperatura=1
    count=0
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
######################## SETTING MQTT ################################
    #client = mqttClient.Client("Pyhton")               #create new instance
    client.username_pw_set(user, password=password)    #set username and password    
    client.on_connect= on_connect 
    client.on_message=on_message                     #attach function to callback
    client.on_disconnect=on_disconnect

#########################   WINDOWS #########################################
    window = tk.Tk() # initialise a window
    window.title("Monitoring IOT")
    window.geometry("1300x700+5+5")

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
       
    conectar = tk.Button(window,text="Connected",height=2, width=10,font=("Helvetica", 9, 'bold'),relief=tk.RAISED,command=conexion)
    conectar.place(x=20,y=450)
    data = DataPlot()
################# PAGINAS ###############################
    Pagina_inicio=Start_page(window)
    submenu = tk.Menu(window)
    submenu.add_command(label="Main",command=conexion_inicio)
    submenu.add_command(label="Temperature",command=conexion_t)
    submenu.add_command(label="Humidity",command=conexion_h)
    submenu.add_command(label="Air quality",command=conexion_a)
    window.config(menu=submenu)
################ PLOTS ####################################
    fig = Figure(figsize=([6.4, 1.9]))
    a = fig.add_subplot(111)
    a.set_ylabel("°C", fontsize=8)
    a.plot([],[],"ro-")    
    a.set_title("TEMPERATURE")
    a.grid()
    a.set_ylim(0,25)
    canvas = FigureCanvasTkAgg(fig, master=Pagina_inicio.box_temp,)
    plot_data_t=RealtimePlot(a,canvas,fig)
    
    fig1 = Figure(figsize=([6.4, 1.9]))
    b = fig1.add_subplot(111)
    b.plot([],[],"ro-")
    b.set_ylabel("°%", fontsize=8)
    b.set_title("HUMIDITY")
    b.grid()    
    b.set_ylim(30,80)
    canvas1 = FigureCanvasTkAgg(fig1, master=Pagina_inicio.box_humd)
    plot_data_h=RealtimePlot(b,canvas1,fig1)

    fig2 = Figure(figsize=([6.4, 1.9]))
    c = fig2.add_subplot(111)
    b.plot([],[], "go-")
    c.set_ylabel("°% Air", fontsize=8)
    c.set_title("AIR QUALITY")
    c.grid()    
    c.set_ylim(0,60)
    canvas2 = FigureCanvasTkAgg(fig2, master=Pagina_inicio.box_air)
    plot_data_a=RealtimePlot(c,canvas2,fig2)

############## LAZO #################################    
    window.mainloop()

