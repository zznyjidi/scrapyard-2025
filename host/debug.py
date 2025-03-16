import config

def debugPrint(*values):
    if config.DEBUG:
        print(*values)
