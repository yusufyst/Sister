import xmlrpc.client
from tkinter import *
import subprocess
from tkinter.filedialog import askopenfilename
ip_server_port = 'http://192.168.100.3:8003'
def upload():
    Tk().withdraw() 
    namafile = askopenfilename() 
    x = namafile.split("/")

    try:
        with open(namafile,"rb") as pointer:
            data = xmlrpc.client.Binary(pointer.read())
            #print(data)
            pointer.close()
            a = x[len(x)-1]
            
            conn.FTPUpload(a,data)
            print("file [ "+a+" ] uploaded")
    except:
        print("UPLOAD FAILED")    
def download():
    dir_server = "R:/FTPServer/"
    namafile = input("NAMA FILE : ")
    dir_server += namafile
    
    dir_client = "R:/FTPClient/"
    
    #print(x)
    #print(filepath)
    try:
        
        pointer = open(dir_client+namafile,"wb")
        data = conn.FTPDownload(dir_server)
        pointer.write(data.data)
        print("Download ["+namafile+"] Berhasil")
        pointer.close()
    except:
        print("Download Gagal")

def DirectoryList():
    data = conn.FTPDirectory()
    print(data)

out=0    
conn = xmlrpc.client.ServerProxy(ip_server_port)
while (out==0):
    print("1. Upload File")
    print("2. Download File")
    print("3. List File di Server")
    print("4. Close")
    inputan = input("Choose : ")
    if inputan == '1':
        upload()
    elif inputan == '2':
        download()
    elif inputan == '3':
        DirectoryList()
    elif inputan == '4':
        out=1
    print("")