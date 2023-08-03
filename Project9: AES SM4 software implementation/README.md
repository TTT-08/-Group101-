# 软件实现AES和SM4
## 1 原理介绍
### 1.1AES
AES在上一个project上面已经介绍，并且在密码学引论实验课上有过了具体实现，在这里就不过多介绍了。
### 1.2 SM4
SM4算法是一种分组密码算法，它将数据分成128位（16字节）的块，并使用128位的密钥进行加密和解密。以下是SM4算法的加密和解密过程的概述：

加密过程：
1. 密钥扩展： 将128位的密钥扩展为一系列子密钥，用于加密的不同轮次。

3. 初始轮： 将明文块与第一个子密钥进行异或操作。

5. 多轮迭代： 对初始轮后的数据块进行一系列迭代。每一轮都包括以下步骤：

- Substitution Layer： 通过S盒（Substitution Box）进行字节代换。
- Permutation Layer： 通过固定的线性变换进行置换。
- Key Mixing： 将当前数据块与对应轮次的子密钥进行异或操作。
- 最终轮： 在迭代完成后，将最后一个数据块与最后一个子密钥进行异或操作。
4. 输出： 得到加密后的密文块。

解密过程：

解密过程与加密过程相似，只是子密钥的使用顺序相反，且在每轮中的加解密使用的子密钥是相同的。
## 2 代码实现
### 2.1 AES
具体代码实现解析见PDF
用C和Python分别实现
### 2.2 SM4
在代码中，首先定义了S盒、轮常量FK、轮秘钥CK和初始轮密钥rk等数据。然后，定义了一系列用于实现SM4算法所需的函数，如循环左移、S盒代换、线性L变换、T变换等。最后，在if __name__ == '__main__':中，代码接受用户输入的密钥和明文，使用密钥进行密钥扩展，然后对明文进行加密得到密文。
## 3 运行结果如下
AES-Python实现如下：
![](https://img1.imgtp.com/2023/08/03/F4d5lPSl.png)
AES-C实现如下：
![](https://img1.imgtp.com/2023/08/03/FlvasBAd.png)
SM4-Python实现如下：
![](https://img1.imgtp.com/2023/08/03/vfTTXAuE.png)