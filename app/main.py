import socket
import struct

#This class represents a DNS query. Can convert itself into bytes following a a DNS query
class DNSAnswer:
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
        return encoded
    
    def to_bytes(self):
        name = self.encode_name()
        type_bytes = struct.pack("!H", 1) # A Record
        class_bytes = struct.pack("!H", 1) # IN class
        ttl_bytes = struct.pack("!H", self.ttl) # 4 byte TTL
        ip_bytes = socket.inet_aton(self.ip_address) # Converts 8.8.8.8 to 4 bytes
        rdlength_bytes = struct.pack("!H", len(ip_bytes)) # 4 bytes for IPV4

    
        return name + type_bytes + class_bytes + ttl_bytes + rdlength_bytes + ip_bytes
    



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
    def __init__(self):
        #attributes go here
        # 16-bit fields
        self.id =  1234
        self.qdcount = 1
        self.ancount = 1
        self.nscount = 0
        self.arcount = 0

        #Bit-packed fields (stored individually first)
        self.qr = 1         # Response
        self.opcode = 0     # Standard query
        self.aa = 0         # Not authoritative
        self.tc = 0         # Not truncated
        self.rd = 0         # No recursion desired
        self.ra = 0         # No recusion available
        self.z = 0          # Reserved  (3 bits)
        self.rcode = 0      # no error
        

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


def main():
    # You can use print statements as follows for debugging, they'll be visible when running tests.
    print("Logs from your program will appear here!")

    # Uncomment this block to pass the first stage
    # Starts the UDP server at port 2053
    udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp_socket.bind(("127.0.0.1", 2053))
    
    while True:
        try:
            buf, source = udp_socket.recvfrom(512)
        
            response = b''
            header = DNSHeader()
            question = DNSQuestion('codecrafters.io')
            answer = DNSAnswer('codecrafters.io', '8.8.8.8')
            response = header.to_bytes() + question.to_bytes() + answer.to_bytes()
            print(response)
    
            udp_socket.sendto(response, source)
            
        except Exception as e:
            print(f"Error receiving data: {e}")
            break




if __name__ == "__main__":
    main()
