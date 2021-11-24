import socket
import time
from random import *
from multiprocessing import Pipe
from threading import Thread

ADDR = ('127.0.0.1', 10000)
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(ADDR)

def Application_layer(up, down):
    a = input("데이터를 입력하세요 : ")
    print("Application : Send a message\n")
    down.send(a)
    msg = down.recv()
    msg = ''.join(msg)
    msg1 = chr(int(msg[0:7],2))
    msg2 = chr(int(msg[7:14],2))
    msg3 = chr(int(msg[14:21],2))
    print("\n*************************")
    print('Receive ACK message : %c%c%c'%(msg1,msg2,msg3))
    print("*************************")

def Transport_layer(up, down):
    msg = up.recv()
    print("Transport : Recieve a message - ",msg)
    packet = msg
    print("Transport : Send a message - ", msg,'\n')
    down.send(packet)
    while True:
        msg = None
        timeout = time.time() + 10
        while time.time() < timeout:
            if down.poll(0.1):
                msg = down.recv()
                print("Transport : Recieve a ACK message - ",msg)
                break
        if msg == None:
            continue
        else:
            up.send(msg)
            print("Transport : Send a ACK message - ",msg)
            break

def Network_layer(up, down):
    msg = up.recv()
    print("Network : Recieve a message - ",msg)
    print("Network : Send a message - ",msg,"\n")
    down.send(msg)
    msg = down.recv()
    print("Network : Recieve a ACK message - ",msg)
    print("Network : Send a ACK message - ",msg,"\n")
    up.send(msg)

def Bit_stuffing(data):
    data = list(data)
    count = 0
    for i in range(0,len(data)):
        if(data[i]=='1'):
            count+=1
        else:
            count = 0 
        if(count==5):
            data[i]= '10'
            count = 0
    return data

def Bit_unstuffing(data):
    data = list(data)
    re = []
    count = 0
    for i in range(0,len(data)):
        if(data[i]=='1'):
            count+=1
            re.append(data[i])
        else:
            if(count != 5):
                count = 0 
                re.append(data[i])
            else:
                count = 0
                continue
    return re

def Persistent_1():
    while True:
        channel = 0
        if(channel==1):
            print("channel busy\n")
            continue
        else:
            print("channel idle")
            break

def Work(collision,success):
    if(collision==0):
        success=1
    return success

def Attemp(k,kmax,success):
    Tp = 0.1
    abort=0
    while True:
        collision = 0
        success = Work(collision,success)
        if(success==0 and collision==0):
            print("working...\n")
            continue
        else:
            if(collision==0):
                print("!success!")
                break
            else:
                print("collision detected\n")
                print("send a jamming signal\n")
                if(k>kmax):
                    abort = 1
                    print("!Abort!\n")
                    break
                else:
                    R = Tp * randint(0,pow(2,k)-1)
                    print("wait TB time\n")
                    print("-------k  = ",k,"-----\n")
                    time.sleep(R)
                    break
    return success, abort
    
def CSMACD_simulate(kmax):
    k=0
    success=0
    while True:
        Persistent_1()
        k=k+1
        success,abort = Attemp(k,kmax,success)
        if success==1 or abort==1:
            break

def Datalink_layer(up, down):
    msg = up.recv()
    print("Datalink : Recieve a message - ",msg)
    msg = Bit_stuffing(msg)
    CSMACD_simulate(kmax=5)
    print("Datalink : Send a message - ",msg,'\n')
    down.send(msg)
    msg = down.recv()
    msg = Bit_unstuffing(msg)
    print("Datalink : Recieve a ACK message - ",msg)
    print("Datalink : Send a ACK message - ",msg,'\n')
    up.send(msg)

def MLT_3(bit_stream):
    n = len(bit_stream)
    result = [] * n
    nonzero = 1
    #At the beginning
    if "0" in bit_stream[0]:
        result.append(0) 
        if (bit_stream[0]=='0' and bit_stream[1]=='1'): result.append(1)
    else: result.append(1)
    #On-running
    for i in range(0,n):
        i=i+1
        if(bit_stream[0]=='0' and bit_stream[1]=='1'): i=i+1
        if i == n: break
        elif "0" in bit_stream[i]: result.append(result[i-1]) 
        else:
            if(result[i-1]==0):
                nonzero = -nonzero
                result.append(nonzero)    
            else: result.append(0)
    #change(1 -> +, -1 -> -)
    b = [] * n
    for i in range(0,len(result)):
        if result[i] == 1: b.append(chr(43))
        elif result[i] == -1: b.append(chr(45))
        else: b.append(0)
    
    return "".join(map(str, b))

def InvMLT_3(bit_stream):
    n = len(bit_stream)
    result = [] * n
    #At the beginning
    if "+" in bit_stream[0]:
        result.append(1) 
    else: result.append(0)
    #On-running
    for i in range(1,n):
        if(bit_stream[i] == bit_stream[i-1]):
            result.append(0)
        else:
            result.append(1)
    result = "".join(map(str, result))
    return ''.join(result)

def Physical_layer(up, down):
    msg = up.recv()
    print("Physical : Recieve a message - ",msg)
    msg = MLT_3(msg)
    down.send(msg.encode())
    print("Physical : Send a message - ",msg,'\n')
    print("--------receicer to sender--------\n")
    msg = down.recv(1024).decode()
    print("Physical : Recieve a ACK message - ",msg)
    msg = InvMLT_3(msg)
    print("Physical : Send a ACK message - ",msg,'\n')
    up.send(msg)

APP_TRANS, TRANS_APP = Pipe()
TRANS_NWK, NWK_TRANS = Pipe()
NWK_DATA, DATA_NWK = Pipe()
DATA_PHY, PHY_DATA = Pipe()

Thread(target=Application_layer, args=(None, APP_TRANS)).start()
Thread(target=Transport_layer, args=(TRANS_APP, TRANS_NWK)).start()
Thread(target=Network_layer, args=(NWK_TRANS, NWK_DATA)).start()
Thread(target=Datalink_layer, args=(DATA_NWK, DATA_PHY)).start()
Thread(target=Physical_layer, args=(PHY_DATA, client_socket)).start()