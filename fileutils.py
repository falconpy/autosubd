#!/usr/bin/env python
import struct
import os

class File(object):
    def __init__(self, archivo):
        self.path = archivo
        self.size = os.path.getsize(archivo)

    def get_hash(self):
        '''Original from: http://goo.gl/qqfM0'''
        longlongformat = 'q'  # long long
        bytesize = struct.calcsize(longlongformat)
        try:
            f = open(self.path, "rb")
        except(IOError):
            return "IOError"
        hash = int(self.size)
        if int(self.size) < 65536 * 2:
            return "SizeError"
        for x in range(65536 / bytesize):
            buffer = f.read(bytesize)
            (l_value, ) = struct.unpack(longlongformat, buffer)
            hash += l_value
            hash = hash & 0xFFFFFFFFFFFFFFFF  # to remain as 64bit number
        f.seek(max(0, int(self.size) - 65536), 0)
        for x in range(65536 / bytesize):
            buffer = f.read(bytesize)
            (l_value, ) = struct.unpack(longlongformat, buffer)
            hash += l_value
            hash = hash & 0xFFFFFFFFFFFFFFFF
        f.close()
        returnedhash = "%016x" % hash
        return str(returnedhash)
