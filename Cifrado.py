

#Abrir el archivo de texto.
mensajeE = open("mensajedeentrada.txt","r+",encoding="utf-8")
#Lee las lineas del archivo de texto.
linea = mensajeE.readline()
#Cierra el archivo de texto.
mensajeE.close()

#CIFRADO Y DESCIFRADO
#Refenciado de :https://github.com/jbdrvl/cryptography/blob/master/Feistel-cipher/feistel.py
import random as rd
import sys
import hashlib
#FUNCION CIFRADO
def cipher(inp, keys, f):
    for key in keys:
        L, R = split(inp)
        Ln = xor(L, f(key, R))
        inp = R+Ln
    return Ln+R
#FUNCION CORTE EN 2 LADOS DER,IZQ.
def split(inp):
    assert len(inp)%2==0
    return inp[:int(len(inp)/2)], inp[int(len(inp)/2):]
#Feistel
def xor(a, b):
    output=""
    for i in range(len(a)):
        #print(i, a, b)
        inter=int(a[i])+int(b[i])
        if inter==2: inter=0
        output = output+str(inter)
    return output
#Funcion para generar las llaves.
def keyGen(l,n):
    '''
    l: length of key
    n: number of keys needed
    '''
    o=[]
    for i in range(n):
        k=""
        for i in range(l):
            k = k + str(rd.randint(0,1))
        o.append(k)
    return o
#Funcion para convertir el codigo binario a hexadecimal.
def binToHex(binary):
	res="0x"
	hexList = [hex(int(binary[i:i+8], 2))[2:] for i in range(0, len(binary),8)]
	for hexa in hexList:
		if len(hexa)==1: hexa ="0"+hexa
		res = res + hexa
	return res
#Funcion para Crear el archivo de texto con el mensaje cifrado dentro.
def ArchivoCifrado(C):
    mensajeS = open("mensajeseguro.txt","w+",encoding="utf-8")
    mensajeS.write(C)
    mensajeS.close()
#Main
if __name__ == "__main__":
    # obtiene el texto y lo convierte en binario
    plainText = linea.strip()
    hashing = hashlib.md5()
    hashing.update(plainText.encode())
    plainTextHash = hashing.hexdigest()
    plainInts = [bin(ord(letter))[2:] for letter in plainText]
    plainBin=""
    for integer in plainInts:
        while len(integer)!=8:
            integer = "0"+integer
        plainBin = plainBin+integer
    #Genera una lista de llaves.
    keyList = keyGen(int(len(plainBin)/2), 16)
    # Encriptado
    C = cipher(plainBin, keyList, xor)
    keyList.reverse()
    result = cipher(C, keyList, xor)
    # convertint result to ASCII string
    resultToChar = [chr(int(result[i:i+8], 2)) for i in range(0, len(result),8)]
    resultText=""
    for letter in resultToChar:
        resultText = resultText+letter

    hashing = hashlib.md5()
    hashing.update(resultText.encode())
    decryptedTextHash = hashing.hexdigest()
    # printing results
    print("\n")
    print("Mensaje de entrada:         {}\n".format(plainText))
    print("Mensaje de entrada a hexadecimal: {}\n".format(binToHex(plainBin)))
    print("Mensaje Cifrado:              {}\n".format(binToHex(C)))
    
    if decryptedTextHash == plainTextHash:
        print("El mensaje no fue modificado")
    else:
        print("virus")

#LLamamos a la funcion para crear el archivo de texto mensajeseguro.txt.
ArchivoCifrado(C)