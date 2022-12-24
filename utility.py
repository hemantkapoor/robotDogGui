
import struct
from ctypes import *

def convert_bytes_to_structure(st, byte):
    # sizoef(st) == sizeof(byte)
    memmove(addressof(st), byte, sizeof(st))


def convert_struct_to_bytes(st):
    buffer = create_string_buffer(sizeof(st))
    memmove(buffer, addressof(st), sizeof(st))
    return buffer.raw


class CommandHeader(Structure):
    _fields_ = [
        ("preamble", c_uint8),
        ("source", c_uint8),
        ("target", c_uint8),
        ("padding", c_uint8),
        ("length", c_uint32) ]

    def __init__(self):
        self.preamble = 0xFA
        self.source = 0x01
        self.target - 0x00
        self.length = 0x00


class CpuInformation(Structure):
    _fields_ = [
        ("preamble", CommandHeader),
        ("cpuTemp", c_float) ]

    def __init__(self):
        self.preamble = CommandHeader()
        self.cpuTemp = 10.0



if __name__ == '__main__':
    # sendingData = CommandHeader()
    # sendingData.preamble = 10
    # print(sendingData.preamble)
    # testArray = bytearray(sendingData)
    # newArray = bytearray(b'\x0A\x0B\x00\x0B')
    # newArray = bytearray(b'\x0A\x0B\x00\x0B')
    # newDataStruct = CommandHeader.from_buffer(newArray[1:])
    # print(newDataStruct.preamble)
    # print(testArray)
    a = 10.5

    #dummyPreamble = CommandHeader()

    PacketSender = CpuInformation()
    # PacketSender.preamble = dummyPreamble
    PacketSender.cpuTemp = 100

    testArray = bytearray(struct.pack("f", a))
    b = struct.unpack("f", testArray)
    print(type(b))
    print(PacketSender.preamble.preamble)
    testCommandHanler = CommandHeader()
    print(testCommandHanler.preamble)

