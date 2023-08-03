import secrets

a_coefficient = 0
b_coefficient = 7
prime_p = 115792089237316195423570985008687907853269984665640564039457584007908834671663
order_n = 115792089237316195423570985008687907852837564279074904382605163141518161494337
x_coordinate = 55066263022277343669578718895168534326250603453777594175500187360389116729240
y_coordinate = 32670510020758816978083085130507043184471273380659243275938904335757337482424
base_point_G = (x_coordinate, y_coordinate)

def bool_quadratic_residue(n, p):
    return pow(n, (p - 1) // 2, p)

def solve_quadratic_residue(n, p):
    assert bool_quadratic_residue(n, p) == 1
    if p % 4 == 3:
        return pow(n, (p + 1) // 4, p)
    q = p - 1
    s = 0
    while q % 2 == 0:
        q = q // 2
        s += 1
    for z in range(2, p):
        if bool_quadratic_residue(z, p) == p - 1:
            c = pow(z, q, p)
            break
    r = pow(n, (q + 1) // 2, p)
    t = pow(n, q, p)
    m = s
    if t % p == 1:
        return r
    else:
        i = 0
        while t % p != 1:
            temp = pow(t, 2 ** (i + 1), p)
            i += 1
            if temp % p == 1:
                b = pow(c, 2 ** (m - i - 1), p)
                r = r * b % p
                c = b * b % p
                t = t * c % p
                m = i
                i = 0
        return r

def modular_inverse(B, N):
    if B == N:
        return (B, 1, 0)
    else:
        i = 0
        b = [B]
        n = [N]
        q = []
        r = []
        flag = False

        while not flag:
            q.append(n[i] // b[i])
            r.append(n[i] % b[i])
            n.append(b[i])
            b.append(r[i])
            if r[i] == 0:
                flag = True
            i += 1
        tmp = b[i - 1]
        x = [1]
        y = [0]

        i -= 2
        num = i

        while i >= 0:
            y.append(x[num - i])
            x.append(y[num - i] - q[i] * x[num - i])
            i -= 1

        return (tmp, x[-1], y[-1])

def extended_gcd(b, n):
    (g, x, y) = modular_inverse(b, n)

    if g == 1:
        return x % n
    else:
        return -1


def point_addition(P, Q):
    if P == 0 and Q == 0:
        return 0
    elif P == 0:
        return Q
    elif Q == 0:
        return P
    else:
        if P[0] > Q[0]:
            tmp = P
            P = Q
            Q = tmp

        Z = []
        t = (Q[1] - P[1]) * extended_gcd(Q[0] - P[0], prime_p) % prime_p
        Z.append((t ** 2 - P[0] - Q[0]) % prime_p)
        Z.append((t * (P[0] - Z[0]) - P[1]) % prime_p)
        return (Z[0], Z[1])

def point_doubling(P):
    Z = []
    tmp = (3 * P[0] ** 2 + a_coefficient) * extended_gcd(2 * P[1], prime_p) % prime_p
    Z.append((tmp ** 2 - 2 * P[0]) % prime_p)
    Z.append((tmp * (P[0] - Z[0]) - P[1]) % prime_p)
    return (Z[0], Z[1])

def point_multiplication(k, g):
    tmp = g
    z = 0
    k_bin = bin(k)[2:]
    k_len = len(k_bin)

    for i in reversed(range(k_len)):
        if k_bin[i] == '1':
            z = point_addition(z, tmp)
        tmp = point_doubling(tmp)

    return z

def generate_key_pair():
    private_key = int(secrets.token_hex(32), 16)
    public_key = point_multiplication(private_key, base_point_G)
    return private_key, public_key

def sign_message(private_key, message):
    e = hash(message)
    k = secrets.randbelow(prime_p)
    R = point_multiplication(k, base_point_G)
    r = R[0] % prime_p
    s = extended_gcd(k, order_n) * (e + r * private_key) % order_n
    return (r, s)

def deduce_public_key_from_signature(signature, message):
    r = signature[0]
    s = signature[1]
    x = r % prime_p
    y = solve_quadratic_residue(((x ** 3) + 7), prime_p)
    e = hash(message)

    P1 = (x, y)
    P2 = (x, prime_p - y)
    sk1 = point_multiplication(s % order_n, P1)
    tmp = point_multiplication(e % order_n, base_point_G)
    tmp_i = (tmp[0], prime_p - tmp[1])
    tmp_1 = point_addition(sk1, tmp_i)
    pk1 = point_multiplication(extended_gcd(r, order_n), tmp_1)

    sk2 = point_multiplication(s % order_n, P2)
    tmp_2 = point_addition(sk2, tmp_i)
    pk2 = point_multiplication(extended_gcd(r, order_n), tmp_2)
    return pk1, pk2

if __name__ == '__main__':
    private_key, public_key = generate_key_pair()
    print("公钥：\n", public_key)
    message = "你好，世界！"
    signature_result = sign_message(private_key, message)
    print("签名：\n", signature_result)
    pub1, pub2 = deduce_public_key_from_signature(signature_result, message)
    print('尝试从签名中推导出公钥：')
    print('可能的公钥 1：\n', pub1)
    print('可能的公钥 2：\n', pub2)
