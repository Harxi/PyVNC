1: ...

ZeroTypes -> Error:
    
    """Number of security types is zero"""
    
    If number-of-security-types is zero, then for some reason the connection failed (e.g., the server cannot support the desired protocol version). This is followed by a string describing the reason (where a string is specified as a length followed by that many ASCII characters):

    +---------------+--------------+---------------+
    | No. of bytes  | Type [Value] | Description   |
    +---------------+--------------+---------------+
    | 4             | U32          | reason-length |
    | reason-length | U8 array     | reason-string |
    +---------------+--------------+---------------+
