from socket import *
from select import *
import sys
from time import ctime
#Reciever를 먼저 실행해야 합니다.
HOST = '127.0.0.1'
PORT = 10000
BUFSIZE = 1024
ADDR = (HOST,PORT)

clientSocket = socket(AF_INET, SOCK_STREAM)

while(True):
    i = 0
    try:
        clientSocket.connect(ADDR)
        a = input("보낼 data 입력 : ")
        print("application에서 data가 왔다!")
        print("packet을 만들어 보내자!")
        while(True): 
            if (i == len(a)): break
            clientSocket.send(a[i].encode())	
            i = i+1
        
    except  Exception as e:
        sys.exit()
    print('End')