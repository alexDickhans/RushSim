import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp
from drivetrain import Drivetrain
from utils import Gear, in_to_m

# List of different drivetrains
drivetrains = [
    Drivetrain("480 rpm, 2.75 in", 48.0 / 60.0, Gear.BLUE, in_to_m(2.75/2), 6.8, 6, 0.02),
    Drivetrain("450 rpm, 2.75 in", 36.0 / 48.0, Gear.BLUE, in_to_m(2.75/2), 6.8, 6, 0.02),
    Drivetrain("450 rpm, 3.25 in", 36.0 / 48.0, Gear.BLUE, in_to_m(3.25/2), 6.8, 6, 0.02),
    Drivetrain("360 rpm, 3.25 in", 36.0 / 60.0, Gear.BLUE, in_to_m(3.25/2), 6.8, 6, 0.02),
    Drivetrain("600 rpm, 2.75 in", 1.0, Gear.BLUE, in_to_m(2.75/2), 6.8, 6, 0.02),
]

# Target distance
target_distance = 0.91

# Time span for the integration
time_span = (0, 0.70)  # 10 seconds

# Positions for vertical lines
vertical_lines = [target_distance, target_distance + 0.15]
names = ["Target", "Target + 6 inches"]

plt.figure(figsize=(10, 6))

for drivetrain in drivetrains:
    # Acceleration function using the Drivetrain object
    def acceleration(t, y):
        speed = y[1]
        return [speed, drivetrain.calculate_force(abs(speed)) * drivetrain.motor_count / (drivetrain.wheel_radius * drivetrain.robot_mass)]

    # Initial conditions: [initial_position, initial_speed]
    initial_conditions = [0, 0]

    # Solve the differential equation
    solution = solve_ivp(acceleration, time_span, initial_conditions, dense_output=True, max_step=0.001, events=lambda t, y: y[0] - target_distance)

    # Extract the distance and time
    distance = solution.y[0]
    time = solution.t

    if solution.t_events[0].size > 0:
        time_to_target = solution.t_events[0][0]
        print(f'{drivetrain.name}: {time_to_target:.4f} seconds')
    else:
        print(f'{drivetrain.name}: did not reach the target distance within the time span')

    # Plotting
    plt.plot(distance, time, label=drivetrain.name)

# Add vertical lines
for i, vline in enumerate(vertical_lines):
    plt.axvline(x=vline, color='r', linestyle='--', label=names[i])

plt.xlabel('Distance (m)')
plt.ylabel('Time (s)')
plt.title('Time over Distance for Different Drivetrains')
plt.legend()
plt.grid(True)
plt.show()