#!/usr/bin/env python

from __future__ import division,print_function
import socket
import Queue
import threading

PLC_PORT = 23500
USER_PORT = 23501

def userToPlcCommand(command):
    if command == 'OPEN_INF':
        return (1 << 1)
    elif command == 'CLOSE_INF':
        return (1 << 2)
    elif command == 'OPEN_SUP':
        return (1 << 3)
    elif command == 'CLOSE_SUP':
        return (1 << 4)
    else:
        return command

def plcToUserStatus(status):
    # no need of parsing
    return status

def plcServer(queue):
    global plc_status
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(('0.0.0.0', PLC_PORT))
    s.listen(2)
    print('Listening on port', str(PLC_PORT))
    while True:
        conn, addr = s.accept()
        print('Connected by', addr)
        # sending command
        try:
            msg = queue.get(0)
            conn.sendall(bytes(msg))
        except Queue.Empty:
            conn.sendall(bytes(1))
        # getting status
        data = conn.recv(1024)
        if data:
            plc_status = plcToUserStatus(data)
        conn.close() 

def userServer(queue):
    global plc_status
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(('0.0.0.0', USER_PORT))
    s.listen(2)
    print('Listening on port', str(USER_PORT))
    while True:
        conn, addr = s.accept()
        print('Connected by', addr)
        data = conn.recv(1024)
        command = userToPlcCommand(data)
        if command != 'GET_STATUS':
            queue.put(command)
        conn.sendall(bytes(plc_status))
        conn.close()
            

command_queue = Queue.Queue()
plc_status = 0

plc_server = threading.Thread(target=plcServer, args=(command_queue, ))
user_server = threading.Thread(target=userServer, args=(command_queue, ))

plc_server.start()
user_server.start()

