__all__ = ["immutable_cache_headers"]


def immutable_cache_headers(max_age: int = 31_536_000) -> dict[str, str]:
    """Return browser cache headers for content-addressed immutable resources."""
    return {"Cache-Control": f"public, max-age={max_age}, immutable"}
