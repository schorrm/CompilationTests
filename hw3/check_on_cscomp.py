#!/usr/bin/python3
from jumpssh import SSHSession # we need this for establishing the SSH
import getpass
import glob

username = input("Username: ")
password = getpass.getpass()

csl3 = 'csl3.cs.technion.ac.il'
cscomp = 'cscomp.cs.technion.ac.il'

CDDIR = 'cd CompilationTests/hw3; ' 

print('Establishing client through csl3 bridge')
gateway_session = SSHSession(csl3, username, password=password)
print('Established bridge. Connecting to remote.')
remote_session = gateway_session.get_remote_session(cscomp, password=password)
print('Connected to remote.')

testdir_exists = remote_session.exists('CompilationTests')
if testdir_exists:
    print('Test dir found')
else:
    print('Test dir not found')
    exit(0)


zips = glob.glob('[0-9]*-[0-9]*.zip')
if not zips:
    print('Submission not found!')
    exit(0)
sub_zip = zips[0]
print(f'File: {sub_zip}')
remote_session.put(sub_zip, f'/home/{username}/CompilationTests/hw3/{sub_zip}')
print('Copied file to remote')

print('Current dir:', remote_session.get_cmd_output('pwd'))
print('Going to hw3 dir')
print(remote_session.get_cmd_output(f'{CDDIR} pwd'))
# print('Current dir:', remote_session.get_cmd_output('pwd'))
print('Updating tests (git pull):')
print(remote_session.get_cmd_output(f'{CDDIR} git pull'))
print('running the official self-check:')
print(remote_session.get_cmd_output(f'{CDDIR} sh selfcheck-hw3 {sub_zip}'))
print("Unzipping")
print(remote_session.get_cmd_output(f'{CDDIR} unzip -o {sub_zip}'))
print("running Moshe's tests:")
print(remote_session.get_cmd_output(f'{CDDIR} python3.6 tests.py'))
print('Done')