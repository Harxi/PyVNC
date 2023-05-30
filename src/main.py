import socket

from Crypto.Cipher import DES

from classes.Node import Node
from classes.PixelFormat import PixelFormat

from utilities import *

class VNConnection(Node):
    def __init__(self, host: str, port: int, password: str):
        super().__init__(host, port, password)
    
    def send(self, value: bytes) -> None:
        self._session.send(value)
    
    def recv(self, length) -> bytes:
        return self._session.recv(length)     
    
    def handshake(self) -> None:
        # Protocol version
        self.send(b"RFB 003.008\n")
        self.version = self.recv(12)
        
        print(f"Protocol: {self.version.decode('utf-8')}")
        
        if self.version != b"RFB 003.008\n":
            self._session.close()
            # TO DO / NotSupportedVersion
            raise RuntimeError
        
        # Get count of supported security types
        data = ord(self.recv(1))
        
        if data == 0:
            self._session.close()
            # TO DO / ZeroTypes
            raise RuntimeError
        
        # Get security types
        self.types = self.recv(data)
        print(f"Security Types: {len(self.types)}: {[_ for _ in self.types]}")
         
        if 2 not in self.types:
            self._session.close()
            # TO DO / NotSupportedVersion
            raise RuntimeError
         
        # Select security type
        self.send(b"\2") 
        
        # Send password
        self.challenge = self.recv(16)
        self.send(self.ECB()) 
        
        # Get status
        self.status = self.recv(4)
        
        if self.status[-1]:
            data = self.recv(bytesToInteger(self.recv(4))).decode("utf-8")
            self._session.close()
            # TO DO / AuthenticationFailure
            raise RuntimeError(data)
        
        # Send ClientInit
        self.send(b"\1")
        
        # Get info about display
        self.width = bytesToShort(self.recv(2))
        self.height = bytesToShort(self.recv(2))
        self.pixelFormat = PixelFormat(ord(self.recv(1)), ord(self.recv(1)), ord(self.recv(1)), ord(self.recv(1)), (bytesToShort(self.recv(2)),bytesToShort(self.recv(2)), bytesToShort(self.recv(2))),(ord(self.recv(1)), ord(self.recv(1)), ord(self.recv(1))), self.recv(3))
        self.name = self.recv(bytesToInteger(self.recv(4)))
    
    def ECB(self) -> bytes:
        return DES.new(bytes([int(f'{ord(c):08b}'[::-1], 2) for c in self.PASSWORD[:8]]).ljust(8, b"\0"), DES.MODE_ECB).encrypt(self.challenge)
    
    def run(self) -> None:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as self._session:
            self._session.connect((self.HOST, self.PORT))
            
            self.handshake()

a = VNConnection("127.0.0.1", 5901, "Password")
a.run() 
