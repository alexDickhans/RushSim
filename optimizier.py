import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp
from drivetrain import Drivetrain
from utils import Gear, in_to_m

def find_optimal_ratio(target_distance, motor_count, gear, wheel_radius, robot_mass, friction_coefficient, ratio_range):
    best_ratio = None
    best_time = float('inf')
    times = []

    for ratio in ratio_range:
        drivetrain = Drivetrain(f"Drivetrain with ratio {ratio:.2f}", ratio, gear, wheel_radius, robot_mass, motor_count, friction_coefficient)

        def acceleration(t, y):
            speed = y[1]
            return [speed, drivetrain.calculate_force(abs(speed)) * drivetrain.motor_count / (drivetrain.wheel_radius * drivetrain.robot_mass)]

        initial_conditions = [0, 0]
        time_span = (0, 10)  # 10 seconds

        solution = solve_ivp(acceleration, time_span, initial_conditions, dense_output=True, max_step=0.001, events=lambda t, y: y[0] - target_distance)

        if solution.t_events[0].size > 0:
            time_to_target = solution.t_events[0][0]
            times.append(time_to_target)
            if time_to_target < best_time:
                best_time = time_to_target
                best_ratio = ratio
        else:
            times.append(float('inf'))

    return best_ratio, best_time, times

# Parameters
target_distance = 0.91  # Target distance in meters
motor_count = 6  # Number of motors
gear = Gear.BLUE  # Gear type
wheel_radius = in_to_m(2.75 / 2)  # Wheel radius in meters
robot_mass = 6.8  # Robot mass in kg
friction_coefficient = 0.02  # Friction coefficient
ratio_range = np.linspace(0.5, 2.0, 100)  # Range of ratios to test

# Find the optimal ratio
optimal_ratio, optimal_time, times = find_optimal_ratio(target_distance, motor_count, gear, wheel_radius, robot_mass, friction_coefficient, ratio_range)

print(f"Optimal ratio: {optimal_ratio:.2f}")
print(f"Time to target distance: {optimal_time:.4f} seconds")

# Plot the times for each ratio
plt.figure(figsize=(10, 6))
plt.plot(ratio_range, times, label='Time to target distance')
plt.axvline(x=optimal_ratio, color='r', linestyle='--', label=f'Optimal ratio 1:{optimal_ratio:.2f}')
plt.xlabel('Ratio')
plt.ylabel('Time (s)')
plt.title('Time to Target Distance for Different Ratios')
plt.legend()
plt.grid(True)
plt.show()