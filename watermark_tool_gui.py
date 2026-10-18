# -*- coding: utf-8 -*-
"""
PDF 去水印工具（完整版 / 按钮界面）
==================================
有窗口、有按钮、有文件列表、有日志区。体积约 30 MB。

用法：
  1. 双击运行 → 窗口 → 「添加 PDF」→「开始去水印」
  2. 命令行： PDF去水印工具_完整版.exe --cli 输入.pdf [输出.pdf]

说明：
  只能去除「矢量水印」（WPS 等工具导出的斜印文字/图形）。
  烙进扫描图/图片像素里的水印去不掉。
"""

import os
import re
import sys

from pypdf import PdfReader, PdfWriter
from pypdf.generic import NameObject

PATTERN = re.compile(
    rb"/Artifact\s*<</[^>]*Subtype/Watermark[^>]*>>\s*BDC.*?EMC\s*",
    re.S,
)


def remove_watermark(src, dst):
    reader = PdfReader(src)
    writer = PdfWriter()
    removed_total = 0
    for page in reader.pages:
        cs = page.get_contents()
        if cs is None:
            writer.add_page(page)
            continue
        data = cs.get_data()
        removed_total += len(PATTERN.findall(data))
        cs.set_data(PATTERN.sub(b"", data))
        page[NameObject("/Contents")] = cs
        writer.add_page(page)
    with open(dst, "wb") as fh:
        writer.write(fh)
    return removed_total, len(reader.pages)


def auto_dst(src):
    folder, name = os.path.split(src)
    stem, ext = os.path.splitext(name)
    out = os.path.join(folder, stem + "_去水印" + ext)
    i = 1
    while os.path.exists(out):
        out = os.path.join(folder, f"{stem}_去水印_{i}{ext}")
        i += 1
    return out


def run_gui():
    import tkinter as tk
    from tkinter import filedialog, messagebox, scrolledtext

    root = tk.Tk()
    root.title("PDF 去水印工具（完整版）")
    root.geometry("720x560")

    files = []

    top = tk.Label(root, text="PDF 去水印工具", font=("Microsoft YaHei", 16, "bold"))
    top.pack(pady=(12, 2))
    sub = tk.Label(
        root,
        text="去掉 WPS 等工具导出的矢量水印（斜印文字/图形）。扫描图里烙进去的水印去不掉。",
        font=("Microsoft YaHei", 9), fg="#666",
    )
    sub.pack(pady=(0, 8))

    listbox = tk.Listbox(root, height=8, font=("Microsoft YaHei", 10))
    listbox.pack(fill="x", padx=16)

    bar = tk.Frame(root)
    bar.pack(fill="x", padx=16, pady=8)
    tk.Button(bar, text="添加 PDF", width=14, command=lambda: add_files()).pack(side="left", padx=4)
    tk.Button(bar, text="清空列表", width=14, command=lambda: clear_files()).pack(side="left", padx=4)
    tk.Button(bar, text="开始去水印", width=16, bg="#2f74b5", fg="white",
              command=lambda: start()).pack(side="left", padx=4)

    log = scrolledtext.ScrolledText(root, height=14, font=("Consolas", 9), state="disabled")
    log.pack(fill="both", expand=True, padx=16, pady=(4, 12))

    def _log(msg):
        log.configure(state="normal")
        log.insert("end", msg + "\n")
        log.see("end")
        log.configure(state="disabled")

    def add_files():
        picked = filedialog.askopenfilenames(
            title="选择 PDF", filetypes=[("PDF 文件", "*.pdf"), ("所有文件", "*.*")]
        )
        for p in picked:
            if p not in files:
                files.append(p)
                listbox.insert("end", os.path.basename(p))
        _log(f"已添加 {len(picked)} 个文件")

    def clear_files():
        files.clear()
        listbox.delete(0, "end")
        _log("列表已清空")

    def start():
        if not files:
            messagebox.showwarning("提示", "请先添加 PDF 文件")
            return
        ok = 0
        for p in list(files):
            try:
                dst = auto_dst(p)
                removed, pages = remove_watermark(p, dst)
                _log(f"✓ {os.path.basename(p)}  ({pages}页, 去水印{removed}处)")
                ok += 1
            except Exception as e:  # noqa
                _log(f"✗ {os.path.basename(p)}  失败: {e}")
        _log(f"完成：成功 {ok}/{len(files)}")
        files.clear()
        listbox.delete(0, "end")
        messagebox.showinfo("完成", f"成功处理 {ok} 个文件。\n输出在原文件同目录，文件名带 _去水印。")

    root.mainloop()


if __name__ == "__main__":
    args = sys.argv[1:]
    if len(args) >= 2 and args[0] == "--cli":
        src = args[1]
        if not os.path.exists(src):
            print("找不到文件: " + src)
            sys.exit(1)
        dst = args[2] if len(args) > 2 else auto_dst(src)
        removed, pages = remove_watermark(src, dst)
        print(f"OK pages={pages} removed={removed} -> {dst}")
        sys.exit(0)
    run_gui()
