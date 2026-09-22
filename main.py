import math
from pathlib import Path
import matplotlib
import matplotlib.pyplot as plt
matplotlib.use("Agg")

MASS = 2000
ROLLING_COEFFICIENT = 0.01
DRAG_COEFFICIENT = 0.30
FRONTAL_AREA = 2.5
AIR_DENSITY = 1.2
GRAVITY = 10
TIRE_RADIUS = 0.4
EFFICIENCY = 0.90
TIME_STEP = 0.01
DURATION = 120
GEAR_RATIOS = [9, 7, 10.5]


def motor_torque(rpm):
    if rpm <= 4000:
        return 250
    if rpm <= 10000:
        return 250 * 4000 / rpm
    return 0


def simulate(gear_ratio):
    times, speeds = [0.0], [0.0]
    time_to_20 = None
    for step in range(1, round(DURATION / TIME_STEP) + 1):
        speed = speeds[-1]
        wheel_radians_per_second = speed / TIRE_RADIUS
        motor_rpm = wheel_radians_per_second * gear_ratio * 60 / (2 * math.pi)
        drive_force = motor_torque(motor_rpm) * gear_ratio * EFFICIENCY / TIRE_RADIUS
        rolling_force = ROLLING_COEFFICIENT * MASS * GRAVITY
        drag_force = 0.5 * AIR_DENSITY * DRAG_COEFFICIENT * FRONTAL_AREA * speed**2
        acceleration = (drive_force - rolling_force - drag_force) / MASS
        new_speed = max(0.0, speed + acceleration * TIME_STEP)
        if time_to_20 is None and speed < 20 <= new_speed:
            time_to_20 = times[-1] + TIME_STEP * (20 - speed) / (new_speed - speed)
        times.append(step * TIME_STEP)
        speeds.append(new_speed)
    return times, speeds, time_to_20


def main():
    fig, ax = plt.subplots(figsize=(9, 5))
    print("gear ratio | time to 20 m/s | top speed (m/s) | speed at 1 s (m/s)")
    for ratio in GEAR_RATIOS:
        times, speeds, time_to_20 = simulate(ratio)
        crossing = "Not reached" if time_to_20 is None else f"{time_to_20:.3f}"
        print(f"{ratio:g} | {crossing} | {max(speeds):.3f} | {speeds[100]:.3f}")
        ax.plot(times, speeds, label=f"Gear ratio {ratio:g}")
    ax.set(xlabel="s", ylabel="m/s",
           title="acceleration on flat ground", xlim=(0, DURATION), ylim=(0, None))
    ax.grid(alpha=0.3)
    ax.legend()
    fig.tight_layout()
    output = Path(__file__).with_name("speed_vs_time.png")
    fig.savefig(output, dpi=160)
    plt.close(fig)
    print(f"Plot saved to {output}")


if __name__ == "__main__":
    main()
