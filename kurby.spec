# -*- mode: python ; coding: utf-8 -*-
import os
from pathlib import Path

block_cipher = None


a = Analysis(['kurby.py'],
             # pathex=['/home/alain/local/workspace/perso/kurby'],
             binaries=[],
             datas=[],
             hiddenimports=["dataclasses", "typer", "typer-cli", "httpx", "Faker", "Js2Py", "pydantic", "fuzzywuzzy", "numpy", "tqdm", "tenacity", "arrow"],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          [],
          name='kurby',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=True )
