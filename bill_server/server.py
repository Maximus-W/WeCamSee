"""
server.py
Send json file to client
Bill Li
Aug. 26th, 2017
"""

import socket


class Server:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        data = b'{"building": "DC", "room": "101", "availability": [true, false, true, false]}'

        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(5)
        self.connection, self.address = self.server_socket.accept()

        print("Running the server")
        self.run()

    def run(self):
            self.connection.send(b'hello')

    def send(self, message):
        self.connection.send(str.encode(message))
