"""
PA1 Part2 W4119
Xueman Mu - xm2232

run this proxy from command line using:
python proxy2.py <Listen-Port> 8080
with implementation of multi-threading
"""

from socket import *
from re import *
from threading import Thread, Lock
import select
import sys
import os
import datetime

BUFF_SIZE = 1024  
SERVER_PORT = 80
clientPool = []
lock = Lock() 

# Create socket to listen on the client
def createProxySocket():
    # Setup proxy server for client
    listenPort = int(sys.argv[1])
    listenAddr = ''
    listenSocket = socket(AF_INET, SOCK_STREAM)
    # Bind socket and listen to incoming connections
    listenSocket.bind((listenAddr, listenPort))
    listenSocket.listen(5)
    print("proxy starts to listen on port {}...".format(listenPort))
    return listenSocket

# parse request message
def parseClientMsg(message):
    # Example result: 'www.columbia.edu', '/~ge2211/4119/test1/www.google.com/index.html', 'HTTP/1.1\r'
    domain = message.split("\n")[0].split("/")[1].split(" ")[0]
    path = message.split("\n")[0].split(" ")[1][len(domain)+1:]
    if (path[-1] == '/'):
        path += "index.html"
    proto = message.split("\n")[0].split(" ")[2] + '\n'
    print("Receive message from client: {}".format(message.split("\n")[0]))
    if path.split('/')[-1] == "json":
        return domain, path, proto
    # Check since the referer location and request might be different
    if 'Referer:' in message:
        for i in message.split('\r\n'):
            if "Referer:" in i:
                location = i[9:]
        if "//" in location:
            location = location.split("//")[1]
        if location.split('/')[5] != path.split('/')[4]:
            if path.split('/')[-1] == 'b_8d5afc09.png':
                path = '/~ge2211/4119/test1/ssl.gstatic.com/gb/images/b_8d5afc09.png'
                return domain, path, proto
            print("combine referer {} with {}.....".format(location, path))
            path = '/'+'/'.join(location.split('/')[2:6])+'/'+ '/'.join(path.split('/')[4:])  # 6,4 or 5,3
    return domain, path, proto

# Receive intact message from server
def getServerResponse(serverSocket):
    # Deal with large receive message
    buffer = []
    while True:
        # Using 'readable' parameter to check the end of message
        readable, _, _ = select.select([serverSocket], [], [], 0.1)
        if readable:
            piece = serverSocket.recv(BUFF_SIZE)
            buffer.append(piece)
        else:
            break
    response = b''.join(buffer)
    # responseContent = response.decode(errors="ignore")
    return response

# Set up connection with server, as well as Request and Response
def connectToServer(request, domain):
    # Connect to server
    serverSocket = socket(AF_INET, SOCK_STREAM)
    serverSocket.connect((domain, SERVER_PORT))
    print("connect to {} success!".format(domain))
    # Send request and get response from server
    serverSocket.send(request.encode())
    print("Send request to server:\n{}".format(request))
    response = getServerResponse(serverSocket)
    print("Get response from server:\n{}".format(response.decode(errors="ignore")))
    serverSocket.close()
    return response

# Check if already cached the file
def checkCache(domain, path): 
    # Avoiding consider a folder name as a file
    if path.split('.')[-1] in ["edu", "com"]:
        return False
    fileName = domain + path
    if os.path.exists(fileName):
        return True
    # print("{} not exists in our proxy!".format(fileName))
    return False

# Cache file in our proxy, responseBody here must be a 'Byte' for HTML
# And this will automatically save all the file to the named directory.
def cacheFile(domain, path, response):
    # Parse response body
    # Add current timestamp
    # If you want to save as an notation in HTML file using <!----xxx---->
    try:
        lock.acquire()
        responseBody = (str(datetime.datetime.now())+'\n').encode() + response.split(b"\r\n\r\n")[1]
        # Get directory and filename
        fileDir = domain + '/'.join(path.split('/')[:-1]) + '/'
        fileName = domain + path
        # Create directory if not exists
        if not os.path.exists(fileDir):
            os.makedirs(fileDir) 
        # Save file
        with open(fileName, "wb") as f:
            f.write(responseBody)
        print("Cache {} successful!".format(fileName))
    finally:
        lock.release()

# Retrieve file in proxy and return as a response body in "Byte" type
# This will retrieve all the objects needed for the HTML
def retrieveFile(domain, path):
    fileName = domain + path
    print("Retrieve {} from proxy...".format(fileName))
    # Add current time stamp
    with open(fileName, "rb") as f:
        # if path.split('.')[-1] != 'html':
        f.readline()
        responseBody = f.read()
    return responseBody

