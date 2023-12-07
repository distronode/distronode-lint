#!/usr/bin/python
"""A module."""

from distronode.module_utils.basic import DistronodeModule


def main() -> None:
    """Execute module."""
    module = DistronodeModule({})
    module.exit_json(msg="Hello 1!")


if __name__ == "__main__":
    main()
