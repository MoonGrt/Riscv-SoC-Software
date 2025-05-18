from RISCVSim.pyriscv import PyRiscv
from RISCVSim.pymem import PyMEM

if __name__ == '__main__':
    imem = PyMEM("./RISCVSim/test1.v")
    PyRiscv(imem, imem)