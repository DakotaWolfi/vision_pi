"""Fan telemetry helpers.

The exact hwmon path may vary between boots, so discover it by looking for
fan1_input rather than hard-coding hwmon0/hwmon1.
"""

from pathlib import Path


def fan_rpm():
    for path in Path("/sys/class/hwmon").glob("hwmon*/fan1_input"):
        try:
            return int(path.read_text().strip())
        except (OSError, ValueError):
            pass
    return None
