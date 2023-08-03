import math
import random
import base64
from gmssl import sm2, sm4
from gmssl.sm4 import CryptSM4, SM4_ENCRYPT, SM4_DECRYPT

curve_params = {
    "p": 0xFFFFFFFEFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF00000000FFFFFFFFFFFFFFFF,
    "a": 0xFFFFFFFEFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF00000000FFFFFFFFFFFFFFFC,
    "b": 0x28E9FA9E9D9F5E344D5A9E4BCF6509A7F39789F515AB8F92DDBCBD414D940E93,
    "n": 0xFFFFFFFEFFFFFFFFFFFFFFFFFFFFFFFF7203DF6B21C6052B53BBF40939D54123,
    "x": 0x32C4AE2C1F1981195F9904466A39C9948FE30BBFF2660BE1715A4589334C74C7,
    "y": 0xBC3736A2F4F6779C59BDCEE36B692153D0A9877CC62A474002DF32E52139F0A0,
}

def epoint_mod(a, n):
    return float('inf') if math.isinf(a) else a % n

def epoint_modmult(a, b, n):
    t = bin(n - 2)[2:]
    y = 1
    for bit in t:
        y = (y ** 2) % n
        if bit == '1':
            y = (y * b) % n
    return (y * a) % n

def epoint_add(P, Q, a, p):
    inf = float('inf')
    if (math.isinf(P[0]) or math.isinf(P[1])) and (~math.isinf(Q[0]) and ~math.isinf(Q[1])):
        return Q
    elif (~math.isinf(P[0]) and ~math.isinf(P[1])) and (math.isinf(Q[0]) or math.isinf(Q[1])):
        return P
    elif (math.isinf(P[0]) or math.isinf(P[1])) and (math.isinf(Q[0]) or math.isinf(Q[1])):
        return [inf, inf]
    l = epoint_modmult(Q[1] - P[1], Q[0] - P[0], p) if P != Q else epoint_modmult(3 * P[0] ** 2 + a, 2 * P[1], p)
    X = epoint_mod(l ** 2 - P[0] - Q[0], p)
    Y = epoint_mod(l * (P[0] - X) - P[1], p)
    return [X, Y]

def epoint_mult(k, P, a, p):
    tmp = bin(k)[2:]
    l = len(tmp) - 1
    Z = P
    if l > 0:
        k = k - 2 ** l
        while l > 0:
            Z = epoint_add(Z, Z, a, p)
            l -= 1
        if k > 0:
            Z = epoint_add(Z, epoint_mult(k, P, a, p), a, p)
    return Z

def generate_key(a, p, n, G):
    n = curve_params["n"]
    d = random.randint(1, n - 2)
    k = epoint_mult(d, G, a, p)
    return d, k

def sm2_pgp_encryption(message, key):
    # Padding
    l = 16
    n = len(message)
    num = l - (n % l) if n % l != 0 else 0
    message = message + ('\0' * num)

    # 转换为字节类型
    message = str.encode(message)
    key = str.encode(key)

    # 输出消息和密钥的十六进制表示
    print("信息：", base64.b16encode(message))
    print("密钥：", base64.b16encode(key))

    # 使用SM4对消息进行加密
    SM4 = CryptSM4()
    SM4.set_key(key, SM4_ENCRYPT)
    c1 = SM4.crypt_ecb(message)

    # 使用SM2对密钥进行加密
    c2 = sm2_crypt.encrypt(key)
    print("加密信息：", base64.b16encode(c1))
    print("加密密钥：", base64.b16encode(c2))

    return c1, c2


# PGP解密
def sm2_pgp_decryption(c1, c2):
    # 使用SM2对密钥进行解密
    k = sm2_crypt.decrypt(c2)

    # 使用SM4对消息进行解密
    SM4 = CryptSM4()
    SM4.set_key(k, SM4_DECRYPT)
    m = SM4.crypt_ecb(c1)

    # 输出解密后的密钥和消息
    print("解密密钥：", base64.b16encode(k))
    print("解密信息", base64.b16encode(m))


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