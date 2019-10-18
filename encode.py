import sys
from compressor import Compressor
from decompressor import Decompressor
from interpretor import Interpretor


if __name__ == '__main__':
    # str = "0100110"
    # bit = [0, 1, 1, 0]
    # interp = Interpretor("Test")
    # ins = interp._createInstruction([interp._interpret4bit(bit), 1, 1])
    # print(len([interp._interpret4bit(bit), 1, 1]))

    if len(sys.argv) == 2:
        comp = Compressor(sys.argv[1])
        comp.run()
    elif len(sys.argv) == 3:
        decomp = Decompressor(sys.argv[1], sys.argv[2])
        decomp.run()
    else:
        print("Please enter the correct number of command arguments.\n")
