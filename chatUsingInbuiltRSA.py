import socket

import threading

import rsa #importing rsa algorithm 

import sys

def ClearPrevLine(): # this function is used to make chat interface better by clearing the previously written line
    sys.stdout.write('\x1b[1A')
    sys.stdout.write('\x1b[2K')



publickey,privatekey=rsa.newkeys(1024) #getting the keys
publickeyPartner=None



choice=int(input("Host(1) or client(2) ? ")) # assuming host will start the chat , if client starts chat first(i.e option 2 is choosen first then it gives error since client tries to connect but the server is not established)


if choice==1: # For the host
    server=socket.socket(socket.AF_INET,socket.SOCK_STREAM) # making a server object using Transmission control protocol (TCP)

    server.bind((socket.gethostbyname(socket.gethostname()),9999))# sever binds to the IP addressed 

    server.listen(1) # listening to client that is waiting for client to request, 1 here means atmost 1 clients are kept waiting when sever is busy
    
    client,addr=server.accept() #Accepting the request sent by the client and recieving its details and address

    client.send(publickey.save_pkcs1("PEM")) # it sends the public key to the partner after converting it to bytes stream

    publickeyPartner=rsa.PublicKey.load_pkcs1(client.recv(1024))#it recieves the public key of partner 

elif choice==2: # For the client

    client=socket.socket(socket.AF_INET,socket.SOCK_STREAM) # making a client object using TCP(that will use TCP for data transfer)

    client.connect((socket.gethostbyname(socket.gethostname()),9999)) # sending request to host to connect to the server

    publickeyPartner=rsa.PublicKey.load_pkcs1(client.recv(1024)) # it recieves the public key of partner

    client.send(publickey.save_pkcs1("PEM")) # sending the public key to the partner

else: # incase of invalid input
    exit() 



def sending(c):# this function is used to send the messages

    while True: # ensures the continues to transfer of information till the connection is maintained

        data=input() #taking message as input

        message=data # creating a copy

        ClearPrevLine() # this function makes the user interface better

        data=rsa.encrypt(data.encode(),publickeyPartner) #encoding using RSA algorithm

        c.send(data) #sending the bytes stream

        print("You : {}".format(message)) # printing the sent message to make interface better

###


def recieving(c): # this function is used to recive the message

    global choice #ensuring to use global variable choice

    while True: # ensures recieving message continueously

        data=c.recv(1024) # data will recieve message of size upto 1024 bytes

        data=rsa.decrypt(data,privatekey).decode() # decrypting the message recieved 
        
        # printing the message recieved

        if choice==1:

            print("Client : {} ".format(data)) 

        else: 

            print("Host : {}".format(data))
       
    
# Here we use multithreading to run the sending and recieving functions simultaneously i.e one function need not to wait for other to complete
#this allow us to continuosly send or recieve messages

threading.Thread(target=sending,args=(client,)).start()

threading.Thread(target=recieving,args=(client,)).start()
    
    

    
