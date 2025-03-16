import os

def upload_program(ttyPath: str):
    os.system(f'ampy --port {ttyPath} run ./client/client.py')

if __name__ == '__main__':
    upload_program(input('Serial Port: '))
