###################################################################
# Author : Abhishek Panda
# Created Date : 3rd November 2021
# Description : Python Socket programming to simulate 
# Distributed system and show the implementation of 
# Ricart-Agrawala algorithm without any enhancements.
# File : server.py[helps simulate the peer to peer connection]
###################################################################

import socket
import select
import pickle

REPLY_MESSAGE = 2
REQUEST_MESSAGE = 1
SENT_REQUEST_MESSAGE = 3
EXEC_MESSAGE = 4
IP = socket.gethostbyname(socket.gethostname())
PORT = 5050
HEADER_LENGTH = 10


server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

server_socket.bind((IP, PORT))
server_socket.listen()
sockets_list = [server_socket]
clients = {}

print(f'Listening for connections on {IP}:{PORT}...')


def receive_message(client_socket):

    try:

        message_header = client_socket.recv(HEADER_LENGTH)
        if len(message_header) == 0:
            return False

        message_length = int(message_header.decode('utf-8').strip())
        data = pickle.loads(client_socket.recv(message_length))
        return data

    except:
        return False


while True:
    read_sockets, _, exception_sockets = select.select(sockets_list, [], sockets_list)

    for notified_socket in read_sockets:

        if notified_socket == server_socket:

            client_socket, client_address = server_socket.accept()
            message = receive_message(client_socket)
            if message is False:
                continue

            sockets_list.append(client_socket)
            clients[client_socket] = message

            print('Accepted new connection from {}:{}, Process ID: {}'.format(*client_address, message['processID']))

        else:

            # Receive message
            message = receive_message(notified_socket)

            if message is False:
                print('Closed connection from: {}'.format(clients[notified_socket]['processID']))

                # Remove from list for socket.socket()
                sockets_list.remove(notified_socket)

                # Remove from our list of users
                del clients[notified_socket]

                continue

            processInfo = clients[notified_socket]

            print(
                f'Received message from {processInfo["processID"]}: {message}')

            if int(message["messageType"]) == REQUEST_MESSAGE:
                count = 0
                print(f"Broadcasting Request message from {message['sentFrom']}")
                for client_socket in clients:
                    if client_socket != notified_socket:
                        msg_header = f"{len(pickle.dumps(message)):<{HEADER_LENGTH}}".encode('utf-8')
                        client_socket.send(msg_header + pickle.dumps(message))
                        count += 1
                count_message={'messageType': SENT_REQUEST_MESSAGE, 'sentCount': count}
                count_msg_header = f"{len(pickle.dumps(count_message)):<{HEADER_LENGTH}}".encode('utf-8')
                notified_socket.send(count_msg_header + pickle.dumps(count_message))

            if int(message["messageType"]) == EXEC_MESSAGE:
                print(f"Broadcasting Executing message from {message['sentFrom']}")
                for client_socket in clients:
                    if client_socket != notified_socket:
                        exec_msq_header = f"{len(pickle.dumps(message)):<{HEADER_LENGTH}}".encode('utf-8')
                        client_socket.send(exec_msq_header + pickle.dumps(message))

            if int(message["messageType"]) == REPLY_MESSAGE:
                print(f"Sending REPLY message to {message['sentTo']}")
                for client_socket in clients:
                    info = clients[client_socket]
                    if info["processID"] == message["sentTo"]:
                        rep_msq_header = f"{len(pickle.dumps(message)):<{HEADER_LENGTH}}".encode('utf-8')
                        client_socket.send(rep_msq_header + pickle.dumps(message))

    for notified_socket in exception_sockets:

        # Remove from list for socket.socket()
        sockets_list.remove(notified_socket)

        # Remove from our list of users
        del clients[notified_socket]
