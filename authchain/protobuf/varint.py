
from io import BytesIO
from math import ceil
import sys
if sys.version > '3':
    def _byte(b):
        return bytes((b, ))
else:
    def _byte(b):
        return chr(b)

def decode_bytes(buf):
    """Read a varint from from `buf` bytes"""
    return decode_stream(BytesIO(buf))


def decode_stream(stream):
    """Read a varint from `stream`"""
    shift = 0
    result = 0
    while True:
        i = _read_one(stream)
        result |= (i & 0x7f) << shift
        shift += 7
        if not (i & 0x80):
            break

    return ZigZagDecode(result)

def decode_bytes(bytes):
    """Read a varint from `stream`"""
    stream = BytesIO(bytes)
    shift = 0
    result = 0
    while True:
        i = _read_one(stream)
        result |= (i & 0x7f) << shift
        shift += 7
        if not (i & 0x80):
            break

    return result

def big_endian_to_int(value):
    return int.from_bytes(value, byteorder='big')

def _read_one(stream):
    """Read a byte from the file (as an integer)
    raises EOFError if the stream ends while reading bytes.
    """
    c = stream.read(1)
    if c == '':
        raise EOFError("Unexpected EOF while reading bytes")
    return ord(c)


def int_to_big_endian(value):
    byte_length = max(ceil(value.bit_length() / 8), 1)
    return (value).to_bytes(byte_length, byteorder='big')


def encode(number):
    """Pack `number` into varint bytes"""
    buf = b''
    number = ZigZagEncode(number)
    while True:
        towrite = number & 0x7f
        number >>= 7
        if number:
            buf += _byte((towrite | 0x80))
        else:
            buf += _byte(towrite)
            break
    return buf

def ZigZagEncode(value):
  """ZigZag Transform:  Encodes signed integers so that they can be
  effectively used with varint encoding.  See wire_format.h for
  more details.
  """
  if value >= 0:
    return value << 1
  return (value << 1) ^ (~0)

def ZigZagDecode(value):
  """Inverse of ZigZagEncode()."""
  if not value & 0x1:
    return value >> 1
  return (value >> 1) ^ (~0)




if __name__ == "__main__":
    result = decode_stream(BytesIO(bytes([0x14,0x02, 0x01])))
    print(ZigZagDecode(result))
