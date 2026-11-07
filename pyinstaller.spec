# -*- mode: python ; coding: utf-8 -*-
import glob
import os
from PyInstaller.utils.hooks import collect_submodules, copy_metadata

# --- 1. زیرماژول‌های ezsynth ---
hiddenimports = collect_submodules('ezsynth')

# --- 2. واردسازی‌های پویا ---
hiddenimports += [
    'numpy', 'numpy.core', 'numpy.core._multiarray_umath', 'numpy.core._methods',
    'numpy.lib.format', 'numpy.random.common', 'numpy.random.bounded_integers',
    'numpy.random.entropy',
    'tqdm', 'tqdm.auto', 'tqdm.std',
    'cv2',
    'PIL', 'PIL.Image', 'PIL.ImageOps',
    'scipy', 'scipy.ndimage', 'scipy.signal',
    'torch', 'torch.nn', 'torch.nn.functional', 'torch.utils', 'torch.utils.data',
    'torchvision', 'torchvision.transforms', 'torchvision.ops',
    'torchvision._C',
    'kornia', 'kornia.filters', 'kornia.geometry',
    'phycv',
    'matplotlib', 'matplotlib.pyplot',
    'imageio', 'imageio.v2',
    'skimage', 'sklearn',
]

# --- 3. dllهای numpy ---
numpy_datas = []
try:
    import numpy
    numpy_libs_path = os.path.abspath(os.path.join(os.path.dirname(numpy.__file__), '..', 'numpy.libs'))
    if os.path.isdir(numpy_libs_path):
        for f in glob.glob(os.path.join(numpy_libs_path, '*')):
            numpy_datas.append((f, 'numpy.libs'))
except Exception:
    pass

# --- 4. متادیتای tqdm ---
tqdm_datas = []
try:
    tqdm_datas += copy_metadata('tqdm')
except Exception:
    pass

# --- 5. پسوند و کتابخانه‌های torchvision ---
torchvision_datas = []
try:
    import torchvision
    tv_path = os.path.dirname(torchvision.__file__)
    for f in glob.glob(os.path.join(tv_path, '*.pyd')):
        torchvision_datas.append((f, 'torchvision'))
    for f in glob.glob(os.path.join(tv_path, '*.dll')):
        torchvision_datas.append((f, 'torchvision'))
    tv_libs = os.path.abspath(os.path.join(tv_path, '..', 'torchvision.libs'))
    if os.path.isdir(tv_libs):
        for f in glob.glob(os.path.join(tv_libs, '*')):
            torchvision_datas.append((f, 'torchvision.libs'))
except Exception:
    pass

# --- 6. dllهای torch ---
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
        ('ezsynth_lib/ezsynth', 'ezsynth_lib/ezsynth'),
        ('ezsynth_lib/ezsynth/utils/flow_utils/ef_raft_models', 'ezsynth_lib/ezsynth/utils/flow_utils/ef_raft_models'),
    ] + numpy_datas + tqdm_datas + torchvision_datas + torch_datas,
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
