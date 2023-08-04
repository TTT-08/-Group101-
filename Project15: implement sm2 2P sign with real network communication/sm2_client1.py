import socket
from os.path import commonprefix
import threading
from random import randint
from gmpy2 import invert
import time

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


host = ''
port = 1234
address = (host, port)

s_client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s_client.bind(address)

print('begin')
d2=randint(1,n)
x,address = s_client.recvfrom(1024)
x=int(x.decode(),16)

y,address= s_client.recvfrom(1024)
y=int(y.decode(),16)

p1=(x,y)
P=mul_add(p1[0],p1[1],invert(d2,p))
P=add(P[0],P[1],Gx,-Gy)

x,address = s_client.recvfrom(1024)
x=int(x.decode(),16)

y ,address= s_client.recvfrom(1024)
y=int(y.decode(),16)
Q1=(x,y)
e,address=s_client.recvfrom(1024)
e=int(e.decode(),16)

k2=randint(1,n)
k3=randint(1,n)
Q2=mul_add(Gx,Gy,k2)
x1,y1=mul_add(Q1[0],Q1[1],k3)
x1,y1=add(x1,y1,Q2[0],Q2[1])
r=(x1+e)%n
s2=(d2*k3)%n
s3=(d2*(r+k2))%n
s_client.sendto(hex(r).encode(),address)

s_client.sendto(hex(s2).encode(),address)

s_client.sendto(hex(s3).encode(),address)

print("END")