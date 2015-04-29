'''
This is simple sender using socket.
You change UDP_IP to any IP4 addresses locating in the same LAN of your own.
'''

import socket

UDP_IP = "127.0.0.1"
UDP_PORT = 5005
MESSAGE = "Hello, World!"

print "UDP target IP:", UDP_IP
print "UDP target port:", UDP_PORT
print "message:", MESSAGE

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) 
sock.sendto(MESSAGE, (UDP_IP, UDP_PORT))