**简体中文 | [English](README.md)**
<div id="top"></div>

[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![License][license-shield]][license-url]


<!-- PROJECT LOGO -->
<br />
<div align="center">
    <a href="https://github.com/MoonGrt/Riscv-SoC-Software">
    <img src="Document/images/logo.png" alt="Logo" width="80" height="80">
    </a>
<h3 align="center">Riscv-SoC-Software</h3>
    <p align="center">
    项目简介
    <br />
    <a href="https://github.com/MoonGrt/Riscv-SoC-Software"><strong>浏览文档 »</strong></a>
    <br />
    <a href="https://github.com/MoonGrt/Riscv-SoC-Software">查看 Demo</a>
    ·
    <a href="https://github.com/MoonGrt/Riscv-SoC-Software/issues">反馈 Bug</a>
    ·
    <a href="https://github.com/MoonGrt/Riscv-SoC-Software/issues">请求新功能</a>
    </p>
</div>




<!-- CONTENTS -->
<details open>
  <summary>目录</summary>
  <ol>
    <li><a href="#文件树">文件树</a></li>
    <li>
      <a href="#关于本项目">关于本项目</a>
      <ul>
      </ul>
    </li>
    <li><a href="#贡献">贡献</a></li>
    <li><a href="#许可证">许可证</a></li>
    <li><a href="#联系我们">联系我们</a></li>
    <li><a href="#致谢">致谢</a></li>
  </ol>
</details>





<!-- 文件树 -->
## 文件树

```
└─ Project
  ├─ .gitignore
  ├─ README.md
  ├─ /projects/
  │ ├─ /freertos/
  │ ├─ /rt-thread/
  │ ├─ /bare/
  │ └─ /pika-python/
  ├─ /.vscode/
  ├─ /GUI/
  │ ├─ DVPConf.py
  │ ├─ Sim_test.py
  │ ├─ IDE.py
  │ ├─ GPIOConf.py
  │ ├─ NewPro.py
  │ ├─ RISCVSimulator.py
  │ └─ /RISCVSim/
  ├─ /Document/
  │ └─ Cyber.scala
  ├─ /scripts/
  │ ├─ openocd
  │ ├─ cyber.yaml
  │ └─ cyber.cfg
  └─ /Workspace/
    ├─ /demo/
    │ ├─ Makefile
    │ ├─ link.lds
    │ ├─ Cyber.v
    │ ├─ /libs/
    │ │ ├─ cyber.h
    │ │ ├─ gpio.c
    │ │ ├─ gpio.h
    │ │ ├─ tim.c
    │ │ └─ tim.h
    │ ├─ /rt-thread/
    │ │ ├─ /components/
    │ │ │ ├─ /finsh/
    │ │ │ └─ /dfs/
    │ │ │   ├─ dfs.c
    │ │ │   └─ dfs.h
    │ │ ├─ /include/
    │ │ │ ├─ rtdef.h
    │ │ │ ├─ rthw.h
    │ │ │ ├─ rtservice.h
    │ │ │ ├─ rtthread.h
    │ │ │ └─ types.h
    │ │ ├─ /libcpu/
    │ │ │ ├─ context_gcc.S
    │ │ │ ├─ stack.c
    │ │ │ ├─ trap.c
    │ │ │ └─ trap_entry.S
    │ │ └─ /src/
    │ ├─ /user/
    │ │ ├─ main.c
    │ │ ├─ rtconfig.h
    │ │ └─ start.S
    │ └─ /build/
    └─ /test/

```



<!-- 关于本项目 -->
## 关于本项目

<p style="-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><br /></p></body></html>
<p align="right">(<a href="#top">top</a>)</p>



<!-- 贡献 -->
## 贡献

贡献让开源社区成为了一个非常适合学习、互相激励和创新的地方。你所做出的任何贡献都是**受人尊敬**的。

如果你有好的建议，请复刻（fork）本仓库并且创建一个拉取请求（pull request）。你也可以简单地创建一个议题（issue），并且添加标签「enhancement」。不要忘记给项目点一个 star！再次感谢！

1. 复刻（Fork）本项目
2. 创建你的 Feature 分支 (`git checkout -b feature/AmazingFeature`)
3. 提交你的变更 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到该分支 (`git push origin feature/AmazingFeature`)
5. 创建一个拉取请求（Pull Request）
<p align="right">(<a href="#top">top</a>)</p>



<!-- 许可证 -->
## 许可证

根据 MIT 许可证分发。打开 [LICENSE](LICENSE) 查看更多内容。
<p align="right">(<a href="#top">top</a>)</p>



<!-- 联系我们 -->
## 联系我们

MoonGrt - 1561145394@qq.com
Project Link: [MoonGrt/Riscv-SoC-Software](https://github.com/MoonGrt/Riscv-SoC-Software)

<p align="right">(<a href="#top">top</a>)</p>



<!-- 致谢 -->
## 致谢

* [Choose an Open Source License](https://choosealicense.com)
* [GitHub Emoji Cheat Sheet](https://www.webpagefx.com/tools/emoji-cheat-sheet)
* [Malven's Flexbox Cheatsheet](https://flexbox.malven.co/)
* [Malven's Grid Cheatsheet](https://grid.malven.co/)
* [Img Shields](https://shields.io)
* [GitHub Pages](https://pages.github.com)
* [Font Awesome](https://fontawesome.com)
* [React Icons](https://react-icons.github.io/react-icons/search)
<p align="right">(<a href="#top">top</a>)</p>




<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[contributors-shield]: https://img.shields.io/github/contributors/MoonGrt/Riscv-SoC-Software.svg?style=for-the-badge
[contributors-url]: https://github.com/MoonGrt/Riscv-SoC-Software/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/MoonGrt/Riscv-SoC-Software.svg?style=for-the-badge
[forks-url]: https://github.com/MoonGrt/Riscv-SoC-Software/network/members
[stars-shield]: https://img.shields.io/github/stars/MoonGrt/Riscv-SoC-Software.svg?style=for-the-badge
[stars-url]: https://github.com/MoonGrt/Riscv-SoC-Software/stargazers
[issues-shield]: https://img.shields.io/github/issues/MoonGrt/Riscv-SoC-Software.svg?style=for-the-badge
[issues-url]: https://github.com/MoonGrt/Riscv-SoC-Software/issues
[license-shield]: https://img.shields.io/github/license/MoonGrt/Riscv-SoC-Software.svg?style=for-the-badge
[license-url]: https://github.com/MoonGrt/Riscv-SoC-Software/blob/master/LICENSE

