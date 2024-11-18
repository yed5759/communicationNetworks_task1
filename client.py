import socket
import sys

#open a socket to resolver
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
while True:
    #ask for a domain's IP
    message=input()
    s.sendto(message.encode(), (sys.argv[1], int(sys.argv[2])))
    #wait for an answer and print it
    data, addr = s.recvfrom(1024)
    print(data.decode())
s.close()
