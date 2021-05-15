
#test
import socket 
import threading


HEADER = 64
PORT = 5050
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

def handle_client(conn, addr):
    print(f"[NEW USER] {addr} connected.")
    
    connected = True
    while connected:
        msg_length = conn.recv(HEADER).decode(FORMAT)
        if msg_length:
            msg_length = int(msg_length)
            msg = conn.recv(msg_length).decode(FORMAT)

            if msg == DISCONNECT_MESSAGE:
                connected = False
        
            if msg == "!DOGECOIN":
                addCoin("Doge")

            print(f"[{addr}] {msg}")
            msg_back = "The following is a list of cryptos avaliable, please pick from the following cryptos followed by a !:"
            conn.send(msg_back.encode(FORMAT))
            conn.send("Test list".encode(FORMAT))
            list_sent = True

        if connected == False:
            conn.send("Disconnecting....".encode(FORMAT))
    conn.close()
 

def start():
    server.listen()
    print(f"[LISTENING] Server is listening on {SERVER}")
    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.activeCount() - 1}")

        
def addCoin(coinname):
    print(coinname)


print("[STARTING] server is starting...")
start()