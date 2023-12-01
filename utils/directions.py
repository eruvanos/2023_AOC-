from utils.vector import Vec2

# Directions
NORTH = "N"
SOUTH = "S"
EAST = "E"
WEST = "W"
LEFT = "L"
RIGHT = "R"
FORWARD = "F"

# Vectors for NESW
NESW_VEC = {
    "E": Vec2(1, 0),
    "W": Vec2(-1, 0),
    "N": Vec2(0, 1),
    "S": Vec2(0, -1),
}

# Turn maps for NESW
TURN_LEFT = {
    "E": "N",
    "W": "S",
    "N": "W",
    "S": "E",
}
TURN_RIGHT = {
    "E": "S",
    "W": "N",
    "N": "E",
    "S": "W",
}

# ARROW directions
UDRL_VEC = {
    "U": Vec2(0, 1),
    "D": Vec2(0, -1),
    "R": Vec2(1, 0),
    "L": Vec2(-1, 0),
}

ARROW_VEC = {
    "^": Vec2(0, 1),
    "v": Vec2(0, -1),
    "<": Vec2(-1, 0),
    ">": Vec2(1, 0),
}
"""ARROW to Angle U = 0° """

NESW_ARROW = {
    "E": "R",
    "W": "L",
    "N": "U",
    "S": "D",
}
"""Convert NESW to Arrow"""

ARROW_NESW = {
    "R": "E",
    "L": "W",
    "U": "N",
    "D": "S",
}
"""Convert Arrow to NESW"""


ANGLES_DIR = {"R": 90, "L": 270, "U": 0, "D": 180}
"""ARROW to Angle U = 0° """


DEGREE_VECTOR = {
    0.0: Vec2(1, 0),
    45.0: Vec2(1, 1),
    90.0: Vec2(0, 1),
    135.0: Vec2(-1, 1),
    180.0: Vec2(-1, 0),
    225.0: Vec2(-1, -1),
    270.0: Vec2(0, -1),
    315.0: Vec2(1, -1),
}
"""Convert angle to slope Vec2, supports 45 degree steps"""
