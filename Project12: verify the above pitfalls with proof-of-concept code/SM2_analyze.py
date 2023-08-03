from gmssl import sm3, func
import secrets

def inv(a, n):
    def ext_gcd(a, b, arr):
        if b == 0:
            arr[0] = 1
            arr[1] = 0
            return a
        g = ext_gcd(b, a % b, arr)
        t = arr[0]
        arr[0] = arr[1]
        arr[1] = t - int(a / b) * arr[1]
        return g

    arr = [0, 1, ]
    gcd = ext_gcd(a, n, arr)
    if gcd == 1:
        return (arr[0] % n + n) % n
    else:
        return -1


# 椭圆曲线加法
def EC_add(p, q):
    # 0 means inf
    if p == 0 and q == 0:
        return 0  # 0 + 0 = 0
    elif p == 0:
        return q  # 0 + q = q
    elif q == 0:
        return p  # p + 0 = p
    else:
        if p[0] == q[0]:
            if (p[1] + q[1]) % P == 0:
                return 0  # mutually inverse
            elif p[1] == q[1]:
                return EC_double(p)
        elif p[0] > q[0]:  # swap if px > qx
            tmp = p
            p = q
            q = tmp
        r = []
        slope = (q[1] - p[1]) * inv(q[0] - p[0], P) % P  # 斜率
        r.append((slope ** 2 - p[0] - q[0]) % P)
        r.append((slope * (p[0] - r[0]) - p[1]) % P)
        return (r[0], r[1])

def EC_inv(p):
    """椭圆曲线逆元"""
    r = [p[0]]
    r.append(P - p[1])
    return r

# 椭圆曲线减法:p - q
def EC_sub(p, q):
    q_inv = EC_inv(q)
    return EC_add(p, q_inv)

# 自加p+p
def EC_double(p):
    r = []
    slope = (3 * p[0] ** 2 + A) * inv(2 * p[1], P) % P
    r.append((slope ** 2 - 2 * p[0]) % P)
    r.append((slope * (p[0] - r[0]) - p[1]) % P)
    return (r[0], r[1])


# 椭圆曲线多倍点运算
def EC_multi(s, p):
    """
    :param s: 倍数
    :param p: 点
    :return: 运算结果
    """
    n = p
    r = 0
    s_bin = bin(s)[2:]
    s_len = len(s_bin)

    for i in reversed(range(s_len)):  # 类快速幂思想
        if s_bin[i] == '1':
            r = EC_add(r, n)
        n = EC_double(n)

    return r

# 定义椭圆曲线参数、基点和阶
A = 0
B = 7
G_X = 55066263022277343669578718895168534326250603453777594175500187360389116729240
G_Y = 32670510020758816978083085130507043184471273380659243275938904335757337482424
G = (G_X, G_Y)
P = 115792089237316195423570985008687907853269984665640564039457584007908834671663
N = 115792089237316195423570985008687907852837564279074904382605163141518161494337
h = 1

def get_bit_num(x):
    """获得x的比特长度"""
    if isinstance(x, int):  # when int
        num = 0
        tmp = x >> 64
        while tmp:
            num += 64
            tmp >>= 64
        tmp = x >> num >> 8
        while tmp:
            num += 8
            tmp >>= 8
        x >>= num
        while x:
            num += 1
            x >>= 1
        return num
    elif isinstance(x, str):  # when string
        return len(x.encode()) << 3
    elif isinstance(x, bytes):  # when bytes
        return len(x) << 3
    return 0


def precompute(ID, a, b, GX, GY, xA, yA):
    a = str(a)
    b = str(b)
    GX = str(GX)
    GY = str(GY)
    xA = str(xA)
    yA = str(yA)
    ENTL = str(get_bit_num(ID))

    joint = ENTL + ID + a + b + GX + GY + xA + yA
    joint_b = bytes(joint, encoding='utf-8')
    digest = sm3.sm3_hash(func.bytes_to_list(joint_b))
    return int(digest, 16)


# 生成公私钥对
def key_gen():
    sk = int(secrets.token_hex(32), 16)  # private key
    pk = EC_multi(sk, G)  # public key
    return sk, pk


# SM2签名
def sm2_sign(sk, msg, ZA):
    gangM = ZA + msg
    gangM_b = bytes(gangM, encoding='utf-8')
    e = sm3.sm3_hash(func.bytes_to_list(gangM_b))
    e = int(e, 16)  # str -> int
    while 1:
        k = secrets.randbelow(N)  # generate random number k
        a_dot = EC_multi(k, G)  # (x1, y1) = kG
        r = (e + a_dot[0]) % N  # r = (e + x1) % n
        s = 0
        if r != 0 and r + k != N:
            s = (inv(1 + sk, N) * (k - r * sk)) % N
        if s != 0:  return (r, s)


