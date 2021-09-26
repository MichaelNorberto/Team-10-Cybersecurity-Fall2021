# Importing necessary libraries
import sympy as sym
from sympy import GF
import secrets
import time
#############################################################
# Strings for use later on
emptyString = ""
spaceString = " "
#############################################################
def convert(plaintext):

    #Initalizing Timing
    t0 = time.time()

    print("Your entered message was: ", plaintext)

    #ASCII Conversion
    asciiString = []
    for character in plaintext:
        if ord(character) == 32:
            asciiString.append(ord('|'))
        elif ord(character) == 46:
            asciiString.append(ord('{'))
        elif ord(character) == 44:
            asciiString.append(ord('}'))
        elif ord(character) == 33:
            asciiString.append(ord('~'))
        elif ord(character) == 63:
            asciiString.append(ord('`'))
        else:
            asciiString.append((ord(character)))
        
    #Binary Conversion
    binString = []
    for integer in asciiString:
        binString.append(bin(integer).replace("0b", ""))

    #Printing Output 
    binaryStr = []
    testStr = emptyString.join(binString)
    binaryStr.append(int(emptyString.join(binString)))
    print("Converting......")
    

    # Creating mutated list of coefficients for message polynomial
    mutatedList = []
    mutationRate = 0.325
    binaryStr = list(map(int, str(binaryStr[0])))
    for integer in binaryStr:
        if secrets.SystemRandom().uniform(0.0000,1.0000) < mutationRate:
            integer = integer - (integer * 2)
            mutatedList.append(integer)
        else:
            mutatedList.append(integer)
    t1 = time.time()
    total  = t1 - t0
    print ("The total time to convert the message was: ", total, "s")
    return mutatedList
###########################################################################
def make_poly(N, coeffs):
    x = sym.Symbol('x')
    coeffs = list(reversed(coeffs))
    y = 0
    if len(coeffs) < N:
        for i in range(len(coeffs)):
            y += (x**i)*coeffs[i]
        y = sym.poly(y)
        return y
    else:
        for i in range(N):
            y += (x**i)*coeffs[i]
        y = sym.poly(y)
        return y
###########################################################################
# Generate randomized f function of length N
def generateF(N):
    mutationRate = 0.4
    fList = []
    for i in range (0,N):
        threshold = secrets.SystemRandom().uniform(0.000000000,1.0000000)
        if threshold >= 0.5:
            if threshold <= mutationRate:
                fList.append(-1)
            fList.append(1)
        elif threshold < 0.5:
            if threshold <= mutationRate:
                fList.append(-1)
            fList.append(0)
    return fList

# Generate randomized g function of length N
def generateG(N):
    mutationRate = 0.4
    gList = []
    for i in range (0,N):
        threshold = secrets.SystemRandom().uniform(0.000000000,1.0000000)
        if threshold >= 0.5:
            if threshold <= mutationRate:
                gList.append(-1)
            gList.append(1)
        elif threshold < 0.5:
            if threshold <= mutationRate:
                gList.append(-1)
            gList.append(0)
    return gList

# Generate randomized r function of length N
def generateR(N):
    mutationRate = 0.4
    rList = []
    for i in range (0,N):
        threshold = secrets.SystemRandom().uniform(0.000000000,1.0000000)
        if threshold >= 0.5:
            if threshold <= mutationRate:
                rList.append(-1)
            rList.append(1)
        elif threshold < 0.5:
            if threshold <= mutationRate:
                rList.append(-1)
            rList.append(0)
    return rList
###########################################################################
# Function to find the inverse of f with respect to p and q
def findInverse(f_poly, p, q, N):
    x = sym.Symbol('x')
    while True:
        try:
            Fp = sym.polys.polytools.invert(f_poly,x**N-1, auto=True, domain=GF(p, symmetric = False))
            break
        except:
            print("Found Non Invertible Polynomial. Regenerating Polynomial.....\n")
            try:
                f = generateF(N)
                f_poly = make_poly(N,f)
                Fp = sym.polys.polytools.invert(f_poly,x**N-1,auto = True, domain=GF(p, symmetric = False))
            except:
                print("Found Second Non Invertible Polynomial. Regenerating.....\n")
                try:
                    f = generateF(N)
                    f_poly = make_poly(N,f)
                    Fp = sym.polys.polytools.invert(f_poly,x**N-1,auto = True, domain=GF(p, symmetric = False))
                except:
                    print("Found Third Non Invertible Polynomial. Regenerating.....\n")
                    f = generateF(N)
                    f_poly = make_poly(N,f)
                    Fp = sym.polys.polytools.invert(f_poly,x**N-1,auto = True, domain=GF(p, symmetric = False))
        else:
            f = generateF(N)
            f_poly = make_poly(N,f)
            Fp = sym.polys.polytools.invert(f_poly,x**N-1,domain=GF(p, symmetric = False))
    Fq = sym.polys.polytools.invert(f_poly,x**N-1,domain=GF(q, symmetric = False))
    return Fp, Fq
###########################################################################
def generateKeys(p, q, N):

    x = sym.Symbol('x')
        
    # Generating necessary coefficients for polynomials
    f = generateF(N)
    g = generateG(N)

    # Converting to polynomials
    f_poly  = make_poly(N, f)
    g_poly = make_poly(N, g)

    # Finding Inverses
    Fp, Fq = findInverse(f_poly, p, q, N)

    # Creating Public Key
    h = Fq.mul(g_poly)
    h = p * h
    h = sym.polys.polytools.trunc(h, q)
    h = h % x**N-1

    print("Your Public Key is: ", h)
    print("\n")
    print("Your Private Key is:\nF:", f_poly, "\n\nFp: ", Fp, "\n\ng: ", g_poly)
    return h
###########################################################################
def encryptMessage(plaintext, p, q, N):

    x = sym.Symbol('x')
    
    m= convert(plaintext)
    m_poly = make_poly(N, m)

    h = generateKeys(p, q, N)

    r = generateR(N)
    r_poly = make_poly(N, r)

    
    e = r_poly.mul(h) + m_poly
    e = sym.polys.polytools.trunc(e,q)
    e = e % x**N-1

    print("\nThe Encrypted Message is: ", e)
    return e
###########################################################################
