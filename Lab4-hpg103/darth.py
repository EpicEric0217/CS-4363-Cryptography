# Message Receiver - crypto_chat_server.py
import hashlib, random, os, time
from binascii import hexlify
from socket import *
import hw4_shared as ct
import dh as deh

# P and G are agreed upon by both Bob and Alice to be 13 and 9 respectively. They are not shared over a network connection, so Darth does not know about it.
P = 13;  # A prime number P is taken
G = 7;  # A primitive root for P, G is taken
d = 6  # Darth's private key


def get_dh_sharedsecret(sharedKey):
    # Enter your code here to call the function from your DiffieHellman file to generate shared secret
    x = deh.dh_generateSecretKey(get_dh_sharedkey(), d, P)
    return x


def get_dh_sharedkey():
    # Enter your code here to call the function from your DiffieHellman file to generate shared secret
    x = deh.dh_generatePublicKey(P, G, d)
    return x


def decrypt(ciphertext, usePKI, useDH, serverSecret):
    # mssg = ct.decrypt(ciphertext, usePKI, useDH, serverSecret)
    try:
        mssg = ct.decrypt(ciphertext, usePKI, useDH, serverSecret)
    except:
        mssg = ciphertext
    return mssg


def main():
    # set variables used to determine scheme
    useClientPKI = False;
    useDHKey = True;
    serverSecret = 0

    # set the variables used for the server components
    key = ""
    host = "127.0.0.1"
    port = 8080
    buf = 1024 * 2
    address = (host, port)
    UDPSock = socket(AF_INET, SOCK_DGRAM)
    # UDPSock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)

    # Enable broadcasting mode
    UDPSock.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)
    UDPSock.bind(address)

    print("Waiting to received shared key from Alice...")
    (inputdata, address) = UDPSock.recvfrom(buf)

    sharedKey = int(str(inputdata, 'utf-8'))
    print("Shared key between Bob and Alice is", sharedKey)
    sharedSecret = get_dh_sharedsecret(sharedKey)

    print("Shared secret between Bob and Alice as calculated by Darth is", sharedSecret)

    # welcome to the server message
    print("Waiting to receive messages...")

    # listening loop
    # Enter your code here for darth.py to listen to alice's messages
    while True:
        inputdata, address = UDPSock.recvfrom(buf)
        inputdata = str(inputdata, 'utf-8')
        mssg = decrypt(inputdata, useClientPKI, useDHKey, sharedSecret)
        print("Received wrong message:", mssg)

    UDPSock.close()
    os._exit(0)


if __name__ == '__main__':
    main()
