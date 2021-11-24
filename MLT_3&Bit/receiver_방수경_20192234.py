def bit_unstuffing(data):
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
    return "".join(map(str, re))

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
    return "".join(map(str, result))

def main():
    data = input()
    result = InvMLT_3(data)
    result = ''.join(result)
    print("MLT-3 알고리즘을 이용하여 0과 1의 bit stream으로 변환 :", result)
    result1 = bit_unstuffing(result)
    print("bit-unstuffing 결과 :", result1)

   

if __name__ == "__main__":
    main()
