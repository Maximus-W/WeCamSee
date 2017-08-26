"""
runServer.py
Runs the server
Bill Li
Aug. 26th, 2017
"""

from server import Server

host = 'localhost'
port = 7878

s = Server(host, port)

while True:
    s.send(str(input()))