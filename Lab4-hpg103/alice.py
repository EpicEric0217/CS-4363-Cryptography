# Message Sender - crypto_chat_client.py
import hashlib, random, os, time
from binascii import hexlify
from socket import *
import hw4_shared as ct
import dh as deh

# P and G are agreed upon by both Bob and Alice. They are not shared over a network connection, so Darth does not know about it.
P = 13;  # A prime number P is taken
G = 7;  # A primitive root for P, G is taken
a = 21
bobPublicKey = 6  # assume received earlier from Bob for the UDP connection setup simplicity of this lab. In real-world, Bob would send it over UDP.


def get_dh_sharedsecret():
    x = deh.dh_generateSecretKey((get_dh_sharedkey()), a, P)
    # Enter your code here to call the function from your DiffieHellman file to generate shared secret
    return x


def get_dh_sharedkey():
    x = deh.dh_generatePublicKey(P, G, a)
    # Enter your code here to call the function from your DiffieHellman file to generate shared key
    return x


def encrypt(plaintext, usePKI, useDH, clientSecret):
    mssg = ct.encrypt(plaintext, usePKI, useDH, clientSecret)
    return mssg


def send_Message(message, UDPsock, address, usePKI, useDH, clientSecret):
    mssg = encrypt(message, usePKI, useDH, clientSecret)
    mssg = bytes(mssg, 'utf-8')
    UDPsock.sendto(mssg, (address))


def main():
    host = "127.0.0.1"  # set to IP address of target computer
    port = 8080
    address = (host, port)
    UDPSock = socket(AF_INET, SOCK_DGRAM)
    UDPSock.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)

    # initiate the encryption variables
    sendUsingPrivate = False;
    sendUsingDH = True;
    skipEncryption = False;
    # Bob and Alice have agreed upon the public keys G and P

    # no matter what, get the ECC shared key, only use it if the user enables
    x = get_dh_sharedkey()
    print("Alice key for sharing is", x)
    clientSecret = str(get_dh_sharedkey()).encode()
    print(clientSecret)

    sharedSecret = get_dh_sharedsecret()
    print("Shared secret between Bob and Alice as calculated by Alice is", sharedSecret)
    # print(sharedSecret)
    # send the packet over UDP
    UDPSock.sendto(clientSecret, address)

    print("Welcome to Crypto-Chat! \n")
    print()
    flag = True

    # Enter your code here for Alice to send messages to Bob.
    while True:
        inputdata = input("Enter secure message to send or type 'exit': ")

        if inputdata == "exit":
            send_Message(inputdata, UDPSock, address, sendUsingPrivate, sendUsingDH, sharedSecret)
            os._exit(0)
        else:
            send_Message(inputdata, UDPSock, address, sendUsingPrivate, sendUsingDH, sharedSecret)

    # close UDP connection
    UDPSock.close()
    os._exit(0)


if __name__ == '__main__':
    main()
