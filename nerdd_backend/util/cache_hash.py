import hashlib

__all__ = ["compute_cache_hash"]


def compute_cache_hash(content: bytes, length: int = 24) -> str:
    """Return a compact, content-addressed cache key suitable for use in URLs."""
    return hashlib.sha256(content).hexdigest()[:length]
