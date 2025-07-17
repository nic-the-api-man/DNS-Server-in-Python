import socket
import struct

class DNSHeader:
    def __init__(self):
        #attributes go here
        # 16-bit fields
        self.id =  1234
        self.qdcount = 0
        self.ancount = 0
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
            # print(buf)
            
            
            response = b"" 
            
    
            udp_socket.sendto(response, source)
            print(buf)
        except Exception as e:
            print(f"Error receiving data: {e}")
            break




if __name__ == "__main__":
    main()
