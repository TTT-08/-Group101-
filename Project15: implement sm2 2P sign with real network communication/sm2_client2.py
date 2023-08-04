import socket
import sys
from random import randint
from gmpy2 import invert
import binascii
iv = "7380166F4914B2B9172442D7DA8A0600A96F30BC163138AAE38DEE4DB0FB0E4E"
T = (0x79cc4519, 0x7a879d8a)
index = "0123456789ABCDEF"
W = []
W_ = []
def padding(n, size,s):
    s=list(s)
    s.append('8')
    for i in range(0, n // 4):
        s.append("0")
    s=''.join(s)
    s+=hex(size)[2:].zfill(16).upper()
    return n,s

def LeftShift(num, left):
    return (((num << left)&((1<<32)-1)) | (num >> (32 - left)))

def Ti(x):
    return (T[1]) if x > 15 else (T[0])

def FFi(x, y, z, n):
    return ((x & y) | (y & z) | (x & z)) if n > 15 else (x ^ y ^ z)

def GGi(x, y, z, n):
    return ((x & y) | ((~x) & z)) if n > 15 else (x ^ y ^ z)

def P0(x):
    return (x ^ LeftShift(x, 9) ^ LeftShift(x, 17))

def P1(x):
    return (x ^ LeftShift(x, 15) ^ LeftShift(x, 23))

def Extend(B):
    for i in range(0, 16):
        W.append(int(B[(8 * i):(8 * i) + 8],16)%((1<<32)))

    for i in range(16, 68):
        W.append(int(hex((P1(W[i - 16] ^ W[i - 9] ^ LeftShift(W[i - 3], 15))) ^ (LeftShift(W[i - 13], 7) ^ W[i - 6])),16)%((1<<32)))

    for i in range(0, 64):
        W_.append(int(hex(W[i] ^ W[i + 4]),16)%((1<<32)))

index=['0','1','2','3','4','5','6','7','8','9','A','B','C','D','E','F']
def uint_to_str(num,k = 8) :
    s=""
    for i in range(0,k):
        s+=index[num % 16]
        num//=16
    return  s[::-1]

def update(V, Bi):
    temp = []
    temp1 = []
    for i in range(0, 8):
        t="0x"+V[8 * i: (8 * i) + 8]
        temp.append(int(t,16))
        temp1.append(temp[i])
    for i in range(0, 64):
        SS1 = LeftShift((LeftShift(temp[0], 12) + temp[4] + LeftShift(Ti(i), i % 32))%(1<<32), 7)
        SS2 = (SS1 ^ LeftShift(temp[0], 12))
        t=(FFi(temp[0], temp[1], temp[2], i)+temp[3])%((1<<32))
        TT1 = (FFi(temp[0], temp[1], temp[2], i) + temp[3] + SS2 + W_[i])%(1<<32)
        TT2 = (GGi(temp[4], temp[5], temp[6], i) + temp[7] + SS1 + W[i])%(1<<32)
        temp[3] = temp[2]
        temp[2] = (LeftShift(temp[1], 9))
        temp[1] = temp[0]
        temp[0] = TT1
        temp[7] = temp[6]
        temp[6] = LeftShift(temp[5], 19)
        temp[5] = temp[4]
        temp[4] = P0(TT2)
    result = ""
    for i in range(0, 8):
        result += uint_to_str(temp1[i] ^ temp[i])
    return result.upper()

def Hash(m):
    size = len(m) * 4
    num = (size + 1) % 512
    t = 448 - num if num < 448 else 960 - num
    k ,m= padding(t,size,m)
    t=len(m)
    group_number = (size + 65 + k) // 512
    B = []
    IV = []
    IV.append(iv)
    for i in range(0, group_number):
        B.append(m[128 * i:128 * i + 128])
        Extend(B[i])
        IV.append(update(IV[i], B[i]))
        W.clear()
        W_.clear()
    temp = IV[group_number]
    return temp

def add(x1,y1,x2,y2):
    if x1==x2 and y1==p-y2:
        return False
    if x1!=x2:
        lamda=((y2-y1)*invert(x2-x1, p))%p
    else:
        lamda=(((3*x1*x1+a)%p)*invert(2*y1, p))%p
    x3=(lamda*lamda-x1-x2)%p
    y3=(lamda*(x1-x3)-y1)%p
    return x3,y3

def mul_add(x,y,k):
    k=bin(k)[2:]
    qx,qy=x,y
    for i in range(1,len(k)):
        qx,qy=add(qx, qy, qx, qy)
        if k[i]=='1':
            qx,qy=add(qx, qy, x, y)
    return qx,qy


p=0x8542D69E4C044F18E8B92435BF6FF7DE457283915C45517D722EDB8B08F1DFC3    #256
a=0x787968B4FA32C3FD2417842E73BBFEFF2F3C848B6831D7E0EC65228B3937E498
b=0x63E4C6D3B23B0C849CF84241484BFE48F61D59A5B16BA06E6E12D1DA27C5249A
n=0x8542D69E4C044F18E8B92435BF6FF7DD297720630485628D5AE74EE7C32E79B7
Gx=0x421DEBD61B62EAB6746434EBC3CC315E32220B3BADD50BDC4C4E6C147FEDD43D
Gy=0x0680512BCBB42C07D47349D2153B70C4E5D7FDFCBFA36EA1A85841B9E46E09A2

host = '127.0.0.1'
port=1234
address=(host,port)
s_client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
try:
    s_client.connect(address)
    print("Successfully connected")
except Exception:
    print('Not found or not open')
    sys.exit()
else:
    d1=randint(1,n)
    p1=mul_add(Gx,Gy,invert(d1,p))
    x,y=hex(p1[0]),hex(p1[1])
    s_client.sendto(x.encode('utf-8'),address)

    s_client.sendto(y.encode('utf-8'),address)

    m = "message digest"
    m = hex(int(binascii.b2a_hex(m.encode()).decode(), 16)).upper()[2:]
    IDa = "ALICE123@YAHOO.COM"
    ida = hex(int(binascii.b2a_hex(IDa.encode()).decode(), 16)).upper()[2:]
    ENTLa = '{:04X}'.format(len(ida) * 4)
    ma = ENTLa + ida + '{:064X}'.format(a) + '{:064X}'.format(b) + '{:064X}'.format(Gx) + '{:064X}'.format(Gy)
    Za = Hash(ma)
    e=Hash(ma+m)
    k1=randint(1,n)
    Q1=mul_add(Gx,Gy,k1)
    x,y=hex(Q1[0]),hex(Q1[1])
    s_client.sendto(x.encode('utf-8'),address)

    s_client.sendto(y.encode('utf-8'),address)

    s_client.sendto(e.encode('utf-8'),address)

    r,address=s_client.recvfrom(1024)
    r=int(r.decode(),16)

    s2,address=s_client.recvfrom(1024)
    s2=int(s2.decode(),16)

    s3,address=s_client.recvfrom(1024)
    s3=int(s3.decode(),16)
    s=((d1*k1)*s2+d1*s3-r)%n
    print((hex(r),hex(s)))
    s_client.close()