DEBUG = True

# Connection Settings
serialPath = '/dev/ttyACM0'

# Mapping Settings
areaSize = (1852, 1235)
areaOffset = (0, 0)

# Client Settings
serialScreenSize = (800, 480)
serialMoveCommand = '(?:x0=)([0-9]+)(?: y0=)([0-9]+)'
serialMouseDownCommand = 'DOWN'
serialMouseUpCommand = 'UP'
serialButtonCommand = 'SWITCH'
