# 在ECDSA中由签名推公钥
## 1 原理介绍
ECDSA（Elliptic Curve Digital Signature Algorithm）是一种基于椭圆曲线密码学的数字签名算法。它是 DSA（Digital Signature Algorithm）的一个变体，使用了椭圆曲线运算来提供更高的安全性和更小的密钥尺寸。ECDSA 在数字签名、身份验证和数据完整性保护等领域具有广泛的应用。
### 1.1密钥的产生
每个签名者需要产生一个密钥对，包括一个私钥和一个公钥。签名者，假设是Bob，通过以下步骤产生上述两个密钥：

1. 选择随机整数d，d在1到n-1之间

2. 计算Q=dG，得到一个曲线上的解点。

3. Bob的公钥是Q，私钥是d

### 1.2签名产生
1. 选择一条椭圆曲线Ep(a,b)，和基点G；

2. 选择私有密钥k（k<n，n为G的阶），利用基点G计算公开密钥K=kG；

3. 产生一个随机整数r（r<n），计算点R=rG；

4. 将原数据和点R的坐标值x,y作为参数，计算SHA1做为hash，即Hash=SHA1(原数据,x,y)；

5. 计算s≡r - Hash * k (mod n)

6. r和s做为签名值，如果r和s其中一个为0，重新从第3步开始执行
### 1.3签名验证
1. 接受方在收到消息(m)和签名值(r,s)后，进行以下运算

2. 计算：sG+H(m)P=(x1,y1), r1≡ x1 mod p。

3. 验证等式：r1 ≡ r mod p。

4. 如果等式成立，接受签名，否则签名无效。
## 2 代码分析

1. 列表项椭圆曲线参数：
- a_coefficient 和 b_coefficient：椭圆曲线的参数。
- prime_p：有限域的素数，用于定义椭圆曲线的参数。
- order_n：椭圆曲线上的点的阶。
- x_coordinate 和 y_coordinate：基点（生成元）的坐标。
- base_point_G：基点的坐标（椭圆曲线上的一个点）。
2. 椭圆曲线运算函数：

- bool_quadratic_residue(n, p)：检查给定的 n 是否是模素数 p 下的二次剩余。
- solve_quadratic_residue(n, p)：求解模素数 p 下的二次剩余方程。
- modular_inverse(B, N)：计算 B 在模素数 N 下的模反元素。
3. 椭圆曲线点运算函数：

- point_addition(P, Q)：计算两个椭圆曲线上的点 P 和 Q 的相加结果。
- point_doubling(P)：计算椭圆曲线上的点 P 的倍乘结果。
- point_multiplication(k, g)：计算椭圆曲线上的点 g 的 k 倍乘结果。
4. 密钥生成函数：

- generate_key_pair()：生成密钥对，包括私钥和相应的公钥。
5.  数字签名和验证函数：

- sign_message(private_key, message)：使用私钥对消息进行签名。
- deduce_public_key_from_signature(signature, message)：尝试从签名中推导出公钥。
主程序：

生成密钥对，签名消息，并尝试从签名中推导出可能的公钥
## 3 运行结果如下：
最终程序成功运行如下：
![](https://img1.imgtp.com/2023/08/03/AsHzNXmU.png)