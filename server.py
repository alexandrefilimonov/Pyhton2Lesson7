#Урок №7:
#1. Реализовать обработку нескольких клиентов на сервере, используя функцию select. 
#Клиенты должны общаться в «общем чате»: каждое сообщение участника отправляется всем, подключенным к серверу.
#2. Реализовать функции отправки/приема данных на стороне клиента. 
#Чтобы упростить разработку на данном этапе, пусть клиентское приложение будет либо только принимать, 
#либо только отправлять сообщения в общий чат. Эти функции надо реализовать в рамках отдельных скриптов.
#python server.py -a 127.0.0.1 -p 8888

from socket import *
import time

import logging
import sys
import json 
from typing import Any, Dict 
import argparse
import select 
print( 'The server has been started!\n' )

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
				
def handle_authenticate(request) :
    if request['user']=={'account_name':'alex','password':'alex_pwd'}:
        return {"response": 200, "alert": "User alex authorized and authenticated successfully!"}
    else:
        return {"response": 402, "alert": "Error of authentication!"}

def handle_message(request) :
    return {"response": 200, "message": request['message']}

def handle_quit(request) :
    return {"response": 200, "action": "quit"}
		
mapping = {
    'authenticate': handle_authenticate, 
    'msg': handle_message, 
    'quit': handle_quit
}

def handler(request: Dict[str, object]) :
    print('Client sent {request}\n')
    response=mapping[request['action']] (request)
    print(f'Response {response}\n')
    return response 

try :
    server, port = get_args()
    port_number = 8000
    for p in port:
        port_number=int(p)
   
    s = socket(AF_INET, SOCK_STREAM) # Создает сокет TCP
    s.bind(( '' , port_number )) # Присваивает порт 8888
   
    # одновременно обслуживает не более 5 запросов.  19-24'/1h07' -->47'
    num_of_clients = 0
    clients = []
    total_msgs_sent_count = 0
    while True:  
        s.listen( 5 ) # Переходит в режим ожидания запросов;  
        print("1")
        #s.settimeout(0.2) 
        try: 
            if (num_of_clients<=15):
                client, addr = s.accept()
                clients.append(addr)			   
                num_of_clients+=1
            else:
                print( 'List of clients is overlimited' )               
        except StopServerException:
            break	   
        #with client:
        finally: 
            print("2")		
            w = []        
            try:
                r, w, e = select.select([],clients, [], 0)
                print("3")					
            except Exception as e: 
                print('Error:', e.strerror)			
                print (e.Message) #pass #do nothing if a client is disconnected
				
            for s_client in w: 
                timestr = time.ctime(time.time())+"\n"	
                print("4")					
                try:
                    print("5")				
                    data_b = client.recv( 1000000 )
                    data = json.loads(data_b, encoding='utf-8')
                    response = handler(data) 
                    print("6")					
					
                    s_client.send(json.dumps(response).encode('utf-8'))	
                    #s_client.send(timestr.encode('ascii'))				
                    total_msgs_sent_count += 1 
					
                    if (data['action']=='quit') :
                        client.close()
                        break
                except: 
                    clients.remote(s_client)
                    print(f'Client removed, total clients: {len(clients)}')
						


except OSError as e:      
    logging.getLogger( 'app_server.log' ).setLevel(logging.ERROR)       
    log.error('Error:', e.strerror)

