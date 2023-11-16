import os

try:
    command = "taskkill /IM WerFault.exe"
    os.system(command)
except Exception as e:
    print('close.py exception:', e)
