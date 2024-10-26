import subprocess, sys, time

# /home/moon/openocd_riscv/src/openocd -f /mnt/hgfs/share/Riscv-SoC-Software/scripts/cyber.cfg

def openocd_connect():
    """启动 OpenOCD 以连接到开发板"""
    try:
        # 启动 OpenOCD
        openocd_cmd = ['/home/moon/openocd_riscv/src/openocd', '-f', '/mnt/hgfs/share/Riscv-SoC-Software/scripts/cyber.cfg']  # 修改为你的 OpenOCD 配置文件路径
        openocd_process = subprocess.Popen(openocd_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        # 等待 OpenOCD 启动
        time.sleep(3)  # 根据需要调整等待时间
        print("OpenOCD 已启动，连接到开发板中...")

        return openocd_process
    except Exception as e:
        print(f"启动 OpenOCD 失败: {e}")
        sys.exit(1)

def gdb_download(program_path):
    """使用 GDB 下载程序"""
    try:
        # 启动 GDB
        gdb_cmd = ["/opt/riscv/bin/riscv64-unknown-elf-gdb", program_path]  # 修改为你的 GDB 路径和程序文件
        gdb_process = subprocess.Popen(gdb_cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        # 发送 GDB 命令
        gdb_process.stdin.write(b"target extended-remote :3333\n")  # 连接到 OpenOCD 的 GDB 服务器
        gdb_process.stdin.write(b"load\n")  # 下载程序
        # gdb_process.stdin.write(b"monitor reset halt\n")
        # gdb_process.stdin.write(b"continue\n")
        gdb_process.stdin.write(b"\nquit\ny\n")  # 退出 GDB
        gdb_process.stdin.flush()

        # 获取输出
        stdout, stderr = gdb_process.communicate()
        print(stdout.decode())
        if stderr:
            print(stderr.decode())
    except Exception as e:
        print(f"下载程序失败: {e}")
        sys.exit(1)


if __name__ == "__main__":
    # openocd_process = openocd_connect()

    # input("按 Enter 键继续以下载程序...")
    program_path = "/mnt/hgfs/share/Riscv-SoC-Software/projects/rt-thread/demo7-finsh+/build/finsh.elf"  # 修改为你的程序文件路径
    gdb_download(program_path)

    # 确保在程序下载后结束 OpenOCD
    # openocd_process.terminate()
    # openocd_process.wait()
    # print("OpenOCD 已停止。")
