DEBUG = True

# Troll Settings
randomJump = False

# Connection Settings
serialPath = '/dev/ttyACM0'

# Mapping Settings
tabletAreaSize = (600, 400)
tabletAreaOffset = (100, 40)
screenAreaSize = (1852, 1235)
screenAreaOffset = (0, 0)

# Client Settings
serialScreenSize = (800, 480)
serialMoveCommand = '(?:x0=)([0-9]+)(?: y0=)([0-9]+)'
serialMouseDownCommand = 'DOWN'
serialMouseUpCommand = 'UP'
serialButtonCommand = 'SWITCH'
