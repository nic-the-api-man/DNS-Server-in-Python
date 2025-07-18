import socket
import struct



class DNSAnswer: #This class represents a DNS query. Can convert itself into bytes following a a DNS query
    def __init__(self, domain_name, ip_address, ttl=60):
        self.domain_name = domain_name
        self.ip_address = ip_address
        self.ttl = ttl

    def encode_name(self):
        parts = self.domain_name.split(".")
        encoded = b''
        for part in parts:
            encoded += bytes([len(part)]) + part.encode()
        encoded += b'\x00'
        # print(encoded)
        return encoded
    
    def to_bytes(self):
        name = self.encode_name()
        type_bytes = struct.pack("!H", 1) # A Record
        class_bytes = struct.pack("!H", 1) # IN class
        ttl_bytes = struct.pack("!I", self.ttl) # 4 byte TTL
        ip_bytes = socket.inet_aton(self.ip_address) # Converts 8.8.8.8 to 4 bytes
        rdlength_bytes = struct.pack("!H", len(ip_bytes)) # 4 bytes for IPV4

    
        return name + type_bytes + class_bytes + ttl_bytes + rdlength_bytes + ip_bytes
    


# DNS Question section
class DNSQuestion:
    def __init__(self, domain_name, qtype=1, qclass=1):
        self.domain_name = domain_name # e.g., codecrafterts.io
        self.qtype = qtype             # usually 1 (A record)
        self.qclass = qclass           # usually 1 (IN class)

    def to_bytes(self):
        # Encodes the domain name into label format
        parts = self.domain_name.split('.')
        name_bytes = b''
        for part in parts:
            name_bytes += bytes([len(part)]) +part.encode()
        name_bytes += b'\00' #null byte to end the domain name

        # Step 2: Encode type and class  (2 bytes each, big-endian)
        qtype_bytes = struct.pack('!H', self.qtype)
        qclass_bytes = struct.pack('!H', self.qclass)

        # Step 3: Concat everything
        return name_bytes + qtype_bytes + qclass_bytes
    
class DNSHeader:
    def __init__(self, id=0, qr=1, opcode=1, aa=0, tc=0, rd=0, ra=0, z=0, rcode=0,
                 qdcount=1, ancount=1, nscount=0, arcount=0):
        
        # 16-bit fields section counts
        self.id =  id
        self.qdcount = qdcount
        self.ancount = ancount
        self.nscount = nscount
        self.arcount = arcount

        #Bit-packed fields (stored individually first)
        self.qr = qr         # Response
        self.opcode = opcode   # Standard query
        self.aa = aa         # Not authoritative
        self.tc = tc         # Not truncated
        self.rd = rd         # No recursion desired
        self.ra = ra         # No recusion available
        self.z = z          # Reserved  (3 bits)
        self.rcode = 4      # no error 4 = not implemented yet
    

    def to_bytes(self):
        flags = (
            (self.qr << 15) |
            (self.opcode << 11) |
            (self.aa << 10) |
            (self.tc << 9) |
            (self.rd << 8) |
            (self.ra << 7) |
            (self.z << 4) |
            (self.rcode)
        )


        
        return struct.pack("!6H", # 6 values, all 2-byte unsigned ints
                        self.id,
                        flags,
                        self.qdcount,
                        self.ancount,
                        self.nscount,
                        self.arcount
                                    )
    

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
        

def main():
    # You can use print statements as follows for debugging, they'll be visible when running tests.
    print("Logs from your program will appear here!")

    # Starts the UDP server at port 2053
    udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp_socket.bind(("127.0.0.1", 2053))
   
    while True:
        try:
            buf, source = udp_socket.recvfrom(512)

            transaction_id = struct.unpack("!H", buf[:2])[0] # Parses transaction ID from buf
            flags = struct.unpack("!H", buf[2:4])[0] # Parses flags from buf, mainly qr, opcode, and rd

            # Header parsing
            qr = (flags >> 15) & 0x1 #1 bit
            opcode = (flags >> 11) & 0xF # 4 bits (bits 11 - 4)
            rd = (flags >> 8) & 0x1 # 1 (Bit 8)
            response = b''
            header = DNSHeader(transaction_id,
                               qdcount=1,
                               opcode=1
            )
            header.opcode = opcode
            header.rd = rd

            # Question Parsing
            parsed_domain_name = parse_domain_name(buf,12)
            print(parsed_domain_name)
            question = DNSQuestion(parsed_domain_name)

            # Answer Parsing
            answer = DNSAnswer(parsed_domain_name, '8.8.8.8')

            response = header.to_bytes() + question.to_bytes() + answer.to_bytes()
            

            udp_socket.sendto(response, source)
            
        except Exception as e:
            print(f"Error receiving data: {e}")
            break




if __name__ == "__main__":
    main()
