class Command:
    s = 1
    c = 2
    u = 3
    f = 4
    n = 5
    e = 6

    def __init__(self):
        pass


class Instruction:
    def __init__(self, command_id, x1=0, x2=0):
        self._id = command_id
        self._x1 = x1
        self._x2 = x2

        tempid = self._generate_binary_code(self._id)
        tempx1 = self._generate_binary_code(self._x1)
        tempx2 = self._generate_binary_code(self._x2)

        self.commandbinary = [tempid, tempx1, tempx2]

    def _generate_binary_code(self, inte):
        tempList = list(bin(inte)[2:])

        for index in range(0, len(tempList)):
            tempList[index] = int(tempList[index])

        while len(tempList) < 4:
            tempList.insert(0, 0)

        return tempList
