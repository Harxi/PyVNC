import struct

def bytesToInteger(b: bytes) -> int:

    return struct.unpack(">I", b)[0]

    

def bytesToShort(b: bytes) -> int:

    return struct.unpack(">H", b)[0]

        
