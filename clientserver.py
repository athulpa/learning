
import socket

DEF_PORT = 9999
SERVER_ADDRESS = "127.0.0.1"
DEF_CONNECTION_IP = "127.0.0.1"

def menu():
    print("1. Listen")
    print("2. Connect")
    action = input("?_ ")
    if(action=="1"):
        runServer()
    elif(action=="2"):
        runClient()
    else:
        print("Invalid Option")
        
def runServer():
    resp = input("Port("+str(DEF_PORT)+"): ")
    port = DEF_PORT if(resp=="") else int(resp)
    
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((SERVER_ADDRESS, port))
        
        s.listen()
        
        print("Listening...")
        conn, addr = s.accept()
        
        with conn:
            print("Connected. Receiving messages from:",addr)
            while True:
                data = conn.recv(1024)
                if not data:
                    break
                msg = data.decode("UTF-8")
                print(msg)
            
    
def runClient():
    resp = input("IP Address (" + str(DEF_CONNECTION_IP) + "): ")
    addr = DEF_CONNECTION_IP if(resp=="") else resp

    resp = input("Port("+str(DEF_PORT)+"): ")
    port = DEF_PORT if(resp=="") else int(resp)
    
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((addr,port))
        print("Connected to", addr)
        while resp!='q':
            msg = input()
            data = bytes(msg, 'utf-8')
            s.sendall(data)
        s.sendall(b'')