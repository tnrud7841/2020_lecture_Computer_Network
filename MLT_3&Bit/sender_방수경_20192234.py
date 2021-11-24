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

def bit_stuffing(data):
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

def main():
    data = input()
    result = bit_stuffing(data)
    result = ''.join(result)
    print("bit-stuffing 결과 :",result)
    result = MLT_3(result)
    print("MLT-3 처리 결과 :",result)

if __name__ == "__main__":
    main()
