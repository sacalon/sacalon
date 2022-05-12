# -*- mode: python ; coding: utf-8 -*-


block_cipher = None

added_files = [
         ( 'src/hlib', 'hlib' )
]

a = Analysis(
    ['src\\hascal.py'],
    pathex=[],
    binaries=[],
    datas=added_files,
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          name='hascal',
          debug=False,
          strip=False,
          upx=True,
          runtime_tmpdir=None,
          console=True,
           )


coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='hascal',
)
