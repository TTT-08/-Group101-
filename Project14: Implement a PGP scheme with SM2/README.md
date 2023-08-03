# SM2应用于PGP
## 1 原理分析
### 1.1 PGP简介
PGP代表"Pretty Good Privacy"，是一种用于加密和签署电子通信的加密软件套件。PGP最初由Philip Zimmermann在1991年开发，旨在提供用户之间安全通信的解决方案，以保护隐私和数据的机密性。它使用非对称加密、对称加密和数字签名等技术来实现安全通信。

PGP在保护电子通信隐私方面发挥了重要作用，尤其是在涉及敏感信息和隐私保护的场景中。然而，随着时间的推移，出现了许多其他加密技术和工具，因此在选择加密方案时需要根据具体情况进行评估。
### 1.2 SM2的PGP实现方法
根据PPT中有关原理的介绍：
![](https://camo.githubusercontent.com/3f30c21917dfbe37a6e4bc375f1d638cb16fca0bcd212011840d42c7829f399d/68747470733a2f2f7a783737372d313331393533353938352e636f732e61702d6265696a696e672e6d7971636c6f75642e636f6d2f32303233303830333230303033302e706e67)
我们可以设计两个模块来实现加密和解密。

调用GMSSL库中封装好的SM2/SM4加解密函数。 加密时使用对称加密算法SM4加密消息，非对称加密算法SM2加密会话密钥； 解密时先使用SM2解密求得会话密钥，再通过SM4和会话密钥求解原消息。
## 2 代码分析
首先导入所需的库：math 用于数学计算，random 用于生成随机数，base64 用于进行Base64编码和解码，gmssl 是一个密码学库，其中包含了 SM2 和 SM4 算法的实现。

为了方便后续操作，定义了一个包含椭圆曲线参数的字典 curve_params，用于存储椭圆曲线的相关参数，并且实现了一些用于椭圆曲线上的点运算的函数：
- epoint_mod：对给定的整数取模，并处理无穷远点的情况。
- epoint_modmult：计算点的倍乘运算，利用了快速幂算法。
- epoint_add：实现点的加法运算，根据点的情况分别处理。
- epoint_mult：计算点的倍乘，同样利用了快速幂算法。

此外定义了具体实现的函数：
- generate_key，用于生成SM2的公钥和私钥
- sm2_pgp_encryption 用于进行SM2和SM4的加密
- sm2_pgp_decryption 用于进行SM2和SM4的解密

主程序代码如下：
```
if __name__ == '__main__':
    d, k = generate_key(curve_params["a"], curve_params["p"], curve_params["n"], [curve_params["x"], curve_params["y"]])
    sk = hex(d)[2:]
    pk = hex(k[0])[2:] + hex(k[1])[2:]
    sm2_crypt = sm2.CryptSM2(public_key=pk, private_key=sk)

    # 加密消息
    m = "txj202100460086"
    k = hex(random.randint(2 ** 127, 2 ** 128))[2:]
    r1, r2 = sm2_pgp_encryption(m, k)

    # 解密消息
    sm2_pgp_decryption(r1, r2)
```
## 3 运行结果
加密消息为txj202100460086
![](https://img1.imgtp.com/2023/08/03/DGxY5scF.png)