import json
import struct


class Communication:
    def __init__(self, sock):
        self.sock = sock

    def send(self, data):
        print("Comm: ",data)
        data_bytes = json.dumps(data, ensure_ascii=True).encode('utf-8')
        header = struct.pack("!I", len(data_bytes))
        self.sock.sendall(header + data_bytes)

    def recv_all(self):
        header_bytes = self.recv(4)
        if not header_bytes:
            return
        header = struct.unpack("!I", header_bytes)[0]
        msg_bytes = self.recv(header)
        if len(msg_bytes) < header:
            return
        return json.loads(msg_bytes.decode('utf-8'))

    def recv(self, length):
        data = bytearray()
        while len(data) < length:
            if not (packet := self.sock.recv(length - len(data))):
                break
            data += packet
        return data
