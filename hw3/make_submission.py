#!/usr/bin/python3

import os
from zipfile import ZipFile
import glob
import sys

if len(sys.argv) == 3:
    tz1 = sys.argv[1]
    tz2 = sys.argv[2]
else:
    tz1 = input("Enter the first Teudat Zehut: ")
    tz2 = input("Enter the second Teudat Zehut: ")


code_files = glob.glob('*.c') + glob.glob('*.cpp') + glob.glob('*.hpp') + ['parser.ypp', 'scanner.lex']
removes = glob.glob('parser.tab.*pp') + glob.glob('lex.yy.c')
for remove in removes:
    code_files.remove(remove)

zipname = f'{tz1}-{tz2}.zip'
if os.path.exists(zipname):
    os.remove(zipname)
    print('Cleaned up old submission zip')

zf = ZipFile(zipname, mode='w')
print('Filename is:', zipname)
print('Including:')
for fn in code_files:
    print(f'- {fn}')
    zf.write(fn)

print('Prepared submission file')
