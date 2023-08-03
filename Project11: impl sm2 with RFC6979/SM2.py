import secrets
from hashlib import sha256
from gmssl import sm3, func

# Elliptic Curve Parameters
Curve_A = 0
Curve_B = 7
Prime_P = 115792089237316195423570985008687907853269984665640564039457584007908834671663
Order_N = 115792089237316195423570985008687907852837564279074904382605163141518161494337
Base_G_X = 55066263022277343669578718895168534326250603453777594175500187360389116729240
Base_G_Y = 32670510020758816978083085130507043184471273380659243275938904335757337482424
Base_G = (Base_G_X, Base_G_Y)

def LegendreSymbol(y, p):
    return pow(y, (p - 1) // 2, p)

def TonelliShanks(y, p):
    assert LegendreSymbol(y, p) == 1
    if p % 4 == 3:
        return pow(y, (p + 1) // 4, p)
    q = p - 1
    s = 0
    while q % 2 == 0:
        q //= 2
        s += 1
    for z in range(2, p):
        if LegendreSymbol(z, p) == p - 1:
            c = pow(z, q, p)
            break
    r = pow(y, (q + 1) // 2, p)
    t = pow(y, q, p)
    m = s
    if t % p == 1:
        return r
    else:
        i = 0
        while t % p != 1:
            temp = pow(t, 2**(i + 1), p)
            i += 1
            if temp % p == 1:
                b = pow(c, 2**(m - i - 1), p)
                r = r * b % p
                c = b * b % p
                t = t * c % p
                m = i
                i = 0
        return r

def extended_euclidean(j, k):
    if j == k:
        return (j, 1, 0)
    else:
        i = 0
        j_array = [j]
        k_array = [k]
        q_array = []
        r_array = []
        prev_r_is_zero = False
        while not (prev_r_is_zero):
            q_array.append(k_array[i] // j_array[i])
            r_array.append(k_array[i] % j_array[i])
            k_array.append(j_array[i])
            j_array.append(r_array[i])
            i += 1
            if r_array[i - 1] == 0:
                prev_r_is_zero = True
        i -= 1
        gcd = j_array[i]
        x_array = [1]
        y_array = [0]
        i -= 1
        total_steps = i
        while i >= 0:
            y_array.append(x_array[total_steps - i])
            x_array.append(y_array[total_steps - i] - q_array[i] * x_array[total_steps - i])
            i -= 1
        return (gcd, x_array[-1], y_array[-1])

def mod_inverse(j, n):
    (gcd, x, y) = extended_euclidean(j, n)
    if gcd == 1:
        return x % n
    else:
        return -1

def elliptic_add(p, q):
    if p == 0 and q == 0:
        return 0
    elif p == 0:
        return q
    elif q == 0:
        return p
    else:
        if p[0] > q[0]:
            p, q = q, p
        r = []
        slope = (q[1] - p[1]) * mod_inverse(q[0] - p[0], Prime_P) % Prime_P
        r.append((slope**2 - p[0] - q[0]) % Prime_P)
        r.append((slope * (p[0] - r[0]) - p[1]) % Prime_P)
        return (r[0], r[1])

def elliptic_double(p):
    r = []
    slope = (3 * p[0]**2 + Curve_A) * mod_inverse(2 * p[1], Prime_P) % Prime_P
    r.append((slope**2 - 2 * p[0]) % Prime_P)
    r.append((slope * (p[0] - r[0]) - p[1]) % Prime_P)
    return (r[0], r[1])

def elliptic_multiply(s, p):
    n = p
    r = 0
    s_binary = bin(s)[2:]
    s_length = len(s_binary)
    for i in reversed(range(s_length)):
        if s_binary[i] == '1':
            r = elliptic_add(r, n)
        n = elliptic_double(n)
    return r

def get_bit_length(x):
    if isinstance(x, int):
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
    elif isinstance(x, str):
        return len(x.encode()) << 3
    elif isinstance(x, bytes):
        return len(x) << 3
    return 0

def precompute(ID, a, b, G_X, G_Y, x_A, y_A):
    a = str(a)
    b = str(b)
    G_X = str(G_X)
    G_Y = str(G_Y)
    x_A = str(x_A)
    y_A = str(y_A)
    ENTL = str(get_bit_length(ID))
    joint = ENTL + ID + a + b + G_X + G_Y + x_A + y_A
    joint_b = bytes(joint, encoding='utf-8')
    digest = sm3.sm3_hash(func.bytes_to_list(joint_b))
    return int(digest, 16)

def generate_key():
    private_key = int(secrets.token_hex(32), 16)
    public_key = elliptic_multiply(private_key, Base_G)
    return private_key, public_key

def sign(private_key, message, Z_A):
    _M = Z_A + message
    _M_b = bytes(_M, encoding='utf-8')
    e = sm3.sm3_hash(func.bytes_to_list(_M_b))
    e = int(e, 16)
    k = secrets.randbelow(Prime_P)
    random_point = elliptic_multiply(k, Base_G)
    r = (e + random_point[0]) % Order_N
    s = (mod_inverse(1 + private_key, Order_N) * (k - r * private_key)) % Order_N
    return r, s

def verify(public_key, ID, message, signature):
    r = signature[0]
    s = signature[1]
    Z = precompute(ID, Curve_A, Curve_B, Base_G_X, Base_G_Y, public_key[0], public_key[1])
    _M = str(Z) + message
    _M_b = bytes(_M, encoding='utf-8')
    e = sm3.sm3_hash(func.bytes_to_list(_M_b))
    e = int(e, 16)
    t = (r + s) % Order_N
    point = elliptic_multiply(s, Base_G)
    point1 = elliptic_multiply(t, public_key)
    point = elliptic_add(point, point1)
    x1 = point[0]
    x2 = point[1]
    R = (e + x1) % Order_N
    return R == r

if __name__ == '__main__':
    pri_key, pub_key = generate_key()
    print('生成的公钥:', pub_key)
    msg = input("请输入信息 = ")
    id_value = input("ID = ")
    Z_A = precompute(id_value, Curve_A, Curve_B, Base_G_X, Base_G_Y, pub_key[0], pub_key[1])
    signature = sign(pri_key, msg, str(Z_A))
    print("得到签名", signature)
    if verify(pub_key, id_value, msg, signature) == 1:
        print('成功了！！！')
