question1 = 'abc.codecrafters.io'

question2 = 'def.codecrafters.io'











# def header_parser(head):
#     transaction_id = struct.unpack("!H", head[:2])[0] # Parses transaction ID from buf
#     flags = struct.unpack("!H", head[2:4])[0] # Parses flags from buf, mainly qr, opcode, and rd
#     qr = (flags >> 15) & 0x1 #1 bit
#     opcode = (flags >> 11) & 0xF # 4 bits (bits 11 - 4)
#     rd = (flags >> 8) & 0x1 # 1 (Bit 8)
#     x = transaction_id, qr, opcode, rd
#     return [x[0],x[1],x[2]]