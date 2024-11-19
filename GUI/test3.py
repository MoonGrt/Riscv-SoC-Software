import os

# 定义目标目录
target_directory = "/mnt/hgfs/share/Riscv-SoC-Software/Workspace"

# 给定的文件路径
filePath = "/mnt/hgfs/share/Riscv-SoC-Software/Workspace/demo/bin"

# 去掉 filePath 的最后一项
parent_directory = os.path.dirname(filePath)

# 判断去掉最后一项后的路径是否等于目标路径
if parent_directory == target_directory:
    print(f"{filePath} 在 {target_directory} 目录下")
else:
    print(f"{filePath} 不在 {target_directory} 目录下")
