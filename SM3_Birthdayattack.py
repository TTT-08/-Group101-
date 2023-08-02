import random
import string
import math
import time
from SM3 import *
from collections import Counter

def brithday_attack():
    random_value = []
    r = randomnum(pow(2,16))
    for i in range(pow(2,16)):
        m = padding(str(r[i]))
        M = block(m)
        Mn = SM3(M)
        tmp=""
        for k in Mn:
            tmp += hex(k)[2:]
        random_value.append(tmp[:8])

    collision = dict(Counter(random_value))
    for key,value in collision.items():
        if value > 1:
            print (key)


print("碰撞攻击：")
start = time.time()
brithday_attack()
end = time.time()
print("运行时间:%.3fs"%(end-start))
