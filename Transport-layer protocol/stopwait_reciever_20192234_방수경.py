import socket
import random
from ast import literal_eval

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host ="localhost"
port =8000
s.connect((host,port))

p_noack = float(input("ack가 가지 않을 확률 : "))
count = 0 

def try_ack(previous, current):
    if abs(previous-current) == 1:
        return True
    else:
        return False 

l = []
for i in range(0,100):
    l = l +[i]
output = ""
   
while 2: 
    data=s.recv(8).decode()
    datadict = literal_eval(data)
    index = list((datadict).keys())[0]
    value = datadict.values()
    print("받은 데이터 ", datadict[index])
    number= random.randint(0,100)
    if count == 0:
        count = count +1
        current = index
        previous = 0
        if current == 0:
            previous = 1
    else: 
        count = count +1
        previous = current
        current = index

    if try_ack(previous, current):
        output  = output + list(datadict.values())[0]
        if l[number]<(p_noack*100):
            print ("Ack 잃어버림")
            pass
        else:    
            str="ACK"
            s.send(str.encode())
    else: 
        str="ACK"
        s.send(str.encode())
        print("!!DISCARD!!")

    print("the received bitstring is",output,'\n')

	
s.close ()