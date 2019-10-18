import sys
from instruction import Instruction, Command


class Interpretor:
    def __init__(self, filename):
        self._file = filename
        self._listofinstruction = []
        self._run = 0
        self._byteList = []
        pass

    def _fillByteList(self):
        with open(self._file, "rb") as f:
            byte = f.read()
            byte = list(bin(int.from_bytes(byte, byteorder=sys.byteorder))[2:])

            for index in range(0, len(byte)):
                byte[index] = int(byte[index])

            byte[0] = 0

            self._byteList = byte

    def _divide_chunks(self, l, n=8):
        for i in range(0, len(l), n):
            yield l[i:i + n]

    def _readByte(self):
        tempbyte = []
        if len(self._byteList) > 0:
            for i in range(0, 4):
                tempbyte.append(self._byteList.pop(0))
            print(len(self._byteList)//4)
            if len(self._byteList) == 0:
                self._run = 0
            return tempbyte
        else:
            self._running = 0
            return [0, 0, 0, 0]

    def _interpret4bit(self, byte):
        intbyte = byte
        intbyte = "".join(str(x) for x in intbyte)
        intbyte = int(intbyte, 2)
        return intbyte

    def _createInstruction(self, intlist):
        # print(intlist)
        return Instruction(intlist[0], intlist[1], intlist[2])

    def interpret(self):
        self._fillByteList()
        self._run = 1
        byte = self._readByte()
        byte2 = self._readByte()
        byte3 = self._readByte()
        intlist = []
        while self._run == 1:
            intlist.append(self._interpret4bit(byte))
            intlist.append(self._interpret4bit(byte2))
            intlist.append(self._interpret4bit(byte3))
            if len(intlist) == 3:
                # print(intlist)
                if intlist[0] != 0:
                    self._listofinstruction.append(self._createInstruction(intlist))
                intlist = []
            byte = self._readByte()
            byte2 = self._readByte()
            byte3 = self._readByte()
        for en in self._listofinstruction:
            print([en._id, en._x1, en._x2])
        self._listofinstruction.append(Instruction(Command.e))
        return self._listofinstruction
