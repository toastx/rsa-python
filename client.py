import socket
import pickle

def encrypt(pk, plaintext):
    key, n = pk
    cipher = [pow(ord(char), key, n) for char in plaintext]
    return cipher



HOST = "127.0.0.1" 
PORT = 65432 

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))

data = s.recv(1024)
puk = pickle.loads(data)
text = "Bye bye cruel world"
print(f"data to send {text}")
enc = encrypt(puk, text)
print(f"enc_data to send {enc}")
n = len(enc)
s.send(str(n).encode())
for i in range(n):
    s.send(str(enc[i]).encode())

print("sent")
