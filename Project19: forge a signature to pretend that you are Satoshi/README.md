# 伪造签名
## 1 原理分析
### 1.1 ECDSA签名过程：
1. 密钥生成：
选择一个适当的椭圆曲线及其参数。
随机生成一个私钥（通常是一个随机数），私钥用于生成签名。
通过椭圆曲线上的点乘法计算公钥，公钥将用于验证签名。
2. 消息哈希：
对待签名的消息进行哈希操作，通常使用哈希函数（如SHA-256），得到一个固定长度的哈希值。
3. 签名生成：
使用私钥和哈希值，进行以下计算：
计算一个临时值 k，通常是一个随机数。
计算点 P = k * G，其中 G 是椭圆曲线的基点。
计算 r = x 坐标（P），如果 r = 0，则重新选择 k。
计算 s = k^-1 * (hash + r * 私钥)，其中 hash 是消息的哈希值。
签名由 (r, s) 组成，这是一对整数值。
### 1.2 ECDSA验证过程：
1. 获取公钥和签名：
获取签名者的公钥和签名，这通常与消息一起传递给验证者。
2. 解析签名：
将签名拆分为两个部分：r 和 s。
3. 消息哈希：
对待验证的消息进行相同的哈希操作，得到哈希值。
4. 验证签名：
使用公钥、哈希值、r 和 s 进行以下计算：
计算 w = s^-1 mod n，其中 n 是椭圆曲线的阶（基点 G 重复相加的次数）。
计算 u1 = (hash * w) mod n 和 u2 = (r * w) mod n。
计算点 P = u1 * G + u2 * 公钥。
验证 r 是否等于 P 的 x 坐标的整数部分。
如果 r 相等，则签名有效，消息未被篡改。否则，签名无效。
## 2 代码分析
每个函数的功能和作用：
- compute_cd(a, b): 这个函数计算a和b的最大公约数，并返回结果。
- compute_xgcd(a, m): 该函数计算a关于模m的乘法逆元（如果存在的话）。在
- compute_the_epoint_add(P, Q): 这个函数实现了椭圆曲线上的点加法运算。
- compute_the_epoint_mul(k, g): 该函数实现了椭圆曲线上的点乘法运算，其中k是一个整数，g是给定的基点。
- hash_the_message(message): 这个函数对输入的消息进行哈希处理。
- signature_message(m, d, n, g): 这个函数用于对消息m进行数字签名。
- verify_message(r, s, m, pk, n, g): 该函数用于验证数字签名。
- attack_the_signature(e, r, s, n, g, pk): 这个函数尝试进行伪造攻击，
- to_forge_signature(r, s, n, g, pk): 这个函数试图伪造一个有效的签名，通过生成不同的a和b值，并构造相应的伪造签名，然后检查是否成功进行伪造。

主函数部分：
```
if __name__ == '__main__':
    # 初始化密钥
    d = 7
    pk = compute_the_epoint_mul(d, g)
    m = 'Satoshi'
    r, s = signature_message(m, d, n, g)
    print("初始化签名", r, s)
    if verify_message(r, s, m, pk, n, g):
        print('签名成功!')
    else:
        print('签名失败！')

    to_forge_signature(r, s, n, g, pk)
```
## 3 运行结果
最终成功伪造：
![](https://img1.imgtp.com/2023/08/04/pFcklnAe.png)