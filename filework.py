import sys
from instruction import Instruction, Command


class workingFunction:
    def _swap(self, x1, x2):
        temp = self._bytelist[self._row][x1]
        self._bytelist[self._row][x1] = self._bytelist[self._row][x2]
        self._bytelist[self._row][x2] = temp
        pass

    def _combine(self, x1, x2):
        if x1 != x2 and x1 < x2:
            del self._bytelist[self._row][x1:x2]
        pass

    def _unpack(self, x1, z):
        for i in range(0, z):
            self._bytelist[self._row].insert(x1, self._bytelist[self._row][x1])
        pass

    def _fill(self, binary, nil=0):
        pass

    def _next(self, nil=0, nill=0):
        self._row += 1
        pass

    def _end(self, nil=0, nill=0):
        self._running = 0
        pass

    execute = {1: _swap,
               2: _combine,
               3: _unpack,
               4: _fill,
               5: _next,
               6: _end,
               }
    pass


class Encryptor(workingFunction):

    def __init__(self, fileName):
        self._file = fileName
        self._outfile = fileName.split('.')[0] + "-encrpt.cmp"
        self._bytelist = []
        self._row = 0
        self._running = 0
        self._instructionlist = []
        self._tempinstruct = []

    def _load_file_binary(self):
        with open(self._file, 'rb') as f:
            byte = f.read()
            byte = list(bin(int.from_bytes(byte, byteorder=sys.byteorder))[2:])

            for index in range(0, len(byte)):
                byte[index] = int(byte[index])

            # print(len(byte))

            while len(byte) % 8 != 0:
                byte.insert(0, 0)

            bytelist = []

            while len(byte) > 0:
                for i in range(0, 8):
                    bytelist.append(byte.pop(0))
                self._bytelist.append(bytelist)
                bytelist = []

            # print(self._bytelist)
        pass

    def _write_file(self):
        with open(self._file, 'wb') as f:
            f.write(self._prep_file_binary())

    def _write_instruction(self):
        with open(self._outfile, 'wb') as f:
            f.write(self._prep_command_binary())

    def _prep_command_binary(self):
        instructbinary = []
        for en in self._instructionlist:
            for e in en:
                instructbinary.append(e)

        while (len(instructbinary) * 4) % 8 != 0:
            instructbinary.append([0, 0, 0, 0])

        bitstring = []
        for en in instructbinary:
            bitstring += en

        bitstring[0] = 1

        bitstring = "".join(str(x) for x in bitstring)

        return int(bitstring, 2).to_bytes((len(bitstring) + 7) // 8, byteorder=sys.byteorder)

    def _prep_file_binary(self):
        filebinary = []
        for en in self._bytelist:
            filebinary += en

        a = 8 - (len(filebinary) % 8)

        # print(len(filebinary) % 8)

        filebinary.insert(0, 0)
        for i in range(0, a - 1):
            filebinary.insert(0, 1)

        # print(filebinary[0:16])
        # print(len(filebinary) % 8)

        filebinary = "".join(str(x) for x in filebinary)

        return int(filebinary, 2).to_bytes((len(filebinary) + 7) // 8, byteorder=sys.byteorder)

    def executeInstruction(self, inst):
        Encryptor.execute[inst._id](self, inst._x1, inst._x2)
        # print(inst.commandbinary)
        if inst._id == Command.c:
            self._tempinstruct.append(Instruction(Command.u, inst._x1, inst._x2 - inst._x1).commandbinary)
        elif inst._id == 6:
            for i in range(0, len(self._tempinstruct)):
                self._instructionlist.append(self._tempinstruct.pop())
            self._instructionlist.append(inst.commandbinary)
            self._tempinstruct.clear()
        elif inst._id == 5:
            for i in range(0, len(self._tempinstruct)):
                self._instructionlist.append(self._tempinstruct.pop())
            self._instructionlist.append(inst.commandbinary)
            self._tempinstruct.clear()
        else:
            self._tempinstruct.append(inst.commandbinary)
        pass

    def end_encrypt(self):
        self._write_file()
        self._write_instruction()
