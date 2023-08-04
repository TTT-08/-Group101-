import random

# 椭圆曲线参数
a = 2
b = 2
p = 17
x = 5
y = 1
g = [x, y]
n = 19

def compute_cd(a, b):
    r = a % b
    while r != 0:
        a, b = b, r
        r = a % b
    return b

def compute_xgcd(a, m):
    if compute_cd(a, m) != 1:
        return None
    u1, u2, u3 = 1, 0, a
    v1, v2, v3 = 0, 1, m
    while v3 != 0:
        q = u3 // v3
        v1, v2, v3, u1, u2, u3 = (u1 - q * v1), (u2 - q * v2), (u3 - q * v3), v1, v2, v3
    return u1 % m

def compute_the_epoint_add(P, Q):
    if P == 0:
        return Q
    if Q == 0:
        return P
    if P == Q:
        t1 = (3 * (P[0]**2) + a)
        t2 = compute_xgcd(2 * P[1], p)
        k = (t1 * t2) % p
    else:
        t1 = (P[1] - Q[1])
        t2 = (P[0] - Q[0])
        k = (t1 * compute_xgcd(t2, p)) % p

    X = (k * k - P[0] - Q[0]) % p
    Y = (k * (P[0] - X) - P[1]) % p
    Z = [X, Y]
    return Z

def compute_the_epoint_mul(k, g):
    if k == 0:
        return 0
    if k == 1:
        return g
    r = g
    while k >= 2:
        r = compute_the_epoint_add(r, g)
        k = k - 1
    return r

def hash_the_message(message):
    return sum([ord(c) for c in message]) % n

def signature_message(m, d, n, g):
    k = random.randint(1, n - 1)
    Z = compute_the_epoint_mul(k, g)
    r = Z[0] % n
    e = hash_the_message(m)
    s = (compute_xgcd(k, n) * (e + d * r)) % n
    return r, s

def verify_message(r, s, m, pk, n, g):
    e = hash_the_message(m)
    t = compute_xgcd(s, n)
    Z = compute_the_epoint_add(compute_the_epoint_mul((e * t) % n, g), compute_the_epoint_mul((r * t) % n, pk))
    return Z != 0 and Z[0] % n == r

def attack_the_signature(e, r, s, n, g, pk):
    t = compute_xgcd(s, n)
    Z = compute_the_epoint_add(compute_the_epoint_mul((e * t) % n, g), compute_the_epoint_mul((r * t) % n, pk))
    return Z != 0 and Z[0] % n == r

def to_forge_signature(r, s, n, g, pk):
    a = random.randint(1, n - 1)
    b = random.randint(1, n - 1)
    Z = compute_the_epoint_add(compute_the_epoint_mul(a, g), compute_the_epoint_mul(b, pk))
    r1 = Z[0] % n
    e1 = (r1 * a * compute_xgcd(b, n)) % n
    s1 = (r1 * compute_xgcd(b, n)) % n
    print('伪造的信息', e1)
    print('伪造的签名', r1, s1)
    if attack_the_signature(e1, r1, s1, n, g, pk):
        print('成功伪造！！！！')
    else:
        print('无法伪造')

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
