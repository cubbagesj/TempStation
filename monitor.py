# monitor.py
#
# Simple code to monitor messages from ESPs

import socket

# open a socket to listen for data on
# all modules send to the same port
UDPSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

listen_addr = ("", 21567)
UDPSock.bind(listen_addr)



while True:
    data, addr = UDPSock.recvfrom(1024)

    print(data)

    
