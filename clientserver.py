
import socket

DEF_PORT = 9999

#SERVER_ADDRESS = "127.0.0.1"
SERVER_ADDRESS = "0.0.0.0"

DEF_CONNECTION_IP = "127.0.0.1"

def menu():
    print("1. Listen")
    print("2. Connect")
    action = input("?_ ")
    print()
    if(action=="1"):
        print("Starting Server...")
        runServer()
    elif(action=="2"):
        print("Starting Client...")
        runClient()
    else:
        print("Invalid Option")
        
        
def runServer():
    print("Which local IP to listen on?")
    resp = input("IP Address (" + str(SERVER_ADDRESS) + "): ")
    addr = SERVER_ADDRESS if(resp=="") else resp
    
    print("Which port number to listen on?")
    resp = input("Port("+str(DEF_PORT)+"): ")
    port = DEF_PORT if(resp=="") else int(resp)
    
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((addr, port))
        
        s.listen()
        
        print("Listening...\n")
        conn, addr = s.accept()
        
        with conn:
            print("Connected. Receiving messages from:",addr)
            while True:
                data = conn.recv(1024)
                msg = data.decode("UTF-8")
                print('\n' + msg)
                if(msg.lower()=="bye"):
                    break
            

def runClient():
    resp = input("IP Address (" + str(DEF_CONNECTION_IP) + "): ")
    addr = DEF_CONNECTION_IP if(resp=="") else resp

    resp = input("Port("+str(DEF_PORT)+"): ")
    port = DEF_PORT if(resp=="") else int(resp)
    
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((addr,port))
        print("Connected to", addr)
        print("Type messages to send ...\n")
        while True:
            msg = input(">: ")
            data = bytes(msg, 'utf-8')
            s.sendall(data)
            if(msg.lower()=='bye'):
                break
        
        
if __name__ == "__main__":
    menu()