
def parse_domain_name(raw, offset):
    offset = 12
    labels = []
    while True:
        length = raw[offset]
        if length == 0:
            break
        offset += 1 # moves to the stard of the label
        label = raw[offset:offset+length].decode()
        labels.append(label)
        offset += length
    return '.'.join(labels)



raw = b'O\xe5\x01\x00\x00\x01\x00\x00\x00\x00\x00\x00\x03abc\x0ccodecrafters\x02io\x00\x00\x01\x00\x01'

x = parse_domain_name(raw, 12)