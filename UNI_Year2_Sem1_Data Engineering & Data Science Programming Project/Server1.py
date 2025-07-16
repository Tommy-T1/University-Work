import socket
import tqdm
import os


#Device's ip address

SERVER_HOST = "192.168.1.159"
SERVER_PORT = 5001


#Recieve 4096 bytes each time
BUFFER_SIZE = 2404404

SEPERATOR="<SEPERATOR>"

#create the server socket
#TCP

s = socket.socket()

#bind the socket to our local adress
s.bind((SERVER_HOST, SERVER_PORT))

#enabling our servet to accept connections 
#5 here is the number of unaccepted connections that the system will allow before refusin new connections
s.listen(5)
print(f"[*] Listening as {SERVER_HOST}: {SERVER_PORT}")

#accept connection fi there is any
client_socket, address = s.accept()

#if below code is executed, that means the sender is connected
print(f"[+] {address} is connected.")


#recieve the file infos
#recieve using client socket, not server socket
received = client_socket.recv(BUFFER_SIZE).decode()
filename, filesize = received.split(SEPERATOR)

#remove absolute path if there is 
filename = os.path.basename(filename)

#convert to integer
filesize = int(filesize)


#start receiving the file from the socket and writing to the file stream 
progress = tqdm.tqdm(range(filesize), f"Receiving {filename}", unit="B", unit_scale=True, unit_divisor=1024)
with open(filename, "wb") as f:
    while True:
        #read 1024 bytes from the socket (recieve)
        bytes_read = client_socket.recv(BUFFER_SIZE)
        if not bytes_read:
            # nothing is received file transmitting is done
            break
        
        #write to the file the bytes we just recieved
        f.write(bytes_read)

        #update the progress bar 
        progress.update(len(bytes_read))
#close the client socket
client_socket.close()

#close the server socet
s.close()
