import PyInstaller.__main__


PyInstaller.__main__.run([
    '--name=' + 'GrelhaPy',
    '--onefile',
    '--console',
    '--icon=''gpy.ico',
    'GrelhaPy.py'
])