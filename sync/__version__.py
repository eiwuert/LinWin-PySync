from subprocess import check_output

VERSION_STRING = '1.6.1b3'

try:
    git_version = check_output(['git', 'log']).split('\n')[0].split(' ')[1]
except:
    git_version = 'N/A'
