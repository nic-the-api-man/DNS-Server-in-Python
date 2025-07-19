import struct


def qd_count(raw):
    raw = struct.unpack("!H", raw[4:6])[0]
    return raw

raw = b'\x7f\\\x01\x00\x00\x01\x00\x00\x00\x00\x00\x00\x0ccodecrafters\x02io\x00\x00\x01\x00\x01'

x = qd_count(raw)

print(x)
