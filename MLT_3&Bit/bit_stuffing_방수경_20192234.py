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
    print(''.join(result))

if __name__ == "__main__":
    main()