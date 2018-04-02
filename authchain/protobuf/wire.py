"""
Minimal implementation of the Tendermint go-wire protocol. Just enough
to support what's needed for ABCI communication with protobuf
"""
from io import BytesIO
from authchain.protobuf.utils import int_to_big_endian, big_endian_to_int
from authchain.protobuf.varint import  decode_stream, ZigZagDecode , encode

def uvarint_size(i):
    if i == 0:
        return 0
    for j in [1,2,3,4,5,6,7,8]:
        if i < 1 << j * 8:
            return j
    return 8

def write_svarint(i, writer):
    size = encode(i)
    writer.write(size)

def read_varint(reader):
    r = decode_stream(reader)
    return ZigZagDecode(r)

def write_byte_slice(bz, buffer):
    write_svarint(len(bz), buffer)
    buffer.write(bz)

def read_byte_slize(reader):
    length = read_varint(reader)
    return length, reader.read(length)

def write_message(message):
    buffer = BytesIO(b'')
    bz = message.SerializeToString()
    write_byte_slice(bz, buffer)
    return buffer.getvalue()

def read_message(reader, message):
    current_position = reader.tell()
    length, bsliced = read_byte_slize(reader)
    if len(bsliced) == 0:
        return None, 0

    if len(bsliced) < length:
        return current_position, -1
    m = message()
    m.ParseFromString(bsliced)
    return m, 1
