from random import *
import time

def persistent_1():
    while True:
        channel = randint(0,1)
        if(channel==1):
            print("channel busy\n")
            continue
        else:
            print("channel idle\n")
            break

def work(collision,success):
    if(collision==0):
        success=1
    return success

def attemp(k,kmax,success):
    Tp = 3
    abort=0
    while True:
        a = randint(1, 10)
        if(a%2==1):
            collision = 1
        else:
            collision = 0
        success = work(collision,success)
        if(success==0 and collision==0):
            print("working...\n")
            continue
        else:
            if(collision==0):
                print("!success!\n")
                break
            else:
                print("collision detected\n")
                print("send a jamming signal\n")
                if(k>kmax):
                    abort = 1
                    print("!Abort!\n")
                    break
                else:
                    R = Tp * randint(1,pow(2,k)-1)
                    print("wait TB time\n")
                    print(R,"second wait!!\n")
                    print("----------------k  = ",k,"----------------\n")
                    time.sleep(R)
                    break
    return success, abort
    
def simulate(kmax):
    k=0
    print("----------------k = ",k,"----------------\n")
    success=0
    while True:
        persistent_1()
        k=k+1
        success,abort = attemp(k,kmax,success)
        if success==1 or abort==1:
            print("The End\n")
            break

def main():
    kmax = int(input("kmax 값 입력 : "))
    simulate(kmax)

if __name__ == "__main__":
   main()