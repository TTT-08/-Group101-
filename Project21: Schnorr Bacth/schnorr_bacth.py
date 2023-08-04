import hashlib
import random

# 常量
p = 2147483647  # 选择一个质数 p (p = 2q + 1，其中 q 也是质数)
q = 1073741823  # p 的一个质数因子
g = 2  # 1 < g < p

# 生成私钥
def generate_private_key():
    return random.randint(1, q)

# 生成公钥
def generate_public_key(private_key):
    return pow(g, private_key, p)

# 生成签名
def generate_signature(message, private_key):
    k = random.randint(1, q)
    r = pow(g, k, p) % q

    message_hash = hashlib.sha256(message.encode()).digest()
    e = int.from_bytes(message_hash, byteorder='big')
    s = (k - private_key * r) % q

    return r, s

# 验证签名
def verify_signature(message, signature, public_key):
    r, s = signature

    if r < 1 or r > q or s < 1 or s > q:
        return False

    message_hash = hashlib.sha256(message.encode()).digest()
    e = int.from_bytes(message_hash, byteorder='big')
    v = pow(g, s, p) * pow(public_key, r, p) % p % q

    return v == r

def tuple_to_int(tuple1, tuple2):
    int_value = (tuple1[0] << 32) + tuple1[1]  # 将第一个二元组转换为 int
    int_value <<= 64  # 左移 64 位，为了给第二个二元组腾出空间
    int_value += (tuple2[0] << 32) + tuple2[1]  # 将第二个二元组转换为 int
    return int_value

# 示例用法
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
