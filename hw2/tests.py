#!/usr/bin/python3

try:
    from tqdm import trange
except ImportError:
    trange = range

import random
import subprocess
import os
from pathlib import Path
import pickle
import glob
from itertools import zip_longest
import argparse


class fg:
    black = '\033[30m'
    red = '\033[31m'
    green = '\033[32m'
    orange = '\033[33m'
    blue = '\033[34m'
    purple = '\033[35m'
    cyan = '\033[36m'
    lightgrey = '\033[37m'
    darkgrey = '\033[90m'
    lightred = '\033[91m'
    lightgreen = '\033[92m'
    yellow = '\033[93m'
    lightblue = '\033[94m'
    pink = '\033[95m'
    lightcyan = '\033[96m'
    end = '\033[00m'


valid_output = b'''rm -f lex.yy.c
rm -f parser.tab.*pp
rm -f hw2
flex scanner.lex
bison -d parser.ypp
g++ -std=c++11 -o hw2 *.c *.cpp
'''


def chunk_lines(lst, n):
    text = ''
    for i in range(0, len(lst), n):
        text += ' '.join(lst[i:i + n]) + '\n'
    return text


def test_validate(testname: str, results1: str, results2: str):
    if (results1 == results2):
        print(f'{testname}: {fg.green}pass{fg.end}')
    else:
        print(f'{testname}: {fg.red}fail{fg.end}')


def log_and_exit(input, o1, o2):
    for i, (l1, l2) in enumerate(zip_longest(o1.splitlines(), o2.splitlines())):
        if l1 != l2:
            print(f'Line #{i}')
            print('Got:')
            print(l1)
            print('Expected:')
            print(l2)
            exit(0)


parser = argparse.ArgumentParser(description='Run the test suite.')

parser.add_argument('-l', '--log', action='store_true', help="Print the first differing file-line and exit")
args = parser.parse_args()


random.seed(12345)

print('Compiling')

chk1 = subprocess.check_output(['make'])
if chk1 != valid_output:
    print('Compilation Error!')
    print(str(chk1))
    exit(1)

EXE = './hw2'

outputs = {}
inputs = {}


for filename in sorted(glob.glob('tests/*.in')):
    filename = filename.split('.')[0]
    pretty = filename.split('/')[1]
    print(f'Running test - {pretty}')

    with open(f'{filename}.in') as f:
        sample = f.read()

    with open(f'{filename}.out') as f:
        output_check = f.read()

    final_line = output_check.splitlines()[-1]
    tst_err = 'error' in final_line
    try:
        output = subprocess.check_output(EXE, input=sample, encoding='utf-8', shell=True)
    except subprocess.CalledProcessError as e:
        if tst_err and e.returncode == 1:
            print(f'Program exited with error code ({e.returncode}) -- this is {fg.green}correct{fg.end}!')
        else:
            print(f'{fg.red}Program exited with error code ({e.returncode}){fg.end}')
        output = e.output

    test_validate('Result', output, output_check)
    if output != output_check:
        if args.log:
            log_and_exit(sample, output, output_check)
