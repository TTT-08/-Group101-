# Rho攻击
## 1 原理分析
Pollard_rho算法的大致流程是 先判断当前数是否是素数（Miller_rabin）了，如果是则直接返回。 如果不是素数的话，试图找到当前数的一个因子（可以不是质因子）。 然后递归对该因子和约去这个因子的另一个因子进行分解。如下图：

![](https://user-images.githubusercontent.com/104118101/179362361-1d20b4f6-3fb8-4335-b9ba-b65ff1b45056.png)

在攻击SM3的时候，通过生成一系列随机输入，并计算它们的哈希值，然后检查是否存在相同的哈希值（即碰撞）。如果发现碰撞，那么就可以推断出哈希函数存在弱点。

## 2 代码分析
本项目采取的方案是，初始随机选取明文对$m_1,m_2$。

每次迭代，计算$h_1=Hash(m_1),h_2=Hash(Hash(m_2))$。根据$\rho$方法的原理，最终一定可以成环，找到$h_1=h_2$的情况。

考虑到sm3的输出是32字节，我们设置初始状态也是32字节。

关键代码如下：
```
def rho_attack():
    random_value = []  # 存储已生成的随机值
    for i in range(pow(2,6)):
        r = random.randint(0, pow(2,64))  # 生成64位的随机数
        m = padding(str(r))  # 对随机数进行填充
        M = block(m)  # 将填充后的消息切分成128位块
        Mn = SM3(M)  # 对消息进行哈希运算
        tmp=""
        for k in Mn:
            tmp += hex(k)[2:]  # 将哈希结果转换为十六进制字符串
            
        t = tmp[:1]  # 提取哈希结果的第一个字节
        if(t in random_value):  # 判断该字节是否在已生成的随机值列表中出现过
            print("Rho攻击成功!")  # 攻击成功
            print("碰撞对应的哈希值为：")
            print(tmp)
            break
        else:
            random_value.append(t)
```
## 3 运行结果
我们很容易就能找到相应的碰撞：
![](https://img1.imgtp.com/2023/08/02/VfyHNJVi.png)