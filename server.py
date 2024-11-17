import socket
import sys

#before the opening of the socket, this code upload the IPs to a dictionary
#create a special dictionary for NS
def handle_txt(path):
    addresses = {}
    dir_ns = {}
    with open(path, 'r') as zone_txt:
        while True:
            line = zone_txt.readline()
            if not line:
                break
            parts = line.split(',')
            addresses[parts[0]] = line
            if "NS" in parts:
                dir_ns[line] = parts[1]
    return addresses, dir_ns


cache, ns = handle_txt(sys.argv[2])
#open a socket
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind(('127.0.0.1', int(sys.argv[1])))
while True:
    #wait for requests from the resolver
    data, addr = s.recvfrom(1024)
    query = data.decode().strip()
    #check the caches
    response = cache.get(query)
    if response:
        #return the IP
        s.sendto(response.encode(), addr)
    else:
        #the server did not find the domain so he check in the NS to find another server who has the mapping
        for key in ns.keys():
            if key in query:
                s.sendto((query + ' ' + ns[key]).encode(), addr)
                break
        else:
            #return domain not found
            s.sendto(b'non-existent domain', addr)