# SM2验签
def sm2_verify(pk, ID, msg, signature):
    r = signature[0]  # r'
    s = signature[1]  # s'
    ZA = precompute(ID, A, B, G_X, G_Y, pk[0], pk[1])
    gangM = str(ZA) + msg
    gangM_b = bytes(gangM, encoding='utf-8')
    e = sm3.sm3_hash(func.bytes_to_list(gangM_b))  # e'
    e = int(e, 16)  # str -> int
    t = (r + s) % N

    dot1 = EC_multi(s, G)
    dot2 = EC_multi(t, pk)
    dot = EC_add(dot1, dot2)  # (x2, y2) = s'G + t'pk

    R = (e + dot[0]) % N  # R = (e' + x2) % N
    return R == r



# 使用sm2签名算法签名
def sm2_sign_and_assign_k(k, sk, msg, ZA):
    M = ZA + msg
    M = bytes(M, encoding='utf-8')
    e = sm3.sm3_hash(func.bytes_to_list(M))
    e = int(e, 16)  # str -> 16进制整型
    a_dot = EC_multi(k, G)  # (x1, y1) = kG
    r = (e + a_dot[0]) % N  # r = (e + x1) % n
    s = 0
    if r != 0 and r + k != N:
        s = (inv(1 + sk, N) * (k - r * sk)) % N
    if s != 0:
        return (r, s)


# 使用ECDSA签名算法签名
def ECDSA_sign_and_assign_k(k, msg, sk):
    R = EC_multi(k, G)
    r = R[0] % N  # Rx mod n
    e = sm3.sm3_hash(func.bytes_to_list(bytes(msg, encoding='utf-8')))  # e = hash(m)
    e = int(e, 16)
    tmp1 = inv(k, N)
    tmp2 = (e + sk * r) % N
    s = tmp1 * tmp2 % N
    return (r, s)


# 【1】k泄露导致d泄露
def sm2_leaking_k():
    """
    A:KeyGen-->(sk_a,pk_a)
       Sign-->Sig_ska(msg)
    """
    ID = 'A'
    msg = "txj"
    sk_a, pk_a = key_gen()
    k = secrets.randbelow(N)  # 泄露的k
    ZA = precompute(ID, A, B, G_X, G_Y, pk_a[0], pk_a[1])
    Sign = sm2_sign_and_assign_k(k, sk_a, msg, str(ZA))
    r, s = Sign
    print("sk_a \t\t\t(private key of A)\t\t", '0x' + hex(sk_a)[2:].rjust(64, '0'))
    print("msg \t\t\t(msg from A)\t\t\t", msg)
    print("Sign_ska_msg\t(A sign msg using sk_a)", Sign)

    """
    B:deduce sk_a from k,Sign
      deduce result: d = (k - s) / (s + r)
    """
    d = (k - s) * inv(s + r, N) % N
    print("d \t\t\t\t(B deduced sk_a)\t\t", '0x' + hex(d)[2:].rjust(64, '0'))
    if d == sk_a:
        print("d=sk_a, B get true sk_a!!!")
    else:
        print("B not get true sk_a")

    """
    B: forge Sign using deduced sk_a(d)
       forge result: Sign_f
       Verify Sign_f using pk_a
    """
    # msg_f是B签名的消息
    msg_f = "not txj"
    print("msg_f\t\t\t(msg for forge from B)\t", msg_f)
    pk_f = EC_multi(d, G)  # d对应的公钥
    ZA_f = precompute(ID, A, B, G_X, G_Y, pk_f[0], pk_f[1])
    Sign_f = sm2_sign(d, msg_f, str(ZA_f))
    print("Sign_f\t\t\t(B Sign msg_f using d)\t", Sign_f)
    print("B Verify using pk_a...")
    if sm2_verify(pk_a, ID, msg_f, Sign_f) == 1:
        print("pass...forge successfully!")
    else:
        print("false...forge unsuccessfully")


# 【2】对不同的消息使用相同的k签名导致d泄露
def sm2_reusing_k():
    """
    A:KeyGen-->(sk_a,pk_a)
       Sign1-->Sig_ska(msg1)
       Sign2-->Sig_ska(msg2)
    """
    sk, pk = key_gen()
    print("sk_a \t\t\t(private key of A)\t\t", '0x' + hex(sk)[2:].rjust(64, '0'))
    msg1 = "sdu"
    msg2 = "txj"
    print("msg1 \t\t\t(msg from A)\t\t\t", msg1)
    print("msg2 \t\t\t(msg from A)\t\t\t", msg2)
    k = secrets.randbelow(N)  # same k
    ID = 'A'
    ZA = precompute(ID, A, B, G_X, G_Y, pk[0], pk[1])
    Sign1 = sm2_sign_and_assign_k(k, sk, msg1, str(ZA))
    Sign2 = sm2_sign_and_assign_k(k, sk, msg2, str(ZA))

    '''
    B: deduce sk_a through msg1,msg2,Sign1,Sign2
       deduce result: d = (s2 - s1) / (s1 - s2 + r1 - r2) mod N
    '''
    r1, s1 = Sign1
    r2, s2 = Sign2
    d = (s2 - s1) * inv((s1 - s2 + r1 - r2), N) % N
    print("d \t\t\t\t(B deduced sk_a)\t\t", '0x' + hex(d)[2:].rjust(64, '0'))
    if d == sk:
        print("d=sk_a, B get true sk_a!!!")
    else:
        print("B not get true sk_a")

    """
        B: forge Sign using deduced sk_a(d)
           forge result: Sign_f
           Verify Sign_f using pk_a
    """
    msg_f = "20000460010"
    print("msg_f\t\t\t(msg for forge from B)\t", msg_f)
    pk_f = EC_multi(d, G)
    ZA_f = precompute(ID, A, B, G_X, G_Y, pk_f[0], pk_f[1])
    Sign_f = sm2_sign(d, msg_f, str(ZA_f))
    print("Sign_f\t\t\t(B Sign msg_f using d)\t", Sign_f)
    print("B Verify using pk_a...")
    if sm2_verify(pk, ID, msg_f, Sign_f) == 1:
        print("pass...forge successfully!")
    else:
        print("false...forge unsuccessfully")


