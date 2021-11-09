# Federated Learning allows for smarter models, lower latency, and less power consumption,
# all while ensuring privacy. And this approach has another immediate benefit: in addition to
# providing an update to the shared model, this model uses several algorithms in random succesion
# in order to secure a system as much as possible. Using a randomly adapting model such as this
# creates a repsonse time that is as low as possible. Power consumption is also low, as the functions
# being used have relatively simple algorithms.

import random

# Performs a caesar cipher that shifts based upon the provided s value
def xxx( message, s ):
    shift_t = ""
    # Transverse the message text
    for i in range( len( message ) ):
        char = message[ i ]
        
        # Encrypt the uppercase characters in plain text
        if( char.isupper() ):
            shift_t += chr( ( ord( char ) + s - 65 ) % 26 + 65 )
        # Encrypt lowercase characters in plain text
        else:
            shift_t += char( ( ord( char ) + s - 97 ) % 26 + 97 )
        return shift_t
    
def shiftCipher(text,s):
    result = ""
    # transverse the plain text
    for i in range(len(text)):
        char = text[i]
       # Encrypt uppercase characters in plain text
      
        if (char.isupper()):
            result += chr((ord(char) + s-65) % 26 + 65)
      # Encrypt lowercase characters in plain text
        else:
            result += chr((ord(char) + s - 97) % 26 + 97)
    return result

def get_cipherletter(new_key, letter):
    #still need alpha to find letters
    alpha = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

    if letter in alpha:
        return alpha[new_key]
    else:
        return letter
    
def decryptShift(key, message):
    message = message.upper()
    alpha = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    result = ""

    for letter in message:
        new_key = (alpha.find(letter) - key) % len(alpha)
        result = result + get_cipherletter(new_key, letter)

    return result

# Reverses the message text
def reverseCipher( message ):    
    # Reverses the string by adding the last character of the original message
    # as the first character of the new string
    reversedText = ""
    for i in range( len( message ), 0, -1 ):
        reversedText += message[ i - 1 ]
    
    return reversedText

print("***PlainText should not contain spaces or any special characters. (Includes periods or commas)***\n")

# The original plain text
plain_t = input("Input plain text:")
# A temporary text store
temporary_t = ""
# The final cipher text
cipher_t = ""

i = 0
# Creates a random length of the encryption cycle
random_length = random.randrange(0, 101, 1)
# Array to hold the checkpoint values
checkpoint_arr = []
# Array to hold the shift values
shift_arr = []

print("PlainText:", plain_t)
    
# Loops random_length number of times in order to encrypt the plain_text
while( i < random_length ):
    # Generates random number from 0 to 1
    random_use = random.randrange(0, 2)
    # Generates random number from 0 to 9
    random_s = random.randrange(0, 10)
    # If we are at the very first encryption, always use the shift cipher
    if(i == 0):
        temporary_t = shiftCipher(plain_t, random_s)
        # Because the shift cipher was used, append a zero to the checkpoint array
        checkpoint_arr.append(0)
        # Append the shift value to the shift array
        shift_arr.append(random_s)
    else:
        # Randomly select between the shift and reverse cipher
        if( random_use == 0 ):
            # Uses the shift cipher
            temporary_t = shiftCipher(temporary_t, random_s)
            # Adds a 0 to represent that the shift cipher was used
            checkpoint_arr.append(0)
            # Adds the number shifted by to the shift array
            shift_arr.append(random_s)
        elif( random_use == 1 ):
            # Uses the reverse cipher
            temporary_t = reverseCipher(temporary_t)
            # Adds a 1 to represent that the reverse cipher was used
            checkpoint_arr.append(1)
        # Increments the counter for the loop
    i = i + 1
# Sets the cipher text value as the end result of the previous encryption loop
cipher_t = temporary_t

print("The checkpoint array is:", checkpoint_arr)
print("The array of shift values is:", shift_arr)
print("CipherText:", cipher_t)
print("")

i = random_length - 1
## Create decryption algorithm
shift_count = 1
while(i >= 0):
     
    # If the array value is 0, it is a shift cipher that needs to be decrypted
    if(checkpoint_arr[i] == 0):
        # Accesses the proper shift increment from the array (in a reverse fashion as the text is being decrpyted)
        shift_v = shift_arr[len(shift_arr) - shift_count]
        cipher_t = decryptShift(shift_v, cipher_t)
        # Increments the shift counter
        shift_count = shift_count + 1
    if(checkpoint_arr[i] == 1):
        cipher_t = reverseCipher(cipher_t)
    i = i - 1
    
new_plain_t = cipher_t
print("PlainText:", new_plain_t)

