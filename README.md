# PDF 去水印工具 · PDF Watermark Remover

[![Download](https://img.shields.io/badge/Download-最新版%20exe-2ea44f?style=for-the-badge)](https://github.com/XUAN1234567890987654321/pdf-watermark-remover/releases/latest)

> ⬇️ **下载 exe 点上面绿色按钮**，或到 [Releases](https://github.com/XUAN1234567890987654321/pdf-watermark-remover/releases/latest) 页面。

一个**离线、免安装、单文件**的 PDF 矢量水印去除工具。双击即用，无需 Python、无需联网。（小登第一次做东西，用大肥鱼跑的，感觉挺好用的就发出来了，多多包涵🙏😭）

> 用于去除 PDF 中以「矢量图形对象」形式绘制的水印——也就是水印本身是 PDF 里一段独立的绘图块，而非烙进图片像素里的那种。

## ✨ 特性

- 🖱️ **一键 / 拖拽**：双击选文件，或把 PDF 拖到程序图标上
- 📚 **批量处理**：一次处理多个文件
- 🔌 **零依赖**：单文件 exe，自带运行时，Windows 10/11 64 位直接运行
- 🛡️ **无损**：只删水印绘图块，正文、页码、图片原样保留
- 📄 **自动命名**：输出 `原名_去水印.pdf`，原文件不被改动

## 🚀 快速开始

1. 到 [**Releases**](https://github.com/XUAN1234567890987654321/pdf-watermark-remover/releases) 页面下载 exe
2. 双击运行：
   - **完整版**：点「添加 PDF」→「开始去水印」
   - **轻量版**：双击弹选择框，或直接把 PDF 拖到 exe 图标上
3. 处理结果保存在原文件同目录，文件名带 `_去水印`

> 首次运行若弹出 Windows SmartScreen「未知发布者」提示，点「更多信息 → 仍要运行」即可（本程序未做代码签名，属正常现象）。

## 📦 版本

> 两个版本功能一致，请到 [Releases](https://github.com/XUAN1234567890987654321/pdf-watermark-remover/releases) 页面下载 exe。

| 文件 | 说明 |
| --- | --- |
| `PDF-Watermark-Remover-Full.exe`（完整版） | 按钮式窗口界面，带文件列表与日志 |
| `PDF-Watermark-Remover-Lite.exe`（轻量版） | 无窗口，双击选文件 / 拖拽即处理 |

## 🖥️ 命令行

```bash
# 两个版本都支持
PDF去水印工具_完整版.exe --cli 输入.pdf [输出.pdf]
PDF去水印工具_轻量版.exe --cli 输入.pdf [输出.pdf]
```

## 🔧 工作原理

水印在 PDF 内部是一段标记为 `Watermark` 的绘图块（`/Artifact <</Subtype/Watermark …>> BDC … EMC`）。

程序解析每一页的内容流，将这段绘图块精确删除，其它内容一律不动。

## ⚠️ 局限

- 只能去除**矢量水印**（PDF 中以独立图形对象绘制的水印）
- 无法去除**已烙进图片像素**的水印（例如扫描件照片上的印章、截图水印），这类需要图像处理工具（如 Photoshop）

## 🧱 目录结构

```
.
├── watermark_tool_gui.py   # 完整版（按钮界面）源码
├── watermark_tool.py       # 轻量版（拖拽）源码
├── LICENSE
└── README.md
```

> 可执行文件（exe）统一放在 [Releases](https://github.com/XUAN1234567890987654321/pdf-watermark-remover/releases) 页面下载，不随源码仓库分发。

## 🛠️ 自行构建

依赖：Python 3.11+、`pypdf`、`pyinstaller`

```bash
pip install pypdf pyinstaller
pyinstaller --onefile --windowed watermark_tool_gui.py   # 完整版
pyinstaller --onefile --windowed watermark_tool.py       # 轻量版
```

## ⚖️ 许可

[MIT](LICENSE)

## 📌 声明

本工具仅用于处理**你有权编辑的文档**。请遵守相关法律法规及你所使用软件的服务协议。
