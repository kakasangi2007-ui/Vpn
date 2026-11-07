# -*- mode: python ; coding: utf-8 -*-
import glob
import os
import sys
from PyInstaller.utils.hooks import collect_submodules

# دریافت زیرماژول‌های ezsynth به صورت پویا
hiddenimports = collect_submodules('ezsynth')

# واردکردن مخفی اجباری numpy و زیرماژول‌های کلیدی آن (جلوگیری از خطای "No module named numpy" هنگام اجرا)
hiddenimports += [
    'numpy',
    'numpy.core',
    'numpy.core._multiarray_umath',
    'numpy.core._methods',
    'numpy.lib.format',
    'numpy.random.common',
    'numpy.random.bounded_integers',
    'numpy.random.entropy',
]

# بسته‌بندی فایل‌های dll کتابخانه numpy (در غیر این صورت حتی اگر ماژول پیدا شود، بارگذاری کتابخانه همچنان شکست می‌خورد)
numpy_datas = []
try:
    import numpy
    numpy_libs_path = os.path.join(os.path.dirname(numpy.__file__), '..', 'numpy.libs')
    numpy_libs_path = os.path.abspath(numpy_libs_path)
    if os.path.isdir(numpy_libs_path):
        for f in glob.glob(os.path.join(numpy_libs_path, '*')):
            numpy_datas.append((f, 'numpy.libs'))
except Exception:
    pass

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('ezsynth_lib/ezsynth', 'ezsynth_lib/ezsynth'),
        ('ezsynth_lib/ezsynth/utils/flow_utils/ef_raft_models', 'ezsynth_lib/ezsynth/utils/flow_utils/ef_raft_models'),
    ] + numpy_datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
)
pyz = PYZ(a.pure)
exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='VideoToAnime',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
)
