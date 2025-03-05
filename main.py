import matplotlib.pyplot as plt
import numpy as np
import csv
import math
from utils import *

# Constants
ratio = 36.0 / 48.0  # input / output
gear = Gear.BLUE
wheel_radius = 0.035  # In meters
robot_mass = 6.8  # In kg
motor_count = 6
maxTime = 1.2

# Time array
time = np.linspace(0, maxTime, 500)  # 10 seconds, 500 points

# Acceleration function
def acceleration(speed):
    return calculate_torque(math.fabs(speed), gear, ratio, wheel_radius) * motor_count / (wheel_radius * robot_mass)

# Calculate speed by integrating acceleration
speed = np.zeros_like(time)
distance = np.zeros_like(time)

direction = 1

for i in range(1, len(time)):
    dt = time[i] - time[i-1]
    direction = -2 if 1.25/2 < distance[i-1] or direction < 0 else 1
    speed[i] = speed[i-1] + acceleration(speed[i-1]) * dt * direction
    distance[i] = distance[i-1] + speed[i-1] * dt

# Function to export speed over time to CSV
def export_to_csv(time, speed, filename='speed_over_time.csv'):
    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Time (s)', 'Speed (m/s)'])
        for t, s in zip(time, speed):
            writer.writerow([t, s])

# Export the data to CSV
export_to_csv(time, speed)

# Plotting
plt.figure(figsize=(10, 6))

# Plot speed over time
plt.subplot(2, 1, 1)
plt.plot(time, speed, label='Speed over time')
plt.axhline(y=maxSpeed(gear, ratio, wheel_radius), color='r', linestyle='--', label='Max Speed')
plt.xlabel('Time (s)')
plt.ylabel('Speed (m/s)')
plt.title('Speed over Time using Proper Acceleration')
plt.legend()
plt.grid(True)

# Plot distance over time
plt.subplot(2, 1, 2)
plt.plot(time, distance, label='Distance over time', color='orange')
plt.xlabel('Time (s)')
plt.ylabel('Distance (m)')
plt.title('Distance over Time using Proper Acceleration')
plt.legend()
plt.grid(True)

plt.tight_layout()
plt.show()