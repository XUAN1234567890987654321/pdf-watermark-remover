# -*- coding: utf-8 -*-
"""
PDF 去水印工具（轻量版）
======================
去掉 WPS 等工具导出的「Artifact 类型」矢量水印（斜着印在页面上的那种）。

用法：
  1. 把 PDF 文件拖到这个 exe 图标上  —— 自动处理并弹结果
  2. 双击 exe                        —— 弹出文件选择框
  3. 命令行：
       PDF去水印工具.exe --cli 输入.pdf [输出.pdf]    # 控制台输出
       PDF去水印工具.exe --silent 文件1.pdf 文件2.pdf # 无弹窗，自动处理（脚本用）

说明：
  只能去除「矢量水印」。烙进扫描图/图片像素里的水印去不掉。
"""

import ctypes
import os
import re
import sys
from ctypes import wintypes

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


def msgbox(text, title="PDF 去水印工具"):
    ctypes.windll.user32.MessageBoxW(0, text, title, 0x40)  # MB_ICONINFORMATION


def process_files(files):
    ok = 0
    fails = []
    for p in files:
        try:
            dst = auto_dst(p)
            removed, pages = remove_watermark(p, dst)
            ok += 1
        except Exception as e:  # noqa
            fails.append(f"{os.path.basename(p)}: {e}")
    lines = [f"完成：成功 {ok} / 共 {len(files)} 个"]
    if fails:
        lines.append("")
        lines.append("失败：")
        lines.extend(fails)
    lines.append("")
    lines.append("输出在原文件同目录，文件名带 _去水印。")
    return "\n".join(lines)


# ================= 文件选择框（Win32 原生） =================
class OPENFILENAME(ctypes.Structure):
    _fields_ = [
        ("lStructSize", wintypes.DWORD),
        ("hwndOwner", wintypes.HWND),
        ("hInstance", wintypes.HINSTANCE),
        ("lpstrFilter", wintypes.LPCWSTR),
        ("lpstrCustomFilter", wintypes.LPWSTR),
        ("nMaxCustFilter", wintypes.DWORD),
        ("nFilterIndex", wintypes.DWORD),
        ("lpstrFile", wintypes.LPWSTR),
        ("nMaxFile", wintypes.DWORD),
        ("lpstrFileTitle", wintypes.LPWSTR),
        ("nMaxFileTitle", wintypes.DWORD),
        ("lpstrInitialDir", wintypes.LPCWSTR),
        ("lpstrTitle", wintypes.LPCWSTR),
        ("Flags", wintypes.DWORD),
        ("nFileOffset", wintypes.WORD),
        ("nFileExtension", wintypes.WORD),
        ("lpstrDefExt", wintypes.LPCWSTR),
        ("lCustData", wintypes.LPARAM),
        ("lpfnHook", ctypes.c_void_p),
        ("lpTemplateName", wintypes.LPCWSTR),
    ]


def pick_pdfs():
    buf = ctypes.create_unicode_buffer(0x8000)
    ofn = OPENFILENAME()
    ofn.lStructSize = ctypes.sizeof(OPENFILENAME)
    ofn.lpstrFilter = "PDF 文件\0*.pdf\0所有文件\0*.*\0"
    ofn.lpstrFile = ctypes.cast(buf, wintypes.LPWSTR)
    ofn.nMaxFile = 0x8000
    ofn.Flags = 0x00080200 | 0x00001000 | 0x00000800 | 0x00000008
    ofn.lpstrTitle = "选择要去水印的 PDF（可多选）"
    ok = ctypes.windll.comdlg32.GetOpenFileNameW(ctypes.byref(ofn))
    if not ok:
        return []
    raw = ctypes.string_at(ctypes.cast(buf, ctypes.c_void_p), ctypes.sizeof(buf))
    text = raw.decode("utf-16-le", errors="ignore")
    parts = [p for p in text.split("\x00") if p]
    if not parts:
        return []
    if len(parts) == 1:
        return parts
    return [os.path.join(parts[0], p) for p in parts[1:]]


# ================= 命令行 / 静默 =================
def run_cli(args):
    if len(args) < 1:
        print("用法: --cli 输入.pdf [输出.pdf]")
        return 2
    src = args[0]
    dst = args[1] if len(args) > 1 else auto_dst(src)
    if not os.path.exists(src):
        print("找不到文件: " + src)
        return 1
    removed, pages = remove_watermark(src, dst)
    print(f"OK pages={pages} removed={removed} -> {dst}")
    return 0


def run_silent(files):
    code = 0
    for p in files:
        if not os.path.exists(p):
            code = 1
            continue
        try:
            remove_watermark(p, auto_dst(p))
        except Exception:
            code = 1
    return code


def main():
    argv = sys.argv[1:]
    if not argv:
        files = pick_pdfs()
        if not files:
            return 0
        msgbox(process_files(files))
        return 0
    if argv[0] == "--cli":
        return run_cli(argv[1:])
    if argv[0] == "--silent":
        return run_silent(argv[1:])
    # 拖拽进来的文件路径
    msgbox(process_files(argv))
    return 0


if __name__ == "__main__":
    sys.exit(main())
