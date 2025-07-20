import struct

raw = b'\x12\x34\x01\x00\x00\x02\x00\x00\x00\x00\x00\x00' \
      b'\x03abc\x11longassdomainname\x03com\x00\x00\x01\x00\x01' \
      b'\x03def\xc0\x10\x00\x01\x00\x01'

offset = 12

def parse_domain_name(raw, offset, visited=None):
    if visited is None:
        visited = set()
    
    labels = []
    original_offset = offset
    jumped = False

    while True:
        length =raw[offset]

        #Pointer handling
        if (length & 0xC0) == 0xC0:
            pointer = ((length & 0x3F) << 8) | raw[offset + 1]
            if pointer in visited:
                raise Exception("Loop Detected")
            visited.add(pointer)

            sub_labels,_= parse_domain_name(raw, pointer, visited)
            labels.extend(sub_labels)
            offset += 2
            jumped = True
            break

        elif length == 0:
            offset += 1
            break
        else:
            offset += 1
            label = raw[offset:offset + length].decode()
            labels.append(label)
            offset += length
    return labels, (offset if not jumped else original_offset + 2)
    

first_labels, offset = parse_domain_name(raw, 12)
print(first_labels)

offset+=4

second_labels = parse_domain_name(raw, offset)
print(second_labels)





