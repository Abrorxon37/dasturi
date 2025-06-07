"""
Lokal tarmoq uchun modul (socket asosida)
"""
import socket
import threading

class NetworkClient:
    def __init__(self, host, port):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((host, port))

    def send(self, data):
        self.sock.sendall(data.encode())

    def recv(self):
        return self.sock.recv(1024).decode()

class NetworkServer:
    def __init__(self, host, port):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind((host, port))
        self.sock.listen(1)
        self.conn, _ = self.sock.accept()

    def send(self, data):
        self.conn.sendall(data.encode())

    def recv(self):
        return self.conn.recv(1024).decode()