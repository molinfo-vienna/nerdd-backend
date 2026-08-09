from inhouse import MemoryStore

__all__ = ["cache_store"]

cache_store = MemoryStore(max_size=512)
