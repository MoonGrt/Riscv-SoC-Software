Need the prebuild GCC from https://www.sifive.com/products/tools/   =>   SiFive GNU Embedded Toolchain

The makefiles are expecting to find this prebuild version in /opt/riscv/__contentOfThisPreBuild__

```sh
version=riscv64-unknown-elf-gcc-8.3.0-2019.08.0-x86_64-linux-ubuntu14
wget -O riscv64-unknown-elf-gcc.tar.gz riscv https://static.dev.sifive.com/dev-tools/$version.tar.gz
tar -xzvf riscv64-unknown-elf-gcc.tar.gz
sudo mv $version /opt/riscv
echo 'export PATH=/opt/riscv/bin:$PATH' >> ~/.bashrc
```
