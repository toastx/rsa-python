import socket
import secrets
from sympy import isprime
import pickle

def gcd(a, b):
    while b != 0:
        a, b = b, a % b
    return a

def multiplicative_inverse(e, phi):
    d = 0
    x1 = 0
    x2 = 1
    y1 = 1
    temp_phi = phi

    while e > 0:
        temp1 = temp_phi//e
        temp2 = temp_phi - temp1 * e
        temp_phi = e
        e = temp2

        x = x2 - temp1 * x1
        y = d - temp1 * y1

        x2 = x1
        x1 = x
        d = y1
        y1 = y

    if temp_phi == 1:
        return d + phi



def generate_prime():
    c = 0
    k = 0 
    bit_length = 1024
    while k == 0:
        random_number = secrets.randbits(bit_length)
        if isprime(random_number):
            print("found")
            k = 1
            return random_number

def generate_key_pair():
    p = generate_prime()
    c = 0
    q = 0
    while c == 0:
        q = generate_prime()
        if p !=q:
            c = 1
    print(f"p:{p}")
    print(f"q:{q}")
    n = p * q
    print(f"n:{n}")
    phi = (p-1) * (q-1)
    e = 65537
    print(f"e:{e}")
    g = gcd(e, phi)
    while g != 1:
        g = gcd(e, phi)
    d = multiplicative_inverse(e, phi)
    print(d)
    return ((e, n), (d, n))



def decrypt(pk, ciphertext):
    
    key, n = pk
    aux = [str(pow(char, key, n)) for char in ciphertext]
    plain = [chr(int(char2)) for char2 in aux]
    return ''.join(plain)


HOST = "127.0.0.1"
PORT = 65432
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
s.listen()
conn, addr = s.accept()
with conn:
    lst = []
    print(f"Connected by {addr}")
    puk,prk = generate_key_pair()
    serialized_data = pickle.dumps(puk)
    conn.send(serialized_data)
    n = conn.recv(1024).decode()
    for i in range(int(n)):
        some_data = conn.recv(1024).decode()
        lst.append(int(some_data))
        
    enc = lst
    print(f"recieved {enc}")
    pt = decrypt(prk,enc)
    print(f"message decrpyterd {pt}")
