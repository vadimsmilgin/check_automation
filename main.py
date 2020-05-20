import os
import sys
import subprocess

command = 'ant retrieveUnpackaged'
command2 = 'ant retrieveSObjects'


def start():
    os.chdir('.\\sample')
    output = subprocess.run(command, shell=True)
    if output.returncode == 0:
        os.chdir('..\\')
        package_creator = subprocess.run([sys.executable, 'package_creator.py'], check=True)
        if package_creator.returncode == 0:
            os.chdir('.\\sample')
            output2 = subprocess.run(command2, shell=True)
            if output2.returncode == 0:
                os.chdir('..\\')
                error_validator = subprocess.run([sys.executable, 'error_validator.py'], check=True, stdout=subprocess.PIPE)
                print(error_validator.stdout.decode('utf-8'))


if __name__ == "__main__":
    start()
