#!/usr/bin/env python

from __future__ import division, print_function
import socket

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(('localhost', 23500))
s.sendall(bytes(1 << 3))
data = s.recv(1024)
if data:
    print(data)

