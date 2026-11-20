import socket
import struct


class Communication:
    def __init__(self,sock):
        self.sock : socket.socket = sock
    def send(self,msg):
        msg_bytes = msg.encode('utf-8')
        header = struct.pack("!I",len(msg_bytes))
        self.sock.sendall(header+msg_bytes)
    def recvall(self):
        header_len = self.recv(4)
        if not header_len:
            self.sock.close()
            return None
        header = struct.unpack("!I",header_len)[0]
        msg_bytes = self.recv(header)
        if not msg_bytes:
            self.sock.close()
            return None
        return msg_bytes.decode('utf-8')
    def recv(self,length):
        data = bytearray()
        while len(data) < length:
            if not (packet := (self.sock.recv(length - len(data)))):
                break
            data += packet
        return data
