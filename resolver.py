import socket
import sys
import time


class EntryCache:
    def __init__(self, domain, ip, record_type):
        self.domain = domain
        self.ip = ip
        self.record_type = record_type
        self.timestamp = time.time() 

    def is_expired(self, ttl_seconds):
        return time.time() > self.timestamp + ttl_seconds
    

def add_cache_entry(domain, ip, record_type):
    cache_dict[domain] = EntryCache(domain, ip, record_type)

def handle_respnse_from_server(data):
    if( data.decode() == "non-existent domain"):
        s.sendto(b'non-existent domain', addr)
    parts = data.decode().split(',')
    add_cache_entry(parts[0],parts[1],parts[2])

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind(('127.0.0.1', int(sys.argv[1])))

serverAddr = (sys.argv[2], int(sys.argv[3]))
cache_dict = {}

while True:
    #wait for requests from the resolver
    data, addr = s.recvfrom(1024)
    query = data.decode().strip()
    #check the caches
    response = cache_dict.get(query)
    if not response or response.is_expired(int(sys.argv[4])):
        print("response not found in the cache")
        s.sendto(query.encode(), serverAddr)
         #wait for an answer and print it
        data, responseAddr = s.recvfrom(1024)
        handle_respnse_from_server(data)
    else:
        print("response found in the cache")
    
    response = cache_dict.get(query)         
    if(not response):
        continue

    if(response.record_type == "NS"):
        pass # need to write the logic 
    else:
        print("sending ", cache_dict.get(query).ip)
        s.sendto(cache_dict.get(query).ip.encode(), addr)
   
    