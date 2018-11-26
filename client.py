#Урок №7:
#1. Реализовать обработку нескольких клиентов на сервере, используя функцию select. 
#Клиенты должны общаться в «общем чате»: каждое сообщение участника отправляется всем, подключенным к серверу.
#2. Реализовать функции отправки/приема данных на стороне клиента. 
#Чтобы упростить разработку на данном этапе, пусть клиентское приложение будет либо только принимать, 
#либо только отправлять сообщения в общий чат. Эти функции надо реализовать в рамках отдельных скриптов.

#python client.py -a 127.0.0.1 -p 8888

import logging 
import sys
import json 
from typing import Any, Dict 
from socket import *
import argparse
from subprocess import Popen 

print( 'Start client!' )
def get_args():
    # Assign description to the help doc
    parser = argparse.ArgumentParser(
        description='Script retrieves schedules from a given server')
    # Add arguments
    parser.add_argument(
        '-a', '--server', type=str, help='Server name', required=True)
    parser.add_argument(
        '-p', '--port', type=str, help='Port number', required=True, nargs='+')
    #parser.add_argument(
    #    '-k', '--keyword', type=str, help='Keyword search', required=False, default=None)
    # Array for all arguments passed to script
    args = parser.parse_args()
    # Assign args to variables
    server = args.server
    port = args.port[0].split(",")
    ##keyword = args.keyword
    # Return all variable values
    return server, port 

try :
    server, port = get_args()
    port_number = 8000
    for p in port:
       port_number=int(p)
	  
    p_list=[]	  
    while True:
        user=input("s - start 10 clients, x - close clients, q - quit \n")
        if user == 'q':
            break
        elif user == 's':	   
            for _ in range(10): 	
                #p_list.append(Popen('python client.py'.split())) 	
                print('10 clients started') 
                serv = socket(AF_INET, SOCK_STREAM) 
                serv.connect(( 'localhost' , port_number )) 
                msg = {"action" : "msg", "to" : "room #1", "from" : "alex_account", "message" : "Hello, server!"}
                msg_str = json.dumps(msg)
                serv.send(msg_str.encode( 'utf-8' ))
                data = serv.recv( 1000000 )
                print('The message from server: '+data.decode( 'utf-8' )+', length '+str(len(data))+'bytes' )
                serv.close()				
                	
        elif user == 'x':
            for p in p_list:
                p.kill()
            p_list.clear()				
    while False :
        s = socket(AF_INET, SOCK_STREAM) 
        s.connect(( 'localhost' , port_number )) 
        msg = {"action" : "authenticate", "user" : {"account_name" : "alex", "password" : "alex_pwd"}}
        msg_str = json.dumps(msg)
        s.send(msg_str.encode( 'utf-8' ))
        data = s.recv( 1000000 )
        print('The message from server: '+data.decode( 'utf-8' )+', length '+str(len(data))+'bytes')
        s.close()
    
        s = socket(AF_INET, SOCK_STREAM) 
        s.connect(( 'localhost' , port_number )) 
        msg = {"action" : "msg", "to" : "room #1", "from" : "alex_account", "message" : "Hello, server!"}
        msg_str = json.dumps(msg)
        s.send(msg_str.encode( 'utf-8' ))
        data = s.recv( 1000000 )
        print('The message from server: '+data.decode( 'utf-8' )+', length '+str(len(data))+'bytes' )
        s.close()
    
        s = socket(AF_INET, SOCK_STREAM) 
        s.connect(( 'localhost' , port_number )) 
        msg = {"action": "quit", "message": "Quit"}
        msg_str = json.dumps(msg)
        s.send(msg_str.encode( 'utf-8' ))
        data = s.recv( 1000000 )
        print('The message from server: '+data.decode( 'utf-8' )+', length '+str(len(data))+'bytes' )
        s.close()
        break

except OSError as e:      
    print('Error:', e.strerror)
    
