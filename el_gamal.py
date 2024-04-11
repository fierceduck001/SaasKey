import numpy as np
import random
from math import sqrt

XA = 1
q = 1
a = 1

def setXA(num):
    global XA
    XA = num

def getXA():
    return XA

def setq(num):
    global q
    q = num

def getq():
    return q

def seta(num):
    global a
    a = num

def geta():
    return a

def power(x, y, p):
    res = 1  # Initialize result
    x = x % p  # Update x if it is more than or equal to p
    while (y > 0):
        if (y & 1):
            res = (res * x) % p
        y = y >> 1  # y = y/2
        x = (x * x) % p
    return res

def findPrimefactors(s, n):
    while (n % 2 == 0):
        s.add(2)
        n = n // 2
    for i in range(3, int(sqrt(n)), 2):
        while (n % i == 0):
            s.add(i)
            n = n // i
    if (n > 2):
        s.add(n)

def findPrimitive(n):
    s = set()
    phi = n - 1
    findPrimefactors(s, phi)
    for r in range(2, phi + 1):
        flag = False
        for it in s:
            if (power(r, phi // it, n) == 1):
                flag = True
                break
        if (flag == False):
            return r
    return -1

def generate_public_key():
    while (1):
        q = random.randrange(100, 999)
        i = q - 1
        ct = 0
        while (i >= 5):
            if (q % i == 0):
                ct += 1
                break
            i -= 1
        if (ct == 0):
            print("🔒 Prime random number q generated:", q)
            break
    a = 15  # findPrimitive(q)
    seta(a)
    print("🔍 Finding a primitive number for the prime number q...")
    print("✅ Primitive number found:", a)
    XA = random.randrange(0, q - 1)
    print("🔑 Private key XA is generated:", XA)
    temp = a ** XA
    YA = temp % q
    publickey = [q, a, YA, XA]
    print("🔑 Public key YA is generated:", YA)
    return publickey

def incrypt_gamal(q, a, YA, text):
    print("🔐 Secure Transmission Initiated: Implementing ElGamal Encryption Protocol")
    text = list(text)
    asc = [ord(char) for char in text]
    M = asc
    k = random.randrange(0, q)
    print("🔢 Random integer k generated between 0 and q:", k)
    temp = YA ** k
    K = temp % q
    print("🔑 K =", K)
    temp = a ** k
    C1 = temp % q
    print("🔐 Generated Cipher 1:", C1)
    C2 = [(K * char) % q for char in M]
    print("🔐 Generated Cipher 2:", C2)
    returnedvalue = str(C1) + ","
    returnedvalue += ",".join([str(char) for char in C2]) + ","
    returnedvalue += str(q)
    print("📤 Returned value:", returnedvalue)
    return returnedvalue

def decrept_gamal(messagecopy, XA):
    print("🔓 Unlocking the Secrets: Commencing Decryption Protocol")
    tempmessage = messagecopy.split(",")
    C1 = int(tempmessage[0])
    q = int(tempmessage[-1])
    C2 = [int(char) for char in tempmessage[1:-1]]
    print("🔐 Received Cipher 1:", C1)
    print("🔐 Received Cipher 2:", C2)
    temp = C1 ** XA
    K = temp % q
    print("🔑 K =", K)
    kinverse = K
    ct = 1
    while ((kinverse * ct) % q != 1):
        ct += 1
    kinverse = ct
    print("🔄 Finding K inverse:", kinverse)
    output = [char * kinverse % q for char in C2]
    print("🔓 The output is:", output)
    decryptedText = "".join([chr(char) for char in output])
    print("🔤 Decrypted Text:", decryptedText)
    return decryptedText
