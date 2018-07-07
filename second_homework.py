lists = range(100)
SALT_KEY=23

def hash(key):
    value_list = [0] * 6
    for index, each in enumerate(key):
        value_list[index%6]+=(ord(each)+index*SALT_KEY)
    for index,i in enumerate(value_list[:-1]):
        if i:
            value_list[index]+=value_list[index+1]

    for index,each in enumerate(value_list):
        for i in range(index):
            value_list[index]+=value_list[i]*(i+1)+SALT_KEY

        value_list[index]%=122
    result=[]
    for i in value_list:
        if 96<i<123 or 64<i<91:
            result.append(chr(i))
        else:
            result.append(str(i%10))
    return ''.join(result)

def main(alist):
    dic={}
    for i in alist:
        if dic.get(i):
            dic[i]=hash(dic[i])

        else:
            dic[i]=hash(i)
        print((i,dic[i]))

alist=['xoo', 'bar', 'boo', 'bar', 'foo']

main(alist)
