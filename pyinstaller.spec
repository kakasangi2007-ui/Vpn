# -*- mode: python ; coding: utf-8 -*-

from PyInstaller.utils.hooks import collect_submodules

hiddenimports = collect_submodules('ezsynth')

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('ezsynth_lib/ezsynth', 'ezsynth_lib/ezsynth'),   # کل پکیج ezsynth
        # مدل‌های EF_RAFT در حین build داخل این مسیر قرار می‌گیرند
        ('ezsynth_lib/ezsynth/utils/flow_utils/ef_raft_models', 'ezsynth_lib/ezsynth/utils/flow_utils/ef_raft_models'),
    ],
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
    console=False,   # چون GUI داریم، کنسول مخفی باشد
)
