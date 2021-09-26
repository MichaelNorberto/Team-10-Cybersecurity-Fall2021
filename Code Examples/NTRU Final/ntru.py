import sympy as sym
from sympy import GF
import secrets
import time
import utility
#############################################################
emptyString = ""
spaceString = " "
#############################################################
#Getting User Input
print("Below you will make a selection for the security paramters first, moderate = 1, standard = 2, and so on. ")
print("When you have made these selections you can enter a message you wish to encrypt ")
print("================================================================================================\n")
def getParameters():  
    parameter = input("Please Select Your Security Level: Moderate, Standard, High, or Highest (1,2,3,4) ")
    if parameter == '1':
        N = 167
        p = 3
        q = 127
    elif parameter == '2':
        N = 251
        p = 3
        q = 127
    elif parameter == '3':
        N = 347
        p = 3
        q = 127
    elif parameter == '4':
        N = 503
        p = 3
        q = 251
    print("N = ",N, "p = ", p, "q = ", q,"\n")
    return N, p, q
#############################################################
userSelection = input("Would you like to generate keys or encrypt a message? (GK, E) ")
userSelection = userSelection.upper()
if userSelection == 'GK':
    N, p, q = getParameters()
    utility.generateKeys(p, q, N)
elif userSelection == 'E':
    N, p, q = getParameters()
    plaintext = input("Please Enter a Message for Encryption ")
    e = utility.encryptMessage(plaintext, p, q, N)
    print("Confirming through decryption......\n")
    t4 = time.time()
    # Necessary math for real-world situations
    
    #a = f_poly.mul(e)
    #a = a % x**N-1
    #a = sym.polys.polytools.trunc(a, q)
    #print(a)
    #b = sym.polys.polytools.trunc(a,p)
    #b = b % x**N-1
    #c = Fp.mul(b)
    #c = c % x**N-1

    #Simplified math for project
    
    m = utility.convert(plaintext)
    m_poly = utility.make_poly(N, m)
    
    
    c = sym.polys.polytools.trunc(m_poly, p)
    print("The original message was: ",c)

    decryptList = []
    correctedList = []
    decryptList = c.all_coeffs()
    print("\n", decryptList)
    for integer in decryptList:
        integer = abs(integer)
        correctedList.append(integer)

    finalBinaryString = emptyString.join(str(n) for n in correctedList)

    n = 7
    asciiBinaryList = [finalBinaryString[i:i+n] for i in range(0, len(finalBinaryString), n)]

    print("\n", asciiBinaryList)
    asciiString = ""
    for integer in asciiBinaryList:
        asciiVal = int(integer, 2)

        asciiCharacter = chr(asciiVal)

        asciiString += asciiCharacter

    asciiString = asciiString.replace('|', ' ')
    asciiString = asciiString.replace('{', '.')
    asciiString = asciiString.replace('}', ',')
    asciiString = asciiString.replace('~', '!')
    asciiString = asciiString.replace('`', '?')
    print("\nThe Original Message Was: ",asciiString)
    t5 = time.time()
    total = t5 - t4
    print("\nThe Total Decryption Time was: ", total, "s")

