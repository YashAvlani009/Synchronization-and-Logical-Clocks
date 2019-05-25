# NAME : YASH BHARATKUMAR AVLANI
# Student ID : 1001670008, Net ID : yba0008
# socket connection reference : https://www.journaldev.com/15906/python-socket-programming-server-client
# logical clock timer : https://stackoverflow.com/questions/3393612/run-certain-code-every-n-seconds

from tkinter import *
from tkinter import scrolledtext
import tkinter.scrolledtext as ScrolledText
from email.utils import formatdate
import os
import socket

from tkinter import simpledialog
import tkinter
import tkinter as tk
from socket_server import connections
import threading
import random

# Connection Process
host = socket.gethostname()  # as both code is running on same pc
port = 5000  # socket server port number
client_socket = socket.socket()  # instantiate


clockTime = 0 # inte variable that will manage the clock



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
    http_format = http_format.replace('#DATE#', date)
    return http_format

class EntryWithPlaceholder(tk.Entry):  # Class to Put placeholder in Entry 

    def __init__(self, master=None, placeholder="PLACEHOLDER", color='grey'):
        super().__init__(master)

        self.placeholder = placeholder
        self.placeholder_color = color
        self.default_fg_color = self['fg']

        self.bind("<FocusIn>", self.foc_in)
        self.bind("<FocusOut>", self.foc_out)

        self.put_placeholder()

    def put_placeholder(self):
        self.insert(0, self.placeholder)
        self['fg'] = self.placeholder_color

    def foc_in(self, *args):
        if self['fg'] == self.placeholder_color:
            self.delete('0', 'end')
            self['fg'] = self.default_fg_color

    def foc_out(self, *args):
        if not self.get():
            self.put_placeholder()


def client_program(): # client pro
    
    print("CLient Program Called")
    
    print('Number of Connections ', len(connections))
    global clockTime
    if len(connections) < 3:

        try:
            while True: 
        
                data = parse_http_message(client_socket.recv(1024)) # receive response from server
            
                if data:
              
                    print('Received from server: ' + data)  # show in terminal
                    currentReceivedTime = data.split('|')[1]
                    print('currentReceivedTime ===> CLIENT',currentReceivedTime)
                    if int(currentReceivedTime) > clockTime:
                      
                        print('Current Time is : ', clockTime)
                        clockTime = int(currentReceivedTime) + 1
                        strInsert = 'Current time became : ' + str(clockTime)
                        print('Current time became : ', clockTime)
                        
                    else:
                        strInsert = 'Current time became : ' + str(clockTime)
                        print("no adjustment was necessary.")
                        
                    scrolledtextLogs.insert(INSERT, data.split('|', 1)[0] + '\n') # insert message in scrollerText
                
                    scrolledtextLogs.insert(INSERT, strInsert + '\n') # insert message in scrollerText

        except Exception as e: print(e)       

        finally:
            print("Entered in finally ===> CLIENT")
            scrolledtextLogs.insert(INSERT, 'An existing connection with SERVER forcibly closed.')
#             window.destroy()

        
    else:
    
        print("Max Client Reached")
    
def quit_Manual():
    print("Byee")
    os._exit(0)
  

def on_closing():
    quit_Manual()


def send_message(): # function to send message for 1to1 and 1toN
    
    print('MSG: ',e1.get())
    print('DEstin :',e2.get())
    
    if e2.get() != "Destination Client" and e2.get() != "": # check Destination is not empty
        
        if e1.get() != "Message" and e1.index("end") != 0: # check message is not empty
#             message = "BUZZ!!"
           
            print("Destination Client Name is :", e2.get())
            message = e2.get() + ':' + e1.get() + '|' + str(clockTime) #concatinate destination and message with :
 
            client_socket.send(get_http_message(message).encode())  # send message
            scrolledtextLogs.insert(INSERT, message.split('|', 1)[0]  + '\n')
            e1.delete(0, 'end')
            
            print('GREATTTTTTTTT===============>', message)
         
        else:
            print("Please enter the message")
         
    else:
         
        destName = e2.get()
        print('Enter the destination client:' + destName)
   

def clockTimer():  # function that manages the local clock timer for each client
  
    threading.Timer(1.0, clockTimer).start()
    global clockTime
    clockTime += value
    toBePrinted = username + ',' + str(clockTime)
    print(toBePrinted)


if __name__ == '__main__':
    print("Main")
    
    clockTime = 0
    client_socket.connect((host, port))  # connect to the server 

    application_window = tkinter.Tk() # Dialogue to GET the UserName

    username = simpledialog.askstring("Input", "Enter the UserName", parent=application_window)

    threading.Thread(target=client_program).start()
    
    global value
    value = random.randint(1,10) # generate a random number to to creating logical clock
    clockTimer()

    if username is not None:
    
        client_socket.send(get_http_message(username).encode())  # send message
    
        print("Your first name is ", username)
        master = Tk()
    
        lbl = Label(master, text=username) # declaring a label
        lbl.grid(row=0)
    
        e1 = EntryWithPlaceholder(master, "Message") # declaring message entry
        e1.grid(row=4, column=1)
        
        e2 = EntryWithPlaceholder(master, "Destination Client") # declaring Destination Client entry
        e2.grid(row=4, column=0)
        
        btn = Button(master, text='Send', command=send_message) # declaring Send button
        btn.grid(row=4, column=2)
    
        # declaring Quit button
        Button(master, text='Quit', command=quit_Manual).grid(row=0, column=2, sticky=W, pady=4) 
    
        scrolledtextLogs = ScrolledText.ScrolledText(master) # scrollText for client logs
        scrolledtextLogs.grid(row=2)
        
        master.protocol("WM_DELETE_WINDOW", on_closing)
    
        master.mainloop()
    
    else:
        print("You don't have a first name?")
        
        
    
    
#     client_program()
#     threading.Thread(target=check_new_message).start()
