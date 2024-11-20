import pexpect

# 启动 gdb
gdb_process = pexpect.spawn('/opt/riscv/bin/riscv64-unknown-elf-gdb')

# 等待 gdb 提示符
gdb_process.expect('(gdb)')

# 输入文件路径
gdb_process.sendline('file /mnt/hgfs/share/Riscv-SoC-Software/projects/rt-thread/test/build/test.elf')

# 等待 gdb 提示符
gdb_process.expect('(gdb)')

# 连接远程目标
gdb_process.sendline('target extended-remote :3333')

# 等待 gdb 提示符
gdb_process.expect('(gdb)')

# 执行监控命令
gdb_process.sendline('monitor reset halt')

# 等待 gdb 提示符
gdb_process.expect('(gdb)')

# 加载程序
gdb_process.sendline('load')

# 等待 gdb 提示符
gdb_process.expect('(gdb)')

# 继续执行
gdb_process.sendline('continue')

# 保持 gdb 进程运行
gdb_process.interact()
