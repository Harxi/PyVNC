import struct

def bytesToInteger(b: bytes) -> int:
    return struct.unpack(">I", b)[0]  

def bytesToShort(b: bytes) -> int:
    return struct.unpack(">H", b)[0]

def shortToBytes(i: int) -> bytes:
    return struct.pack(">h", i)
    
def integerToBytes(i: int) -> bytes:
    return struct.pack(">I", i)
        
