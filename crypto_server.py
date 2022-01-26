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
username = ""

#create a dictionary for storing connections and corrosponding subscriptions 
subs = {}

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

def handle_client(conn, addr):
    print(f"[NEW USER] {addr} connected.")
    username = get_username(conn)
    #send list from there 
    try:
        handle_list(username ,conn)
    except:
        action_listen(username,conn)
    #action_listen(conn)

    
        

def start():
    server.listen()
    print(f"[LISTENING] Server is listening on {SERVER}")
    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.activeCount() - 1}")

def get_username(conn):
    msg_length = conn.recv(HEADER).decode(FORMAT)
    msg_length = int(msg_length)
    msg = conn.recv(msg_length).decode(FORMAT)
    return msg
        
def subscribe_coin(coinname, username, conn):
    subs[username] = []
    subs[username].append(coinname)
    #add assosiated user with coin 
    print("subbed")
    #print("current sub list is :" + subs["zyad"])

def get_subscriptions(username):
    print("getting......")
    #sub_list = subs[username]
    #print("sub list is: " + sub_list)
    #return ",".join(sub_list)


def handle_list(username, conn):
    try:
        crypto_list = subs[username]
        list_ordered = ",".join(crypto_list)
        subs_list = get_subscriptions(username)
        msg = "Connected.\nyour current subscriptions are\n" + subs_list
        conn.send(msg.encode(FORMAT))
        action_listen(username, conn)
    except:
        conn.send("Connected.\nyou currently have no subscriptions\ncurrent options are: !DOGECOIN and !ETH".encode(FORMAT))
        action_listen(username, conn)

def action_listen(username, conn):
    connected = True
    while True:
        msg_length = conn.recv(HEADER).decode(FORMAT)
        if msg_length:
            msg_length = int(msg_length)
            msg = conn.recv(msg_length).decode(FORMAT)

            if msg == DISCONNECT_MESSAGE:
                connected = False

            if msg == "!DOGECOIN":
                print("got doge req")
                conn.send("Added Dogecoin".encode(FORMAT))
                subscribe_coin("Doge", username, conn)
                action_listen(username, conn)
            
            if msg == "!ETH":
                print("got eth req")
                conn.send("Added ETH".encode(FORMAT))
                subscribe_coin("ETH",  username, conn)
                action_listen(username, conn)

            if msg == "!notify":
                for x in range(100):
                    conn.send((cryptocompare.get_price('BTC')).encode(FORMAT))
                notify_client(username,conn)

            

        if connected == False:
            conn.send("Disconnecting....".encode(FORMAT))
            conn.close()


def notify_client(username, conn):
    print("Notifs on")
    subs_list = get_subscriptions(username)
    for x in subs_list:
        print(x)
    #grab subs and send back prices 
    #for i in range(60): 
     #   price_json = cryptocompare.get_price(coinname, 'USD')
      #  price = json.dumps(price_json)
       # print("Sending price")
        #conn.send((price).encode(FORMAT))

print("[STARTING] server is starting...")
start()