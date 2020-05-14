"""
server code sample
Computer Networks Spring 2020

run this from command line:
python server.py
"""          

from socket import *
import sys
import select     
BUFF_SIZE = 1024         

# Create server socket
serverPort = 8888
serverAddr = ''  # localhost

# (domain, type)
# SOCK_STREAM for connection-oriented protocols 
# SOCK_DGRAM for connectionless protocols.
serverSocket = socket(AF_INET, SOCK_STREAM)

# Bind socket and listen to incoming connections
serverSocket.bind((serverAddr, serverPort))
# queue up to 5 requests
serverSocket.listen(5)
print("listening on localhost...")

while True:
    # Accept incoming connection
    clientSocket, clientAddr = serverSocket.accept()  # returns tuple
    print("Connected to client on ", clientAddr)

    while True:
        try:
            message = clientSocket.recv(BUFF_SIZE).decode()
            if message:
                print("Message from client: ", message)
                message = message.upper()
                clientSocket.send(message.encode())
                print("Message to client: ", message)
            else:
                readable, writable, errorable = select([],[], [clientSocket])
                for s in errorable:
                    s.close()
                break
        except:
            clientSocket.close()
            print("Connection closed")
            break

serverSocket.close()    