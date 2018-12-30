import sys
import socket
import struct


class CANSocket:
    PACKET_FORMAT = "<IB3x8s"

    # Used for CAN_FD compatibility
    PACKET_FD_FORMAT = "<IB3x64s"
    CAN_RAW_FD_FRAMES = 5

    # Maximum transfer units
    CAN_MTU = 16
    CANFD_MTU = 72

    def __init__(self, interface):
        self.sock = socket.socket(socket.PF_CAN, socket.SOCK_RAW, socket.CAN_RAW)
        self.bind(interface)

    def bind(self, interface):
        try:
            self.sock.bind((interface,))
        except OSError as e:
            sys.stderr.write("Error at interface binding: '%s'\n" % interface)
            sys.exit(e.errno)

    def send(self, cob_id, data, flags=0):
        cob_id = cob_id | flags
        if len(data) > 8:
            packet = struct.pack(self.PACKET_FD_FORMAT, cob_id, len(data), data)
        else:
            packet = struct.pack(self.PACKET_FORMAT, cob_id, len(data), data)
        self.sock.send(packet)

    def recv(self):
        packet = self.sock.recv(self.CANFD_MTU)
        if len(packet) == self.CAN_MTU:
            cob_id, length, data = struct.unpack(self.PACKET_FORMAT, packet)
        else:
            cob_id, length, data = struct.unpack(self.PACKET_FORMAT, packet)

        cob_id &= socket.CAN_EFF_MASK
        return cob_id, data[:length]
