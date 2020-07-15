import xmlrpc.server
import subprocess
from os import listdir
from os.path import isfile, join
import xmlrpc.client
from tkinter import *
from xmlrpc.server import SimpleXMLRPCServer
from xmlrpc.server import SimpleXMLRPCRequestHandler
from threading import Thread
client = 'a'
connection = []
client_label = 'a'
ip = "192.168.100.3"
port = 8003

def start_server():
    server.serve_forever()
def start_thread():
    button.destroy()
    button2 = Button(window,command=dis,text="GET BEST CLIENT")
    button2.pack()
    thread = Thread(target=start_server)
    thread.start()
def start_window():
    window.mainloop()
def clientList():
    for i in range(len(connection)):
        print(connection[i])
def cekDirektori():
    #print((a))
    mypath="R:/FTPServer"
    onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]

    # for i in range(len(onlyfiles)):
    #     print(onlyfiles[i])
    return onlyfiles

def upload(filename,file):
    
    try:
        path = "R:/FTPServer/"+filename
        with open(path,"wb") as pointer:                  
            pointer.write(file.data)        
            pointer.close()
        x=0
        for i in connection:
            if i['ip'] == client:
                i['activity_point']+=1
                x=1
                print(i['ip'],"Telah Melakukan Upload")
                break
        if x == 0 :
            objek = {'ip' : client, 'activity_point' : 1}
            print(objek['ip'],"Telah Melakukan Upload")
            connection.append(objek)
        return True
    except:
        return "Error"
def recieveFile(file):
    print(file)
    try:
        with open(file,"rb") as pointer:
            data = xmlrpc.client.Binary(pointer.read())
            #print(data)
            pointer.close()
        x=0
        for i in connection:
            if i['ip'] == client:
                i['activity_point']+=1
                x=1
                print(i['ip'],"Telah Melakukan Download")
                break
        if x == 0 :
            objek = {'ip' : client, 'activity_point' : 1}
            print(objek['ip'],"Telah Melakukan Download")
            connection.append(objek)
        return data
    except:
        return "Error"

class RequestHandler(SimpleXMLRPCRequestHandler):
    rpc_paths = ('/RPC2')
    def __init__(self, request, client_address, server):
        global client
        client = client_address[0]
        SimpleXMLRPCRequestHandler.__init__(self, request, client_address, server)

def dis():
    global connection
    connection = sorted(connection, key= lambda x:x['activity_point'],reverse=True)
    best_client.config(text=connection[0])
def display_all_client():
    global client_label
    try:
        print("X")
        for i in connection:
            item = connection[i]
        
    except:
        client_label = Label(window,text=connection[0])
        client_label.pack()

# Membuat server
server = SimpleXMLRPCServer((ip,port), requestHandler=RequestHandler)
server.register_introspection_functions()

# Agar dapat diakses Client
server.register_function(upload,'FTPUpload')
server.register_function(recieveFile,'FTPDownload')
server.register_function(cekDirektori,'FTPDirectory')

# Membuat Tampilan
window = Tk()
window.geometry('500x500')
window.configure(bg='#fbcffc')
button = Button(window,command=start_thread,text="START SERVER",bg='#be79df')
button.pack()
buttonC = Button(window,command=display_all_client,text="GET CLIENT",bg='#be79df')
buttonC.pack()
best_client=Label(window,text="None")
best_client.pack()
window.mainloop()
