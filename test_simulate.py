"""Run with python3 test_simulate.py; no test framework needed."""

# This file is 100% GPT'd

import math

from main import motor_torque, simulate

assert [motor_torque(rpm) for rpm in (0, 4000, 8000, 10000, 10001)] == [250, 250, 125, 100, 0]
times, speeds, crossing = simulate(9)
assert len(times) == 12001 and times[-1] == 120
assert speeds[0] == 0 and min(speeds) >= 0
assert math.isclose(speeds[1], 0.0243125, abs_tol=1e-12)
assert abs(speeds[100] - 2.4) < 0.05, speeds[100]
assert crossing is not None and 8 < crossing < 12
index = next(i for i, speed in enumerate(speeds) if speed >= 20)
assert times[index - 1] <= crossing <= times[index]
assert simulate(0.01)[2] is None
for invalid in (0, -1, float("nan"), float("inf")):
    try:
        simulate(invalid)
    except ValueError:
        pass
    else:
        raise AssertionError(f"Accepted invalid ratio {invalid}")
print("All checks passed, including the gear-9 checkpoint.")
