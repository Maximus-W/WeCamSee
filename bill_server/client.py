"""
client.py
Receive json file from server
Bill Li
Aug. 26th, 2017
"""

import socket


class Client:
    def __init__(self, host, port):
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect((host, port))

        print("Running Client")
        self.run()

    def run(self):
        while True:
            data_encoded = self.client_socket.recv(128)
            data = data_encoded.decode()
            print(data)
