import socket,fcntl,struct

def get_ip_addr(ifname):
   temp_sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
   return socket.inet_ntoa(fcnt.ioctl(
      temp_sock.fileno(),
      0x8915,
      struct.pack('256s',ifname[:15])
   )[20:24])
   
mysock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
wlan_ip = get_ip_addr('wlan0')
mysock.bind(wlan_ip,8800)
mysock.connect(('www.google.com',80))
