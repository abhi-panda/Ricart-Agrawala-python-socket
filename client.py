###################################################################
# Author : Abhishek Panda
# Created Date : 3rd November 2021
# Description : Python Socket programming to simulate 
# Distributed system and show the implementation of 
# Ricart-Agrawala algorithm without any enhancements.
# File : client.py [Process]
###################################################################


import socket
import errno
import sys
import uuid
from datetime import datetime
import time
import pickle

REPLY_MESSAGE = 2
REQUEST_MESSAGE = 1
SENT_REQUEST_MESSAGE = 3
EXEC_MESSAGE = 4
IP = socket.gethostbyname(socket.gethostname())
PORT = 5050
HEADER_LENGTH = 10
CS_EXECUTION_TIME = 30
selfProcessID = str(uuid.uuid1())
selfCreatedts = f"{int(round((datetime.now()).timestamp()))}"
repdi = []
reqdi = []
reqdi_count = 0
executingCS = False
requestedCS = False
requestedCStime = 0 
executedCS = False

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

client_socket.connect((IP, PORT))
client_socket.setblocking(False)
intro={'processID': selfProcessID,'createdts': selfCreatedts}
intro_header = f"{len(pickle.dumps(intro)):<{HEADER_LENGTH}}".encode('utf-8')
client_socket.send(intro_header + pickle.dumps(intro))

def logicalClock():
    now = datetime.now()
    seconds_since_midnight = (now - now.replace(hour=0, minute=0, second=0, microsecond=0)).total_seconds()
    logicalClock = int(seconds_since_midnight/15)
    return logicalClock

def executeCS():
    try : 
        global requestedCS
        global executingCS
        executingCS = True
        requestedCS = False
        reqdi.clear()
        print (f"self : {selfProcessID} : executing CS... at {logicalClock()}")
        time.sleep(CS_EXECUTION_TIME)
        print (f"self : {selfProcessID} : exiting CS... at {logicalClock()}")
        executingCS = False
        return True
    except Exception as e :
        return False


def receive_message():

    try:
        # Receive our "header" containing message length, it's size is defined and constant
        message_header = client_socket.recv(HEADER_LENGTH)

        if len(message_header) == 0:
            return False

        message_length = int(message_header.decode('utf-8').strip())
        data = pickle.loads(client_socket.recv(message_length))
        # Return an object of message header and message data
        return data

    except:
        return False

while True:
    ip = input(f'Type 1 to request entry to CS or Press Enter to check/update proceedings => ')
    if ip and int(ip.strip()) == REQUEST_MESSAGE and not requestedCS:
        print (f"Requesting Entry at Logical Timestamp : {str(logicalClock())}")
        msg = {'sentFrom': selfProcessID, 'messageType': REQUEST_MESSAGE,'timestamp': logicalClock(), 'createdts': selfCreatedts}
        requestedCStime = msg['timestamp']
        requestedCS = True
        msg_header = f"{len(pickle.dumps(msg)):<{HEADER_LENGTH}}".encode('utf-8')
        client_socket.send(msg_header + pickle.dumps(msg))
    try:
        while True:
            if executedCS:
                print(f"Sending Replies from the RDi after CS execution")
                for rep in repdi:
                    print(f"self : {selfProcessID} --> {rep['sentFrom']}")
                    repdi_msq= {'messageType': REPLY_MESSAGE, 'sentTo': rep['sentFrom']}
                    repdi_msq_header = f"{len(pickle.dumps(repdi_msq)):<{HEADER_LENGTH}}".encode('utf-8')
                    client_socket.send(repdi_msq_header + pickle.dumps(repdi_msq))
                repdi.clear()
                executedCS = False
            servmsg = receive_message()

            if servmsg is False:
                print('Didnt Receive Anything')
                raise RuntimeError() 
                

            if int(servmsg['messageType']) == REQUEST_MESSAGE:
                if executingCS:
                    for rep in repdi:
                        if rep['sentFrom'] == servmsg['sentFrom']:
                            print (f"Request from {rep['sentFrom']} already in RDi")
                            raise RuntimeError()
                    repdi.append(servmsg)
                    print(f"Appending to RDi as this process({selfProcessID}) is executing CS")
                else:
                    if requestedCS and (selfCreatedts > servmsg['createdts'] or servmsg['timestamp'] < requestedCStime):
                        repdi.append(servmsg)
                        print(f"Appending to RDi as this process({selfProcessID}) has more priority")
                    else:
                        print(f"Sending reply to {servmsg['sentFrom']} for its Request sent at {servmsg['timestamp']}")
                        rep_msq= {'messageType': REPLY_MESSAGE, 'sentTo': servmsg['sentFrom']}
                        rep_msq_header = f"{len(pickle.dumps(rep_msq)):<{HEADER_LENGTH}}".encode('utf-8')
                        client_socket.send(rep_msq_header + pickle.dumps(rep_msq))
            
            if int(servmsg['messageType']) == SENT_REQUEST_MESSAGE:
                print(f"Request sent to {servmsg['sentCount']} from {selfProcessID}")
                reqdi_count=servmsg['sentCount']
            
            if int(servmsg['messageType']) == REPLY_MESSAGE:
                print(f"Replies recieved at {selfProcessID}")
                reqdi.append(servmsg)
                print (reqdi_count, len(reqdi), reqdi)
                if reqdi_count == len(reqdi):
                    print("Replies recieved from : "+str(reqdi_count)+" process(es)")
                    reqdi_count -= len(reqdi)
                    if (reqdi_count == 0):
                        exec_msq= {'messageType': EXEC_MESSAGE, 'sentFrom': selfProcessID, 'timestamp': logicalClock()}
                        exec_msq_header = f"{len(pickle.dumps(exec_msq)):<{HEADER_LENGTH}}".encode('utf-8')
                        client_socket.send(exec_msq_header + pickle.dumps(exec_msq))
                        ecs = executeCS()
                        if ecs and len(repdi) > 0:
                            executedCS = True
                            
            if int(servmsg['messageType']) == EXEC_MESSAGE:
                print(f"{servmsg['sentFrom']} is executing CS at logical time {servmsg['timestamp']}")

    except IOError as e:
        if e.errno != errno.EAGAIN and e.errno != errno.EWOULDBLOCK:
            print('Reading error: {}'.format(str(e)))
            sys.exit()

        # We just did not receive anything
        continue
    except RuntimeError as e:
        continue

    except Exception as e:
        # Any other exception - something happened, exit
        print('Reading error: '.format(str(e)))
        sys.exit()
