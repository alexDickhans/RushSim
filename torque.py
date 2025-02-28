import matplotlib.pyplot as plt
import numpy as np
from utils import torque, Gear

# Constants
ratio = 36.0 / 48.0  # input / output
gear = Gear.BLUE
wheel_radius = 0.035  # In meters

# Speed array
speed = np.linspace(0, 1, 100)  # Speed range from 0 to 10 m/s

# Calculate torque for each speed
torque_values = [torque(s) for s in speed]

# Plotting
plt.figure(figsize=(10, 6))
plt.plot(speed, torque_values, label='Torque over speed')
plt.xlabel('Speed (m/s)')
plt.ylabel('Torque (Nm)')
plt.title('Torque over Speed')
plt.legend()
plt.grid(True)
plt.show()