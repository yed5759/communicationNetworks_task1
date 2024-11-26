import socket
import sys
import time


class EntryCache:
    def __init__(self, domain, ip=None, record_type=None):
        self.domain = domain
        self.ip = ip
        self.record_type = record_type
        self.timestamp = time.time()

    #check if the entry has been x seconds in the cache
    def is_expired(self, ttl_seconds):
        return time.time() > self.timestamp + ttl_seconds


def handle_response_from_server(data):
    #decode the data
    print("new cache data: " + data.decode())

    split = data.decode().strip()
    split = split.split(',')

    #the result was non-existent domain
    if len(split) == 1:
        entry = EntryCache(split[0])

    #create an entry and put in the cache
    else:
        ip = split[1].split(':')
        if len(ip) == 2:
            entry = EntryCache(split[0], (ip[0], int(ip[1])), split[2])
        else:
            entry = EntryCache(split[0], ip[0], split[2])

    cache_dict[split[0]] = entry
    print("cache:")
    for key, value in cache_dict.items():
        print(f"{key}: {value.domain}, {value.ip}, {value.record_type}")
    print("--------------------")

    return entry

#create and bind the socket
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind(('', int(sys.argv[1])))

#handle the program args
serverAddr = (sys.argv[2], int(sys.argv[3]))
cache_dict = {}
seconds = int(sys.argv[3])
clientAddr = []
while True:
    # wait for requests from the client
    data, addr = s.recvfrom(1024)
    query = data.decode().strip()
    clientAddr.append(addr)

    # check the caches
    response = cache_dict.get(query)

    #the domain is not in the cache
    if not response or response.is_expired(seconds):
        s.sendto(query.encode(), serverAddr)
        # wait for an answer and print it
        data, responseAddr = s.recvfrom(1024)
        response = handle_response_from_server(data)

    #the father server returns ip of type NS
    while "NS" == response.record_type:
        serverAddr = response.ip
        s.sendto(query.encode(), serverAddr)
        print(query)

        data, addr = s.recvfrom(1024)
        query = data.decode().strip()
        clientAddr.append(addr)
        # check the caches
        response = cache_dict.get(query)
        print(data.decode())
        if not response or response.is_expired(seconds):
            response = handle_response_from_server(data)

    #return response.domain to client
    serverAddr = (sys.argv[2], int(sys.argv[3]))
    s.sendto(response.ip.encode(), clientAddr[0])

