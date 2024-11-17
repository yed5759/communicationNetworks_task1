import socket
import sys
from datetime import datetime

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind(('127.0.0.1', int(sys.argv[1])))




