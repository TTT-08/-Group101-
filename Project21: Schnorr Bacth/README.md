# Schnorr Bacth签名方案
## 1 原理分析
### 1.1 Schnorr签名
根据密码学引论所学：
![](https://img1.imgtp.com/2023/08/04/WL78ecu6.png)
### 1.2 Bacth方法
批量验证（Batch Verification）是密码学领域中的一个概念，用于在一个操作中同时验证多个签名的有效性，以提高效率。在数字签名系统中，批量验证允许同时验证多个签名，而不是逐个验证每个签名，从而减少计算成本。

通常情况下，单独验证每个签名需要执行多个运算，包括点的乘法、加法、哈希等。但通过批量验证，可以将多个签名一起处理，利用并行计算的能力，从而节省时间和计算资源。

在批量验证中，有几种方法可以实现：

- 聚合方案（Aggregate Schemes）：在这种方法中，多个签名可以被聚合成一个单一的签名，然后一次性验证这个聚合签名。这需要特殊的签名方案支持，以及对聚合后签名的验证算法。
- 多签名方案（Multisignature Schemes）：在多签名方案中，多个签名者可以共同生成一个集体签名。验证者只需验证这个集体签名一次，就可以验证多个签名的有效性。
- 向量化验证（Vectorized Verification）：这种方法通过使用向量化操作，一次性验证多个签名。它通常利用CPU或GPU的并行计算能力，以更高效的方式验证签名。
## 2 代码分析
在本project，使用聚合签名的方法验证Schnorr签名。
1. generate_private_key函数：生成一个随机的私钥，范围在1到q之间。
2. generate_public_key函数：通过私钥计算对应的公钥，使用了ElGamal的幂模运算。
3. generate_signature函数：为给定的消息和私钥生成数字签名。
- 随机选择一个k，然后计算r，其中r = g^k mod p % q。
- 计算消息的SHA-256哈希，并将其转换为整数e。
- 计算s，其中s = (k - private_key * r) % q，是签名的一部分。
4. verify_signature函数：验证消息的签名是否有效。
- 对r和s的范围进行检查。
- 计算v，其中v = g^s * public_key^r mod p % q。
- 比较v与r，如果相等，则签名有效。
为了实现聚合签名，我们加密两条信息，并且将两条信息的签名作为一个新的信息进行签名，从而实现一次验证多条签名的目的。
```
private_key1 = generate_private_key()
public_key1 = generate_public_key(private_key1)
private_key2 = generate_private_key()
public_key2 = generate_public_key(private_key2)
private_key = generate_private_key()
public_key = generate_public_key(private_key)

message1 = input("请输入要加密的消息1：")
message2 = input("请输入要加密的消息2：")

signature1 = generate_signature(message1, private_key1)
valid1 = verify_signature(message1, signature1, public_key1)

signature2 = generate_signature(message2, private_key2)
valid2 = verify_signature(message2, signature2, public_key2)

message = str(tuple_to_int(signature1, signature2))

signature = generate_signature(message, private_key)
valid = verify_signature(message, signature, public_key)

print("私钥1:", private_key1)
print("公钥1:", public_key1)
print("签名1:", signature1)
print("签名验证结果1:", valid1)
print("私钥2:", private_key2)
print("公钥2:", public_key2)
print("签名2:", signature2)
print("签名验证结果2:", valid2)
print("1和2签名一起验证结果:", valid)
```
## 3 结果分析
最终成功运行
![](https://img1.imgtp.com/2023/08/04/lRLSvvt5.png)