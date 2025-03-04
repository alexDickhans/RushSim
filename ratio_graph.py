import matplotlib.pyplot as plt
import numpy as np
from scipy.integrate import solve_ivp
from drivetrain import Drivetrain
from utils import Gear, in_to_m

def simulate_drivetrain(ratio, target_distance, motor_count, gear, wheel_radius, robot_mass, friction_coefficient):
    drivetrain = Drivetrain(f"Drivetrain with ratio {ratio:.2f}", ratio, gear, wheel_radius, robot_mass, motor_count, friction_coefficient)

    def acceleration(t, y):
        speed = y[1]
        return [speed, drivetrain.calculate_force(abs(speed)) * drivetrain.motor_count / (drivetrain.wheel_radius * drivetrain.robot_mass)]

    initial_conditions = [0, 0]
    time_span = (0, 10)  # 10 seconds

    solution = solve_ivp(acceleration, time_span, initial_conditions, dense_output=True, max_step=0.001)
    return solution.t, solution.y[1]

# Parameters
target_distance = 0.91  # Target distance in meters
motor_count = 6  # Number of motors
gear = Gear.BLUE  # Gear type
wheel_radius = in_to_m(2.75 / 2)  # Wheel radius in meters
robot_mass = 6.8  # Robot mass in kg
friction_coefficient = 0.02  # Friction coefficient
ratio_range = np.linspace(0.5, 3.0, 5)  # Range of ratios to test

plt.figure(figsize=(10, 6))

for ratio in ratio_range:
    time, speed = simulate_drivetrain(ratio, target_distance, motor_count, gear, wheel_radius, robot_mass, friction_coefficient)
    plt.plot(time, speed, label=f'Ratio 1:{ratio:.2f}')

plt.xlabel('Time (s)')
plt.ylabel('Speed (m/s)')
plt.title('Speed over Time for Different Ratios')
plt.legend()
plt.grid(True)
plt.show()