from enum import Enum

class Direction(Enum):
    cw = 0
    ccw = 1

class Column(Enum):
    current = 0
    voltage = 1
    watts_in = 2
    efficiency = 3
    speed = 4
    torque = 5
    watts_out = 6
    cw_ccw = 7
