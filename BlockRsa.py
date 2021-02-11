"""
Author:Jiaxi Chen
"""
#Euler's totient function
def totientFunction(p, q):
    return (p - 1) * (q - 1)


#Euclidean algorithm
def gcd(a, b):
    while a != 0:
        a, b = b % a, a
    return b
"""
Generate e value   
from 1 < e < totient
co-prime with totient
"""

def chooseE(totient):
    e = 2
    while gcd(e, totient) != 1:
        e += 1
    return e

#Extended Euclidean algorithm
def egcd(a,b):
    if a == 0:
        return b, 0, 1
    else:
        g, y, x = egcd(b % a, a)
        return g, x-(b//a) * y, y

#modular inverse
def modInverse(e, totient):
    g, x, y = egcd(e, totient)
    if g != 1:
        return -1
    else:
        return x % totient

def powMod(m, ed, n):
    m %= n
    result = 1
    while ed != 0:
        if ed & 1:
            result = (result * m) % n
        ed >>= 1
        m = (m % n) * (m % n)
    return result
#Check whether nums is prime
def isPrime(nums):
    if nums <= 1:
        return False
    if nums <= 3:
        return True
    for i in range(2, int(nums ** 0.5) + 1):
        if nums % i == 0:
            return False
    return True

#Generate public key and private key
def createKey(blocksize):
    while(True):
        try:
            p = int(input("Type p value: "))
            q = int(input("Type q value: "))
            if p * q < int("27"*blocksize):
                print("The Value of p and q is too small. p * q should be larger than %d" %(int("27"*blocksize)))
                continue
            if isPrime(p) & isPrime(q):
                break
            print("p or q is not prime, try again. ")
        except(ValueError):
            print("Invalid, Input p and q value again. ")
    n = p * q
    totient = totientFunction(p, q)
    e = chooseE(totient)
    d = modInverse(e, totient)
    return ((e, n), (d, n))

#Encrypt with public key and message
def encryptMessage(publicKey, message, blocksize):
    e, n = publicKey
    blocktext =[]
    count = 0
    value = 0
    for c in message:
        if c == ' ':
            value = value * 100 + ord(c) - 5
        else:
            value = value*100 + ord(c)-96
        count += 1
        if count == blocksize:
            count = 0
            blocktext.append(value)
            value = 0
    if value != 0:
        for i in range(blocksize - value):
            value *= 100
        blocktext.append(value)
    ciphertext = []
    for c in blocktext:
        ciphertext.append(powMod(c, e, n))
    return ciphertext

#decrypt with private key and ciphertext
def decryptMessage(privateKey, ciphertext, blocksize):
    d, n = privateKey
    originaltext =[]

    for c in ciphertext:
        blockvalue = powMod(c, d, n)
        temptext = str(blockvalue).zfill(2 * blocksize)
        for i in range(0, len(temptext),2):
            if int(temptext[i:i+2]) == 27:
                originaltext.append(" ")
            elif int(temptext[i:i+2]) != 0:
                originaltext.append(chr(int(temptext[i:i+2])+96))
    return ("".join(originaltext))


#test main funciton
if __name__ == '__main__':
#block size is how many character in the block. tester can change the value of the blocksize
    blocksize = 2
    publicKey, privateKey = createKey(blocksize)
    pliantext = input("Input a message: ")
    ciphertext = encryptMessage(publicKey, pliantext, blocksize)
    originaltext = decryptMessage(privateKey, ciphertext, blocksize)
    print('\n-------------Public Key--------------------')
    print('e = %-10d' % publicKey[0], 'n = ', publicKey[1])
    print('\n-------------Private Key-------------------')
    print('d = %-10d' % privateKey[0], 'n = ', privateKey[1])
    print('\n-------------Ciphertext--------------------')
    print(''.join(map(lambda x: str(x), ciphertext)))
    print('\n-------------Decrypted plaintext-----------')
    print(originaltext)


