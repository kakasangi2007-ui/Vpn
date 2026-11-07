# -*- mode: python ; coding: utf-8 -*-
import glob
import os
from PyInstaller.utils.hooks import collect_submodules, copy_metadata

# 1. تمام زیرماژول‌های ezsynth را به صورت پویا جمع‌آوری کن
hiddenimports = collect_submodules('ezsynth')

# 2. لیست جبرانی واردسازی‌های پویا (تمام ماژول‌هایی که Ezsynth ممکن است به صورت پویا استفاده کند)
hiddenimports += [
    # --- پایه و ابزارها ---
    'numpy', 'numpy.core', 'numpy.core._multiarray_umath', 'numpy.core._methods',
    'numpy.lib.format', 'numpy.random.common', 'numpy.random.bounded_integers',
    'numpy.random.entropy',
    'tqdm', 'tqdm.auto', 'tqdm.std',
    
    # --- پردازش تصویر و بینایی کامپیوتر ---
    'cv2',
    'PIL', 'PIL.Image', 'PIL.ImageOps',
    
    # --- محاسبات علمی ---
    'scipy', 'scipy.ndimage', 'scipy.signal',
    
    # --- یادگیری عمیق و جریان نوری (هسته اصلی Ezsynth) ---
    'torch', 'torch.nn', 'torch.nn.functional', 'torch.utils', 'torch.utils.data',
    'torchvision', 'torchvision.transforms',
    'kornia', 'kornia.filters', 'kornia.geometry',
    'phycv',  # Ezsynth برای تشخیص لبه PAGE/PST از آن استفاده می‌کند
    
    # --- سایر کتابخانه‌های کمکی که ممکن است استفاده شوند ---
    'matplotlib', 'matplotlib.pyplot',
    'imageio', 'imageio.v2',
    'skimage', 'sklearn', # برخی کدهای جریان نوری ممکن است به آن وابسته باشند
]

# 3. فایل‌های dll کتابخانه numpy را به صورت دستی بسته‌بندی کن
numpy_datas = []
try:
    import numpy
    numpy_libs_path = os.path.abspath(os.path.join(os.path.dirname(numpy.__file__), '..', 'numpy.libs'))
    if os.path.isdir(numpy_libs_path):
        for f in glob.glob(os.path.join(numpy_libs_path, '*')):
            numpy_datas.append((f, 'numpy.libs'))
except Exception:
    pass

# 4. متادیتای tqdm را کپی کن (جلوگیری از خطای PackageNotFound در زمان اجرا)
tqdm_datas = []
try:
    tqdm_datas += copy_metadata('tqdm')
except Exception:
    pass

# 5. فایل‌های dll کتابخانه torch را جمع‌آوری کن (اختیاری اما برای اطمینان از بارگذاری torch مفید است)
torch_datas = []
try:
    import torch
    torch_lib_path = os.path.join(os.path.dirname(torch.__file__), 'lib')
    if os.path.isdir(torch_lib_path):
        for f in glob.glob(os.path.join(torch_lib_path, '*.dll')):
            torch_datas.append((f, 'torch/lib'))
except Exception:
    pass

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[
        # فایل‌های اصلی Ezsynth
        ('ezsynth_lib/ezsynth', 'ezsynth_lib/ezsynth'),
        ('ezsynth_lib/ezsynth/utils/flow_utils/ef_raft_models', 'ezsynth_lib/ezsynth/utils/flow_utils/ef_raft_models'),
    ] + numpy_datas + tqdm_datas + torch_datas,
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
