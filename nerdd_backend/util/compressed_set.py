from __future__ import annotations

from typing import List, Optional, Tuple, Union

__all__ = ["CompressedSet"]


class CompressedSet:
    def __init__(
        self, intervals_or_entries: Optional[Union[List[Tuple[int, int]], List[int]]] = None
    ):
        if intervals_or_entries is None or len(intervals_or_entries) == 0:
            intervals_or_entries = []
        else:
            if isinstance(intervals_or_entries[0], int):
                # convert list of entries to list of intervals
                entries = sorted(set(intervals_or_entries))
                intervals = []
                start = entries[0]
                for i in range(1, len(entries)):
                    if entries[i] != entries[i - 1] + 1:
                        intervals.append((start, entries[i - 1] + 1))
                        start = entries[i]
                intervals.append((start, entries[-1] + 1))
                self.intervals = intervals
            elif isinstance(intervals_or_entries[0], tuple) and len(intervals_or_entries[0]) == 2:
                # copy the list of intervals
                self.intervals = list(intervals_or_entries)
            else:
                raise ValueError(
                    f"Invalid input: must be a list of intervals or entries, got "
                    f"{intervals_or_entries} of type {type(intervals_or_entries)}"
                )

    def add(self, x: int) -> CompressedSet:
        i = 0
        while i < len(self.intervals) and self.intervals[i][0] <= x:
            i += 1
        i = max(0, i - 1)
        if i >= len(self.intervals):
            self.intervals.append((x, x + 1))
        else:
            left, right = self.intervals[i]
            if left <= x < right:
                return self
            elif x < left:
                self.intervals.insert(i, (x, x + 1))
            else:
                self.intervals.insert(i + 1, (x, x + 1))
                i += 1
        if i > 0 and self.intervals[i - 1][1] == self.intervals[i][0]:
            self.intervals[i - 1] = (self.intervals[i - 1][0], self.intervals[i][1])
            self.intervals.pop(i)
            i -= 1
        if i < len(self.intervals) - 1 and self.intervals[i][1] == self.intervals[i + 1][0]:
            self.intervals[i] = (self.intervals[i][0], self.intervals[i + 1][1])
            self.intervals.pop(i + 1)
        return self

    def contains(self, x: int) -> bool:
        i = 0
        while i < len(self.intervals) and self.intervals[i][0] <= x:
            if x < self.intervals[i][1]:
                return True
            i += 1
        return False

    def __contains__(self, x: int) -> bool:
        return self.contains(x)

    def count(self) -> int:
        return sum(j - i for i, j in self.intervals)

    def to_intervals(self) -> List[Tuple[int, int]]:
        return self.intervals

    def __repr__(self) -> str:
        return f"CompressedSet({self.intervals})"
