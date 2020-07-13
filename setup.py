import PyInstaller.__main__


PyInstaller.__main__.run([
    '--name=' + 'GrelhaPy',
    '--onefile',
    '--windowed',
    '--icon=''gpy.ico',
    'GrelhaPy.py'
])