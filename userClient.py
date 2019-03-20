#!/usr/bin/env python

from __future__ import division, print_function
import socket
import sys

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(('localhost', 23501))
s.sendall(bytes(sys.argv[1]))
data = s.recv(1024)
if data:
    print(data)

