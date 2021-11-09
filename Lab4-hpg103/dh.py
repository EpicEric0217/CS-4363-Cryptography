def power(a, b, p):
    if (b == 1):
        return a % p;
    else:
        return pow(a, b, p)


def dh_generatePublicKey(P, G, privateKey):
    # Your code for this function (copy from your homework3 submission)
    return power(G, privateKey, P)


def dh_generateSecretKey(publicKey, privateKey, P):
    # Your code for this function (copy from your homework3 submission)
    return power(publicKey, privateKey, P)