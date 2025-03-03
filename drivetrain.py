
from utils import *

class Drivetrain:
    def __init__(self, name, ratio, gear, wheel_radius, robot_mass, motor_count, friction_coefficient):
        self.name = name
        self.ratio = ratio
        self.gear = gear
        self.wheel_radius = wheel_radius
        self.robot_mass = robot_mass
        self.motor_count = motor_count
        self.friction_coefficient = friction_coefficient

    def calculate_force(self, speed):
        base_torque = torque(speed / maxSpeed(self.gear, self.ratio, self.wheel_radius)) * 2.1 / (self.gear.value * self.ratio)
        friction_torque = self.friction_coefficient * speed
        return base_torque - friction_torque

    def acceleration(self, t, y):
        speed = y[1]
        return [speed, self.calculate_force(abs(speed)) * self.motor_count / (self.wheel_radius * self.robot_mass)]
