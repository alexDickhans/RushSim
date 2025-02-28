import matplotlib.pyplot as plt
import numpy as np
from scipy.integrate import solve_ivp
from utils import calculate_torque, Gear

# Constants
ratio = 36.0 / 48.0  # input / output
gear = Gear.BLUE
wheel_radius = 0.035  # In meters
robot_mass = 6.8  # In kg
motor_count = 6
friction_coefficient = 0.02  # Friction coefficient
target_distance = 1.22  # Target distance in meters

# Acceleration function
def acceleration(t, y):
    speed = y[1]
    return [speed, calculate_torque(abs(speed), gear, ratio, wheel_radius, friction_coefficient) * motor_count / (wheel_radius * robot_mass)]

# Initial conditions: [initial_position, initial_speed]
initial_conditions = [0, 0]

# Time span for the integration
time_span = (0, 0.9)  # 10 seconds

# Solve the differential equation
solution = solve_ivp(acceleration, time_span, initial_conditions, dense_output=True, max_step=0.001, events=lambda t, y: y[0] - target_distance)

# Extract the distance and time
distance = solution.y[0]
time = solution.t

# Plotting
plt.figure(figsize=(10, 6))
plt.plot(distance, time, label='Time over distance', color='orange')
plt.xlabel('Distance (m)')
plt.ylabel('Time (s)')
plt.title('Time over Distance')
plt.legend()
plt.grid(True)
plt.show()