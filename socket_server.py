# NAME : YASH BHARATKUMAR AVLANI
# Student ID : 1001670008, Net ID : yba0008
# socket connection reference : https://www.journaldev.com/15906/python-socket-programming-server-client
# logical clock timer : https://stackoverflow.com/questions/3393612/run-certain-code-every-n-seconds

import socket
import threading
from tkinter import *
import tkinter.scrolledtext as ScrolledText
import tkinter
import tkinter as tk
from datetime import datetime
import datetime
from email.utils import formatdate, localtime
from lib2to3.tests.data.infinite_recursion import timeval
import os
from test.test_threading_local import target


connections = {}
scrollTextMain = None # declaring scrolledText (Server Log) to be accessible from anywhere
scrollTextSub = None # declaring scrolledText (Connection Log) to be accessible from anywhere

def parse_http_message(message): # parse HTTP message
    data = message.decode().split('\r\n')[-1]
    data = data.replace('DATA:', '')
    return data

    
def get_http_message(message): # encode HTTP message
    http_format = 'POST /test HTTP/1.1\r\n'\
'Host: localhost\r\n'\
'Date: #DATE#\r\n'\
'User-Agent: client_application\r\n'\
'Content-Type: application/x-www-form-urlencoded\r\n'\
'Content-Length: #LEN#\r\n'\
'\r\n'\
'DATA:' + message
    http_format = http_format.replace('#LEN#', str(len(message)))
    date = formatdate(timeval=None, localtime=False, usegmt=True)
    return http_format


def server_program(): #defining server program
    
    while True:
        host = socket.gethostname() # get the hostname
        port = 5000  # initiate port no above 1024
    
        server_socket = socket.socket()  # get instance
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        # bind function takes tuple as argument
        server_socket.bind((host, port))  # bind host address and port together
    
        # configure how many client the server can listen simultaneously
        server_socket.listen(2)
        print("Server Connecting with host : " + host)
        scrollTextMain.insert(INSERT, "Server Started with host : " + host)
        
        conn, address = server_socket.accept()  # accept new connection
        print('Accepted')

        threading.Thread(target=client_handler, args=(conn, address)).start() # call server_program with thread
    

def quit_Manual_Server():
    print("Quit Called 1")
    os._exit(0)   


def client_handler(conn, address):
    
    user = ''
    print(connections)
    print("Connection from: " + str(address))
    
    try:
        while True:
     
            receivedData = conn.recv(1024)
            
            if receivedData:
            # receive data stream. it won't accept data packet greater than 1024 bytes
            
                print(' Received Unparsed Data From Client : ', receivedData)
                scrollTextMain.insert(INSERT, 'Unparsed Data From Client : ' + receivedData.decode() + '\n')
                receivedData = parse_http_message(receivedData)
                print('Received Data ', receivedData)
                print('From', user)
                
                if ':' in receivedData:
                                   
                        # send message to destination
                        dest_client_name = receivedData.split(':')[0]
                        
                        if dest_client_name == "All":
#                             print("1toN")
                            for key, value in connections.items():
                                if user != key:
                                    receivedStr = receivedData
                                    strTemp = dest_client_name + ':'
                                    receivedStr = receivedData.replace(strTemp, '')
                                    receivedStr = 'From ' + user + ' : ' + receivedStr  + ' to : All***' 
                                    dest_conn = value
                                    dest_conn.send(get_http_message(receivedStr).encode())
                            scrollTextMain.insert(INSERT, receivedStr + '\n') # insert message in scrollerText
                                 
                        
                        else:
                            strTemp = dest_client_name + ':'
                            receivedData = receivedData.replace(strTemp, '')
                            receivedData = 'From ' + user + ' : ' + receivedData
                            print(receivedData)
                            print("Destination Client Name is :", dest_client_name)
                            dest_conn = connections[dest_client_name]
                            dest_conn.send(get_http_message(receivedData).encode())
                            
                            scrollTextMain.insert(INSERT, receivedData + '\n') # insert message in scrollerText
        
                
                else:
            
                    user = receivedData
                    print('Client ' + user + ' has connected.')
                    connections[user] = conn
                    print(connections)
                    scrollTextMain.insert(INSERT, 'Client ' + user + ' has connected.' + '\n' + '\n')
                    strConnectionList = ''
                    for key, value in connections.items():
                        strConnectionList = strConnectionList + key + ' '
            
                    lblConnections['text'] = strConnectionList
        #             scrollTextSub.insert(INSERT, user + '\n') # insert message in scrollerText
        
                print("Out of both conditions")
                
            else:
                print(user + 'DISCONNECTED')
    
    except Exception as e: print(e)
        
        
    finally:
        print("Client Destroyed ===> SERVER")
        print('USER Name : ', user)
        if user:
            scrollTextMain.insert(INSERT, 'Client ' + user + ' Disconnected')
            del connections[user]
            strConnectionList = ''
            for key, value in connections.items():
                strConnectionList = strConnectionList + key + ' '
            lblConnections['text'] = strConnectionList
            print(connections)
            

    
    

if __name__ == '__main__':
    
    threading.Thread(target=server_program).start() # call server_program with thread
    
    master = Tk()

    lbl = Label(master, text='SERVER')
    lbl.grid(row=0)

    Button(master, text='Quit',command=quit_Manual_Server).grid(row=0, column=1, sticky=W, pady=4)

    scrollTextMain = ScrolledText.ScrolledText(master)
    scrollTextMain.grid(row=1)
    lblConnections = Label(master, text='Client Connected')
    lblConnections.grid(row=3, column=0)
    lblConnections['text'] = 'List of Client'
    
#     self.lblConnections = 'Hello!'
#     scrollTextSub = ScrolledText.ScrolledText(master)
#     scrollTextSub.grid(row=1, column=1)

    master.mainloop()
    
#     server_program()
