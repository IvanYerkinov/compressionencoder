import sys
import os
from interpretor import Interpretor
from filework import workingFunction
from instruction import Command


class Decompressor(workingFunction):

    def __init__(self, file, key):
        self._filename = file
        self._keyfile = key
        self._bytelist = []
        self._row = 0
        self._running = 0
        self._instructions = []
        self._interp = Interpretor(self._keyfile)
        pass

    def _get_file_binary(self):
        op = 1
        with open(self._filename, 'rb') as f:
            byte = f.read()
            byte = list(bin(int.from_bytes(byte, byteorder=sys.byteorder))[2:])

            for index in range(0, len(byte)):
                byte[index] = int(byte[index])

            # print(byte[0:8])
            if op == 1:
                i = 0

                while byte[i] != 0:
                    i += 1
                    if byte[i] == 0:
                        i += 1
                        del byte[0:i]
                        op = 0

            # print(byte[0:8])

            while len(byte) > 0:
                pushbyte = []
                pushbyte.append(byte.pop(0))
                pushbyte.append(byte.pop(0))
                self._bytelist.append(pushbyte)

    def _executeInstruction(self, instruct):
        Decompressor.execute[instruct._id](self, instruct._x1, instruct._x2)

    def _decompress(self):
        self._executeInstruction(self._instructions.pop(0))

    def _remove_key(self):
        os.remove(self._keyfile)

    def _write_file(self):
        with open(self._filename, 'wb') as f:
            f.write(self._prep_file_binary())

    def _prep_file_binary(self):
        temp = []
        for en in self._bytelist:
            if len(en) > 2:
                temp += en

        print(self._bytelist[0:8])

        temp = "".join(str(x) for x in temp)

        return int(temp, 2).to_bytes((len(temp) + 7) // 8, byteorder=sys.byteorder)

    def run(self):
        self._instructions = self._interp.interpret()
        self._get_file_binary()
        self._running = 1
        while self._running == 1:
            # print([self._instructions[0]._id, self._instructions[0]._x1, self._instructions[0]._x2])

            if self._instructions[0]._id == Command.e:
                self._running = 0
            elif self._instructions[0]._id == 0:
                self._instructions.pop(0)
            else:
                self._decompress()
        self._write_file()
        self._remove_key()
