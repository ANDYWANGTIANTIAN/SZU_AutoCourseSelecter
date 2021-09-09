# -*- mode: python ; coding: utf-8 -*-

import sys
import os.path as osp
sys.setrecursionlimit(5000)

SETUP_DIR = 'E:\\SZU_AutoCourseSelecter\\'
block_cipher = None


a = Analysis(['main.py'],
             pathex=['E:\\SZU_AutoCourseSelecter'],
             binaries=[],
             datas=[(SETUP_DIR+'image','image')],
             hiddenimports=[],
             hookspath=[],
             hooksconfig={},
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
          [],
          exclude_binaries=True,
          name='main',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          console=False,
          disable_windowed_traceback=False,
          target_arch=None,
          codesign_identity=None,
          entitlements_file=None, icon='E:\\SZU_AutoCourseSelecter\\image\\favicon.ico' )
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas, 
               strip=False,
               upx=True,
               upx_exclude=[],
               name='main')
