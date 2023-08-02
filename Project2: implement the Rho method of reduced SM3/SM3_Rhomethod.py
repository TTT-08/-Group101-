import random
import string
import math
import time
from SM3 import *
from collections import Counter

def rho_attack():
    random_value = []  # 存储已生成的随机值
    for i in range(pow(2, 6)):
        r = random.randint(0, pow(2, 64))  # 生成64位的随机数
        m = padding(str(r))  # 对随机数进行填充
        M = block(m)  # 将填充后的消息切分成128位块
        Mn = SM3(M)  # 对消息进行哈希运算
        tmp = ""
        for k in Mn:
            tmp += hex(k)[2:]  # 将哈希结果转换为十六进制字符串

        t = tmp[:1]  # 提取哈希结果的第一个字节
        if (t in random_value):  # 判断该字节是否在已生成的随机值列表中出现过
            print("Rho攻击成功!\n")
            print("碰撞对应的哈希值为：")
            print(tmp)
            break
        else:
            random_value.append(t)


start = time.time()
rho_attack()  # 执行Rho攻击
end = time.time()
print("运行时间：%.3fs" % (end - start))  # 打印运行时间