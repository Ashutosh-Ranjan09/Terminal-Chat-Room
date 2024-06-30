import math

import random

# defining some variable which will be used as global variable
e=0  # (e,n) is public key

d=0  # (d,n) is private key

n=0 # part of keys

publickey=() # tuple to store public key

privatekey=() # tuple to store private key

prime=[]  # List to store the prime numbers in the desired range 


def prime_filler(): # this funtion will fill the list with prime numbers

    i=2 
    while i<500: # value 500 ensures that all prime no.s are less than 500 , we can choose a larger value to increase security but will in crease the time to encrypt and decrypt(mainly) the message
        
        for j in prime: #using the concept of seive of eratosthenis to fill the list with prime numbers

            if i%j==0:

                break

        else: # else condition is hit when the break statement doesnot work i.e for prime numbers

            prime.append(i) 

        i+=1

###

def keygen(): # funtion to generate public and private keys
    global prime
    global e
    global d
    global publickey
    global privatekey

    prime_filler() #function is called to fill the prime global list with prime numbers

    size=prime.__len__() #Number of integers in list

    random_index=random.randint(int(size/2),size-1) #selecting the random index from the larger half (for better security) of the prime list

    p=prime[random_index] # picking a prime number from the list

    prime.remove(p) # removing the number which is picked to avoid repition of choosen prime numbers

    size=size-1 # after removal size decreases by one

    random_index=random.randint(int(size/2),size-1) # picking the index randomly from larger half for the second prime number

    q=prime[random_index] #picking the second prime number
    
    
    n=p*q #part of key

    phi=(p-1)*(q-1) #euler's toitient function for prime products

    e=2

    while e<phi: # finding the other part of the public key

        if math.gcd(e,phi)==1:
            break

        else:
            e+=1

    d=2

    while True:# finding the other part of the private key
        if (d*e)%phi==1:
            break

        else:
            d+=1

    publickey=(e,n)#storing public key

    privatekey=(d,n)#storing private key

###

def take_users_key(userk): # this function is used to take other user's public key which will be used to encrypt the message so that , it could only be decrypted by that other user
    global publickey
    userkey=userk
    publickey=userkey # we will replace the public key with other user's public key after giving the generated key to the user

###

def encrypt(ascii):#taking ascii value of characters present in the message string as input and returning the encrypted value
    global publickey
    global privatekey

    temp_e=publickey[0] #part of public key of other user
    temp_n=publickey[1] #other part of public key of other user

    encrypted_ascii=1

    while temp_e :#enrypting the ascii value of characters

        encrypted_ascii*=ascii

        encrypted_ascii%=temp_n

        temp_e-=1

    return encrypted_ascii

def decrypt(en_ascii):#decrypting the encrypted value to get original ascii values
    global privatekey

    temp_d=privatekey[0]
    temp_n=privatekey[1]

    decrypted_ascii=1

    while temp_d:

        decrypted_ascii*=en_ascii

        decrypted_ascii%=temp_n

        temp_d-=1

    return decrypted_ascii

def encoder(message):#encoding the entire string

    encoded_list=[] #list to store encoded values of each character of string

    for ch in message:#iterating over message to encrypt each character

        encoded_list.append(encrypt(ord(ch))) #storing the encrypted ascii values of each character present in string  in the list 
        
    return encoded_list

def decoder(enList):#decoding the entire encoded string present as list and returning the original message

    s=""
    
    for li in enList: #iterating over list to decrypt each character
        s+=chr(decrypt(li))

    return s



    
    
    


    
