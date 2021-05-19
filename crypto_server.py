
#test

import socket 
import threading
import json
import cryptocompare
import time
from time import sleep
from threading import Thread

HEADER = 64
PORT = 5050
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"
subscriptions = {}

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

def handle_client(conn, addr):
    print(f"[NEW USER] {addr} connected.")
    
    connected = True
    send_list(conn)
    while connected:
        msg_length = conn.recv(HEADER).decode(FORMAT)
        if msg_length:
            msg_length = int(msg_length)
            msg = conn.recv(msg_length).decode(FORMAT)

            if msg == DISCONNECT_MESSAGE:
                connected = False
        
            if msg == "!DOGECOIN":
                conn.send("Added Dogecoin".encode(FORMAT))
                subscribe_coin("Doge",conn)
               

            if msg == "!notify":
                notify_client("Doge",conn)

            

        if connected == False:
            conn.close()
            conn.send("Disconnecting....".encode(FORMAT))
        
    conn.send("".encode(FORMAT))

    
        

def start():
    server.listen()
    print(f"[LISTENING] Server is listening on {SERVER}")
    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.activeCount() - 1}")

def send_list(conn):
        msg_back = "The following is a list of cryptos avaliable, please pick from the following cryptos followed by a !:"
        conn.send(msg_back.encode(FORMAT))
        conn.send("Test list".encode(FORMAT))
        
def subscribe_coin(coinname, conn):

    #add assosiated user with coin 
    print("subbed")



def notify_client(coinname, conn):
    print("Notifs on")
    while True:
        price_json = cryptocompare.get_price(coinname, 'USD')
        price = json.dumps(price_json)
        print("Sending price")
        conn.send((price).encode(FORMAT))


print("[STARTING] server is starting...")
start()