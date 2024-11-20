class RISCVSimulator:
    def __init__(self, memory_size=8192):
        self.registers = [0] * 32
        self.pc = 0  # 程序计数器
        self.memory = [0] * memory_size  # 模拟内存
        # 指令集字典
        self.instruction_set = {}

        # 初始化一些常用指令
        self.add_instruction(0b0110011, 0b000, 0b0000000, self.execute_add)
        self.add_instruction(0b0110011, 0b000, 0b0100000, self.execute_sub)
        self.add_instruction(0b0010011, 0b000, None, self.execute_addi)
        self.add_instruction(0b0000011, 0b010, None, self.execute_lw)
        self.add_instruction(0b0100011, 0b010, None, self.execute_sw)

    def add_instruction(self, opcode, funct3, funct7, execute_func):
        """添加新的指令到指令集"""
        self.instruction_set[(opcode, funct3, funct7)] = execute_func

    def load_instructions(self, instructions):
        """加载指令到内存"""
        for i, instr in enumerate(instructions):
            self.memory[i] = instr

    def fetch(self):
        """获取当前指令"""
        instr = self.memory[self.pc]
        self.pc += 1
        return instr

    def decode(self, instr):
        """解码指令，提取字段"""
        opcode = instr & 0b1111111
        rd = (instr >> 7) & 0b11111
        funct3 = (instr >> 12) & 0b111
        rs1 = (instr >> 15) & 0b11111
        rs2 = (instr >> 20) & 0b11111
        funct7 = (instr >> 25) & 0b1111111
        imm = (instr >> 20)  # 立即数
        return opcode, rd, funct3, rs1, rs2, funct7, imm

    def execute(self, opcode, rd, funct3, rs1, rs2, funct7, imm):
        """执行指令，根据opcode, funct3, funct7查找指令集"""
        execute_func = self.instruction_set.get((opcode, funct3, funct7))
        if execute_func:
            execute_func(rd, rs1, rs2, imm)
        else:
            print(f"未知指令: opcode={opcode}, funct3={funct3}, funct7={funct7}")

    # 执行指令的具体函数
    def execute_add(self, rd, rs1, rs2, imm=None):
        """ADD 指令"""
        self.registers[rd] = self.registers[rs1] + self.registers[rs2]

    def execute_sub(self, rd, rs1, rs2, imm=None):
        """SUB 指令"""
        self.registers[rd] = self.registers[rs1] - self.registers[rs2]

    def execute_addi(self, rd, rs1, rs2=None, imm=None):
        """ADDI 指令"""
        self.registers[rd] = self.registers[rs1] + imm

    def execute_lw(self, rd, rs1, rs2=None, imm=None):
        """LW 指令"""
        address = self.registers[rs1] + imm
        self.registers[rd] = self.memory[address]

    def execute_sw(self, rd, rs1, rs2=None, imm=None):
        """SW 指令"""
        address = self.registers[rs1] + imm
        self.memory[address] = self.registers[rs2]

    def run(self):
        """运行所有指令"""
        while self.pc < len(self.memory):
            instr = self.fetch()
            opcode, rd, funct3, rs1, rs2, funct7, imm = self.decode(instr)
            self.execute(opcode, rd, funct3, rs1, rs2, funct7, imm)
            self.registers[0] = 0  # 确保 x0 始终为0

# 示例使用
sim = RISCVSimulator()

# 假设我们加载一组汇编码为机器码的指令
instructions = [
    0x0B00006F,
    0x00000013,
    0x00000013,
    0x00000013,
    0x00000013,
    0x00000013,
    0x00000013,
    0x00000013,
    0xFE112E23,
    0xFE512C23,
    0xFE612A23,
    0xFE712823,
    0xFEA12623,
    0xFEB12423,
    0xFEC12223,
    0xFED12023,
    0xFCE12E23,
    0xFCF12C23,
    0xFD012A23,
]
sim.load_instructions(instructions)
sim.run()

print("Registers:", sim.registers)
