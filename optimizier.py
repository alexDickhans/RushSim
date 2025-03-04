import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from scipy.integrate import solve_ivp
from concurrent.futures import ThreadPoolExecutor
from tqdm import tqdm
from drivetrain import Drivetrain
from utils import Gear, in_to_m

def simulate_drivetrain(ratio, target_distance, motor_count, gear, wheel_radius, robot_mass, friction_coefficient):
    drivetrain = Drivetrain(f"Drivetrain with ratio {ratio:.2f}", ratio, gear, wheel_radius, robot_mass, motor_count, friction_coefficient)

    def acceleration(t, y):
        speed = y[1]
        return [speed, drivetrain.calculate_force(abs(speed)) * drivetrain.motor_count / (drivetrain.wheel_radius * drivetrain.robot_mass)]

    initial_conditions = [0, 0]
    time_span = (0, 10)  # 10 seconds

    solution = solve_ivp(acceleration, time_span, initial_conditions, dense_output=True, max_step=0.5, events=lambda t, y: y[0] - target_distance)

    if solution.t_events[0].size > 0:
        return solution.t_events[0][0]
    else:
        return float('inf')

def find_optimal_ratio(target_distances, motor_count, gear, wheel_radius, robot_mass, friction_coefficient, ratio_range):
    times = np.zeros((len(ratio_range), len(target_distances)))

    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = []
        for i, ratio in enumerate(ratio_range):
            for j, target_distance in enumerate(target_distances):
                futures.append((i, j, executor.submit(simulate_drivetrain, ratio, target_distance, motor_count, gear, wheel_radius, robot_mass, friction_coefficient)))

        for i, j, future in tqdm(futures, desc="Calculating", total=len(futures)):
            times[i, j] = future.result()

    return times

# Parameters
target_distances = np.linspace(0.1, 1.5, 100)  # Range of target distances to test
motor_count = 6  # Number of motors
gear = Gear.BLUE  # Gear type
wheel_radius = in_to_m(2.75 / 2)  # Wheel radius in meters
robot_mass = 6.8  # Robot mass in kg
friction_coefficient = 0.02  # Friction coefficient
ratio_range = np.linspace(0.3, 1.8, 100)  # Range of ratios to test

# Find the times for each combination of ratio and target distance
times = find_optimal_ratio(target_distances, motor_count, gear, wheel_radius, robot_mass, friction_coefficient, ratio_range)

# Create a 3D plot
X, Y = np.meshgrid(ratio_range, target_distances)
Z = times.T

fig = plt.figure(figsize=(12, 8))
ax = fig.add_subplot(111, projection='3d')
ax.plot_surface(X, Y, Z, cmap='viridis')

ax.set_xlabel('Ratio')
ax.set_ylabel('Target Distance (m)')
ax.set_zlabel('Time (s)')
ax.set_title('Time to Target Distance for Different Ratios and Distances')

plt.show()