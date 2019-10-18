from instruction import Instruction
from instruction import Command
from filework import Encryptor


class Compressor:
    def __init__(self, file1):
        self._file = file1
        self._mode = 0  # 0 = encrypt 1 = decrypt

        self.program = Encryptor(self._file)
        self.program._load_file_binary()

    def _determine_instruction(self):

        if len(self.program._bytelist[self.program._row]) == 2:
            if self.program._row + 1 == len(self.program._bytelist):
                return "End"  # Instruction(Command.e)
            else:
                return "Next"  # Instruction(Command.n)

        if all(elm == 0 for elm in self.program._bytelist[self.program._row]) or all(elm == 1 for elm in self.program._bytelist[self.program._row]):
            return "CombineFill"

        if all(self.program._bytelist[self.program._row][i] <= self.program._bytelist[self.program._row][i+1] for i in range(len(self.program._bytelist[self.program._row])-1)) is True:
            return "Combine"
        else:
            return "Swap"
        pass

    def _swapFunction(self):
        n = len(self.program._bytelist[self.program._row])
        for i in range(n):
            for j in range(n - i - 1):
                if self.program._bytelist[self.program._row][j] > self.program._bytelist[self.program._row][j+1]:
                    self.program.executeInstruction(Instruction(Command.s, j, j+1))
        pass

    def _combineFunction(self):
        firstOne = self.program._bytelist[self.program._row].index(1)
        LastZero = firstOne - 1
        self.program.executeInstruction(Instruction(Command.c, firstOne, len(self.program._bytelist[self.program._row]) - 1))
        self.program.executeInstruction(Instruction(Command.c, 0, LastZero))
        pass

    def _combineFill(self):
        self.program.executeInstruction(Instruction(Command.c, 0, 6))

    def _runInstruction(self, commandStr):
        if commandStr == "Swap":
            self._swapFunction()
        elif commandStr == "Combine":
            self._combineFunction()
        elif commandStr == "CombineFill":
            self._combineFill()
        elif commandStr == "Next":
            self.program.executeInstruction(Instruction(Command.n))
        elif commandStr == "End":
            self.program.executeInstruction(Instruction(Command.e))

    def run(self):
        self.program._running = 1
        while self.program._running == 1:
            self._runInstruction(self._determine_instruction())
        self.program.end_encrypt()
