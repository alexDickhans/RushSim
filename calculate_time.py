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
time_span = (0, 10)  # 10 seconds

# Solve the differential equation
solution = solve_ivp(acceleration, time_span, initial_conditions, dense_output=True, events=lambda t, y: y[0] - target_distance)

# Extract the time to reach the target distance
time_to_reach_distance = solution.t_events[0][0] if solution.t_events[0].size > 0 else None

if time_to_reach_distance is not None:
    print(f"Time to reach {target_distance} meters: {time_to_reach_distance:.2f} seconds")
else:
    print(f"The robot did not reach {target_distance} meters within the time span.")