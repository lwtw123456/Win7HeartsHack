# Win7HeartsHack

> 🎯 一个针对 **Windows 7 64 位版《红心大战》(Hearts.exe)** 的学习型修改器项目。
> 主要用于 **逆向工程 / 内存分析 / Windows API / Tkinter GUI** 的研究与交流。

⚠️ **本项目仅用于技术学习与研究，请勿用于任何商业用途或破坏他人环境。**

---

## ✨ 功能特性

当前版本实现了以下功能（部分基于内存修改，部分基于代码注入）：

- ⚡ **直接获胜**
- 🔓 **自由模式（无视出牌规则）**
- 👁️‍🗨️ **透视模式（显示对手手牌）**
- 👀 **明牌模式（对手直接明牌）**
- 👑 **自定模式（直接自定义手牌）**
- 🧲 **全收模式（出啥都全收所有牌）**
- 🛡️ **无敌模式（收牌不计分+直接击中月亮）**
- 🤪 **降智模式（重写了AI，只会遵循弱智套路）**

GUI 使用 **Tkinter** 构建，操作直观。

---

## 🧱 项目结构

```text
.
├── main.py                  # 程序入口
├── controller.py            # 主控制器
├── override_ai.c            # 重写的AI
├── ui.py                    # UI 界面定义
├── heartshack.py            # 核心修改逻辑
├── cardselector.py          # 简易的选牌界面
├── memoryeditor.py          # 通用内存编辑引擎
├── win_api.py               # Windows API / ctypes 封装
└── README.md
```

---

## 🔧 运行环境

- Python 3.8+

### Python 依赖

```bash
pip install pymem
```

---

## ▶️ 使用方法
1. 编译dll并放在同一目录
```bash
gcc -shared -o override_ai.dll override_ai.c -O2
```
2. 运行红心大战
3. 启动本程序
```bash
python main.py
```

---

## 🧠 技术点说明

本项目涉及但不限于以下技术：

- Windows 进程内存读写（`pymem`）
- 指针链计算
- 特征码扫描（AOB Scan）
- 内存保护修改（`VirtualProtectEx`）
- Shellcode 注入
- DLL注入
- Windows API（User32 / GDI / Kernel32 / psapi）
- Tkinter GUI

非常适合作为：

> 🔍 **Windows 游戏逆向 / Python Hack Tool 入门项目**

---

## ⚠️ 注意事项

- **仅支持 Win7 64 位版红心大战**
- 杀毒软件可能会误报（涉及内存操作）
- 请勿用于任何比赛、排行或破坏他人数据

---

## 📜 免责声明

本项目 **仅用于学习与研究目的**。  
因使用本程序造成的任何后果，作者概不负责。

如果你用于：

- 逆向工程学习 ✅
- Windows 内存机制研究 ✅
- Python + WinAPI 学习 ✅

那非常欢迎 👍

---

## 📄 开源协议

本项目基于 MIT License
开源，可自由用于个人或商业用途，但需保留版权声明。

---

## ⭐ Star

如果你觉得这个项目对你有帮助，欢迎 Star ⭐  
也欢迎 Fork / PR / Issue 交流实现思路。

---

**Enjoy reverse engineering! 🧠🔥**
