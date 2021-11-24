import socket
from threading import *
import time
import random

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = "localhost"
port = 8000
s.bind((host, port))

class client(Thread):
	def __init__(self, socket, address):
		Thread.__init__(self)
		self.sock = socket
		self.addr = address
		self.start()

	def run(self):
		while True:
			bitstring  = str(input("데이터 입력 : "))
			propogationtime = float(input("propogation 시간(초) : "))
			p_nosend = float(input("packet 보낼 확률 : " ))
			l = []
			for i in range(0,1000):
				l = l +[i]

			i = 0
			while i < len(bitstring):
				datadict = {}
				datadict = {i%2 : bitstring[i], }
				sendstring = str(datadict)
				number= random.randint(0,100)
				time1 = time.time()
				if l[number] < (p_nosend*100):
					clientsocket.send(sendstring.encode('utf-8'))
					time.sleep((propogationtime)/1.1)
					time2 = time.time() 
					print("packet 보내기!")
					ackflag= False

				else: 
					time.sleep(propogationtime/1.1)
					time2 = time.time()
					print ("packet 없어짐")
					ackflag= False               

				while True:
					if time2-time1<= propogationtime:  
						time2= time.time()
						clientsocket.settimeout(propogationtime/1.1)
						try:
							recieved = clientsocket.recv(1024).decode()
							print(recieved)
                            
							if recieved:
								i = i+1
								ackflag = True
								break 

						except:
							if time2 - time1 >propogationtime and ackflag == False:
								print ("timeout")

								if l[random.randint(0,100)] < (p_nosend*100):
									clientsocket.send(sendstring.encode('utf-8'))
									time1 = time.time()
									time2 = time.time()
									print("packet 보내기!")

								else: 
									time1 = time.time()
									time2 = time.time()
									print("packet 없어짐!")

            
s.listen(5)
print ('stay')
while (True):

    clientsocket, address = s.accept()
    print("Receiver "+str(address)+" connected")
    client(clientsocket, address)