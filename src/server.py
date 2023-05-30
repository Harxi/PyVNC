
import socket, os

from Crypto.Cipher import DES

from classes.Node import Node
from classes.PixelFormat import PixelFormat

from utilities import *

class VNConnection(Node):
    def __init__(self, host: str, port: int, password: str, name: str, width: int, height: int):
        super().__init__(host, port, password)
        self.name = name
        self.width = width
        self.height = height
        self.pixelFormat = PixelFormat(0, 0, 0, 0, (255, 255, 255), (0, 0, 0), 0)
        
    def send(self, value: bytes) -> None:
        self.connection.send(value)
    
    def recv(self, length) -> bytes:
        return self.connection.recv(length)     
    
    def handshake(self) -> None:
        # Protocol version
        self.send(b"RFB 003.008\n")
        self.version = self.recv(12)
        
        print(f"Protocol: {self.version.decode('utf-8')}")
        
        if self.version != b"RFB 003.008\n":
            self._session.close()
            # TO DO / NotSupportedVersion
            raise RuntimeError
        
        # Send count of supported security types
        self.send(b"\1")
        
        # Send security types
        self.send(b"\2")
         
        # Get security type
        self.type = self.recv(1)
        
        if 2 not in self.type:
            self.send(b"\0\0\0\x19Not allowed security type")
            self._session.close()
            exit(-1)
        
        # Send challenge
        self.challenge = os.urandom(16)
        self.send(self.challenge)
        self.key = self.recv(16)
        if self.ECB() != self.challenge:
            self.send(b"\0\0\0\1\0\0\0\x14Authentication error")
            self._session.close()
            print("Authentication error")
            exit(-1)
        
        # Send status
        self.send(b"\0\0\0\0")
        
        # Im too lazy to do disconnection of other clients, so we skip it
        self.recv(1)
        
        # Send ServerInit
        self.send(shortToBytes(self.width))
        self.send(shortToBytes(self.height))
        
        # Send pixelFormat. TODO / Send data from class PixelFormat
        self.send(b'\x18\x00\x01\x00\xff\x00\xff\x00\xff\x10\x08\x00\x00\x00\x00')
        
        self.name = self.send(integerToBytes(len(self.name)) + bytes(self.name, "utf-8"))
        
        
    
    def ECB(self) -> bytes:
        return DES.new(bytes([int(f'{ord(c):08b}'[::-1], 2) for c in self.PASSWORD[:8]]).ljust(8, b"\0"), DES.MODE_ECB).decrypt(self.key)
    
    def run(self) -> None:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as self._session:
            self._session.bind((self.HOST, self.PORT))
            self._session.listen(0)
            self.connection, self.address = self._session.accept()
            self.handshake()

a = VNConnection("127.0.0.1", 5901, "password", "name", 100, 100)
a.run()
