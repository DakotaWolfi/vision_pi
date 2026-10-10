#!/usr/bin/env python3
"""VisionPi launcher.

The current working prototype should remain in tools/ until it has been
migrated module-by-module.
"""

from visionpi import __version__


def main() -> None:
    print(f"VisionPi {__version__}")
    print("Prototype migration not completed yet. See MIGRATION.md.")


if __name__ == "__main__":
    main()
