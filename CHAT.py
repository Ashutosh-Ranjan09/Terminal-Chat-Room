import socket

import pickle

import threading

import MYRSA #importing rsa algorithm 

import sys

def ClearPrevLine(): # this function is used to make chat interface better by clearing the previously written line
    sys.stdout.write('\x1b[1A')
    sys.stdout.write('\x1b[2K')

MYRSA.keygen() # generating keys

myprivatekey=MYRSA.privatekey # accesing keys as tuple
mypublickey=MYRSA.publickey


choice=int(input("Host(1) or client(2) ? ")) # assuming host will start the chat , if client starts chat first(i.e option 2 is choosen first then it gives error since client tries to connect but the server is not established)


if choice==1: # For the host
    server=socket.socket(socket.AF_INET,socket.SOCK_STREAM) # making a server object using Transmission control protocol (TCP)

    server.bind((socket.gethostbyname(socket.gethostname()),9999))# sever binds to the IP addressed 

    server.listen(1) # listening to client that is waiting for client to request, 1 here means atmost 1 clients are kept waiting when sever is busy
    
    client,addr=server.accept() #Accepting the request sent by the client and recieving its details and address

elif choice==2: # For the client

    client=socket.socket(socket.AF_INET,socket.SOCK_STREAM) # making a client object using TCP(that will use TCP for data transfer)

    client.connect((socket.gethostbyname(socket.gethostname()),9999)) # sending request to host to connect to the server

else: # incase of invalid input
    exit() 


##### An alternative way to share the public key without using pickle module

# e=mypublickey[0]
# client.send(str(e).encode('utf-8'))
# e=client.recv(4096)
# e=e.decode('utf-8')
# e=int(e)

# n=mypublickey[1]
# client.send(str(n).encode('utf-8'))
# n=client.recv(4096)
# n=n.decode('utf-8')
# n=int(n)
# userkey=(e,n)

####

# with the help of pickle module we can convert the container objects like tuple in to bytes streams , which we can share

client.send(pickle.dumps(mypublickey)) # sending public key to the other user

userkey=client.recv(4096) # recieving the public key of the other user

userkey=pickle.loads(userkey) #program decodes the byte streams recieved by client.recv into it's original container form (tuple here)

####

MYRSA.take_users_key(userkey)#this call will replace the public key with the other user's public key in RSA algorithm so, that we could code with the other user's public key and at other end that user will be able to decode the message with his private key only

###

def sending(c):# this function is used to send the messages

    while True: # ensures the continues to transfer of information till the connection is maintained

        data=input() #taking message as input

        message=data # creating a copy

        ClearPrevLine() # this function makes the user interface better

        data=MYRSA.encoder(data) #encoding using RSA algorithm

        data=pickle.dumps(data) #converting the list returned above in bytes streams

        c.send(data) #sending the bytes stream

        print("You : {}".format(message)) # printing the sent message to make interface better

###


def recieving(c): # this function is used to recive the message

    global choice #ensuring to use global variable choice

    while True: # ensures recieving message continueously

        data=c.recv(4096) # data will recieve message of size upto 4096 bytes

        data=pickle.loads(data) #will convert back the bytes into list 

        data=MYRSA.decoder(data) # the above list will get converted into string using decoder functin present in RSA algorithm

        # printing the message recieved

        if choice==1:

            print("Client : {} ".format(data)) 

        else: 

            print("Host : {}".format(data))
       
    
# Here we use multithreading to run the sending and recieving functions simultaneously i.e one function need not to wait for other to complete
#this allow us to continuosly send or recieve messages

threading.Thread(target=sending,args=(client,)).start()

threading.Thread(target=recieving,args=(client,)).start()
    
    

    