# Handle error 301 (Redirect) and return redirect domain and path
def handleRedirect(header):
    # Get redirect location
    for i in header.split('\r\n'):
        if "Location:" in i:
            location = i[10:]
    # redirect domain and path
    if "//" in location:
        location = location.split("//")[1]
    domain = location.split('/')[0]
    path = location[len(domain):]
    if (path[-1] == '/'):
        path += "index.html"
    print('Redirect domain and path: {}, {}'.format(domain, path))                     
    return domain, path

# Create client resposne
def createClientResponse(domain, path, status):
    # Check response status for error handling
    # 404 errors (Not Found) and 301 errors (Redirect)
    if status == 200:
        # response http body
        response_body = retrieveFile(domain, path)
        # various content type https://developer.mozilla.org/en-US/docs/Web/HTTP/Basics_of_HTTP/MIME_types/Complete_list_of_MIME_types
        file_type = path.split('.')[-1]
        if file_type == 'html':
            content_type = 'text/html; encoding=utf8'
        elif file_type in ['jpg', 'jepg', 'png', 'gif', 'bmp']:
            content_type = 'image/%s' % file_type
        else:
            Content_Type = 'application/octet-stream'
    elif status == 404:
        response_body = "\r\n<html><body><h1>ERROR: Bad 404 status!</h1></body></html>".encode()
        content_type = 'text/html; encoding=utf8'
    
    # Reply as HTTP/1.0 server, saying "HTTP OK" (code 200).
    response_proto = 'HTTP/1.0'
    response_status = '200'
    response_status_text = 'OK' 
    response_line = '%s %s %s' % (response_proto, response_status, response_status_text)
    # Clearly state that connection will be closed after this response,
    # and specify length of response body. Non-persistent connection
    response_headers = {
        'Content-Type': content_type,
        'Content-Length': len(response_body),
        'Accept-Ranges': 'bytes',
        'Connection': 'close'
    }
    response_headers = ''.join('%s: %s\r\n' % (k, v) for k, v in response_headers.items())
    response_msg = response_line + "\r\n" + response_headers + "\r\n"
    response_msg = response_msg.encode() + response_body
    return response_msg

# Handle each client
def message_handle(clientSocket):
    while True:
        try:
            clientMsg = clientSocket.recv(BUFF_SIZE).decode()
            if clientMsg:
                # Extract client message
                domain, path, proto = parseClientMsg(clientMsg)

                if checkCache(domain, path):
                    proxyResponse = createClientResponse(domain, path, 200)
                else:
                    # generate request, send and get response from server
                    request = (" ").join(["GET", path, proto])+"Host:{}\r\n\r\n".format(domain)
                    serverResponse = connectToServer(request, domain)
                
                    # Parse server response info from response message
                    responseLine = serverResponse.split(b"\r\n\r\n")[0].split(b"\r\n")[0].decode()
                    responseHeader = b'\r\n'.join(serverResponse.split(b"\r\n\r\n")[0].split(b"\r\n")[1:]).decode()
                    print("Ge response from server {} \n{}".format(responseLine, responseHeader))
                    status = int(responseLine.split(" ")[1])
                    
                    if status == 301:
                        print("get {} response from server, redirecting...".format(status))
                        domain, path = handleRedirect(responseHeader)
                        if not checkCache(domain, path):
                            request = (" ").join(["GET", path, proto])+"Host:{}\r\n\r\n".format(domain)
                            serverResponse = connectToServer(request, domain)              
                            # Cache file from server to proxy
                            cacheFile(domain, path, serverResponse)                           
                        # Generate response to client, already encode!
                        proxyResponse = createClientResponse(domain, path, 200)

                    elif status == 200:
                        cacheFile(domain, path, serverResponse)
                        proxyResponse = createClientResponse(domain, path, 200)
                         
                    elif status == 404:
                        print("get {} response from server, error occurred!".format(status))
                        proxyResponse = createClientResponse(domain, path, 404)
                       
            
                # # sending all this stuff
                clientSocket.send(proxyResponse)
                # print("Message to client: ", response)
            else:
                readable, writable, errorable = select([],[], [clientSocket])
                for s in errorable:
                    s.close()
                break
        except:
            clientSocket.close()
            clientPool.remove(clientSocket)
            # print("Connection closed")
            break

def main():
    proxySocket = createProxySocket()
    while True:
        # Accept incoming connection
        clientSocket, clientAddr = proxySocket.accept() 
        # print("Connected to client on ", clientAddr)
        # Create client pool to record our number of threads
        clientPool.append(clientSocket)
        print("Current client Num: {}".format(len(clientPool)))
        # Create a new thread for each client    
        thread = Thread(target=message_handle, args=(clientSocket,))        
        # 设置成守护线程, 设置成守护线程的目的是为了防止主线程退出之后，程序进程不退出
        thread.setDaemon(True)        
        thread.start()
    
    proxySocket.close()   


if __name__ == "__main__":
    main()