# 【3】两个不同的user使用相同的k,可以相互推测对方的私钥
def same_k_of_different_users():
    # A1和A2使用相同的k签名
    k = secrets.randbelow(N)  # 相同的k值
    """
        A1:KeyGen-->(sk_a1,pk_a1)
           Sign1-->Sig_ska1(msg1)
    """
    sk_a1, pk_a1 = key_gen()
    msg_a1 = "I'm A1"
    ID_a1 = 'A1'
    ZA1 = precompute(ID_a1, A, B, G_X, G_Y, pk_a1[0], pk_a1[1])
    Sign1 = sm2_sign_and_assign_k(k, sk_a1, msg_a1, str(ZA1))
    print("sk_a1 \t\t\t(private key of A1)\t\t", '0x' + hex(sk_a1)[2:].rjust(64, '0'))

    '''
        A2: deduce sk_a1 through msg_a1,Sign1
            deduce result: d1 = (k - s) / (s + r)
    '''
    r1, s1 = Sign1
    d1 = (k - s1) * inv(s1 + r1, N) % N
    print("d1 \t\t\t\t(A2 deduced sk_a)\t\t", '0x' + hex(d1)[2:].rjust(64, '0'))
    if d1 == sk_a1:
        print("d1=sk_a1, A2 get true sk_a1!!!")
    else:
        print("A2 not get true sk_a1")

    """
        A2:KeyGen-->(sk_a2,pk_a2)
           Sign1-->Sig_ska2(msg2)
    """
    sk_a2, pk_a2 = key_gen()
    msg_a2 = "I'm A2"
    ID_a2 = 'A2'
    ZA2 = precompute(ID_a2, A, B, G_X, G_Y, pk_a2[0], pk_a2[1])
    Sign2 = sm2_sign_and_assign_k(k, sk_a2, msg_a2, str(ZA2))
    print("sk_a2 \t\t\t(private key of A2)\t\t", '0x' + hex(sk_a2)[2:].rjust(64, '0'))

    '''
        A1: deduce sk_a2 through msg_a2,Sign2
            deduce result: d2 = (k - s) / (s + r)
    '''
    r2, s2 = Sign2
    d2 = (k - s2) * inv(s2 + r2, N) % N
    print("d2 \t\t\t\t(A1 deduced sk_a)\t\t", '0x' + hex(d2)[2:].rjust(64, '0'))
    if d2 == sk_a2:
        print("d2=sk_a2, A1 get true sk_a2!!!")
    else:
        print("A1 not get true sk_a2")


#【4】 ECDSA与SM2使用相同的d和k导致d泄露
def same_dk_of_ECDSA_SM2():
    # same d and k
    sk, pk = key_gen()
    print("same sk\t\t\t", "0x" + hex(sk)[2:].rjust(64, '0'))
    k = secrets.randbelow(N)
    # ECDSA签名(1)
    message1 = "ECSDA"
    signature1 = ECDSA_sign_and_assign_k(k, message1, sk)
    # SM2签名(2)
    message2 = "sm2"
    ID = 'A'
    ZA = precompute(ID, A, B, G_X, G_Y, pk[0], pk[1])
    signature2 = sm2_sign_and_assign_k(k, sk, message2, str(ZA))

    """
    deduce sk from msg1，msg2，Sign1，Sign2
    deduce result: d = (s1s2 - e1) / (r1 - s1s1 - s1r2)
    """
    r1, s1 = signature1
    r2, s2 = signature2
    e1 = int(sm3.sm3_hash(func.bytes_to_list(bytes(message1, encoding='utf-8'))), 16)
    tmp1 = s1 * s2 - e1 % N
    tmp2 = r1 - s1 * s2 - s1 * r2 % N
    tmp2 = inv(tmp2, N)
    d = tmp1 * tmp2 % N

    print("d (deduced sk)  ", '0x' + hex(d)[2:].rjust(64, '0'))
    if d == sk:
        print("d=sk, get true sk_a!!!")
    else:
        print("not get true sk_a")


if __name__ == '__main__':
    print("k泄露导致d泄露:")
    sm2_leaking_k()
    print("对不同的消息使用相同的k签名导致d泄露:")
    sm2_reusing_k()
    print("两个不同的user使用相同的k,可以相互推测对方的私钥:")
    same_k_of_different_users()
    print("ECDSA与SM2使用相同的d和k导致d泄露:")
    same_dk_of_ECDSA_SM2()