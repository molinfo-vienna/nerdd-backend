__all__ = ["clamp"]


def clamp(value: int, min_value: int, max_value: int) -> int:
    """Clamp a value between a minimum and maximum value."""
    return max(min_value, min(value, max_value))
