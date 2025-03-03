import enum
import math

class Gear(enum.Enum):
    RED = 1
    GREEN = 2
    BLUE = 6

def torque(pct):
    if pct < 0.58:
        return 1.0

    return -1.59524 * pct + 1.92143

def maxSpeed(gear: Gear, ratio, radius):
    return (gear.value * 200 * math.pi * radius * ratio) / 60

def calculate_torque(speed, gear: Gear, ratio, radius, friction_coefficient=0.02):
    base_torque = torque(speed / maxSpeed(gear, ratio, radius)) * 2.1 / (gear.value * ratio)
    friction_torque = friction_coefficient * speed
    return base_torque - friction_torque

def in_to_m(inches):
    return inches * 0.0254



