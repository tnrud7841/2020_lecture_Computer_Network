from socket import *
from select import *
#Reciever를 먼저 실행해야 합니다.
HOST = ''
PORT = 10000
BUFSIZE = 1024
ADDR = (HOST, PORT)


serverSocket = socket(AF_INET, SOCK_STREAM)

serverSocket.bind(ADDR)
print('stay')
serverSocket.listen(100)
clientSocket, addr_info = serverSocket.accept()
print('accept')

while(True):
    data = clientSocket.recv(1)
    if not data:  
        break
    print('받은 packet :',data.decode())


clientSocket.close()
serverSocket.close()
print('close')