
import struct
from ctypes import *

class CommandHeader(Structure):
    _fields_ = [
        ("preamble", c_uint8),
        ("source", c_uint8),
        ("target", c_uint8),
        ("function", c_uint8),
        ("length", c_uint32) ]

    def __init__(self):
        self.preamble = 0xFA
        self.source = 0x01
        self.target - 0x00
        self.length = 0x00
        self.function = 0x00


class CpuInformation(Structure):
    _fields_ = [
        ("preamble", CommandHeader),
        ("cpuTemp", c_float) ]

    def __init__(self):
        self.preamble = CommandHeader()
        self.cpuTemp = 10.0
