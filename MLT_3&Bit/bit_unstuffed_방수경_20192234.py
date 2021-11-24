def bit_unstuffing(data):
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


def main():
    data = []
    data = input()
    result = bit_unstuffing(data)
    print(''.join(result))

if __name__ == "__main__":
    main()