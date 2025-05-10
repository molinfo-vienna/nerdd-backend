from __future__ import annotations

from collections.abc import Sequence
from typing import List, Optional, Tuple, Union

from pydantic import GetCoreSchemaHandler
from pydantic_core.core_schema import (
    ValidationInfo,
    plain_serializer_function_ser_schema,
    with_info_plain_validator_function,
)

__all__ = ["CompressedSet"]


def _merge_intervals(intervals, i) -> None:
    if i < 0 or i >= len(intervals) - 1:
        return False

    # merge intervals[i] with intervals[i + 1] if they are adjacent / overlapping
    if intervals[i][1] >= intervals[i + 1][0]:
        start = min(intervals[i][0], intervals[i + 1][0])
        end = max(intervals[i][1], intervals[i + 1][1])
        intervals[i] = (start, end)
        intervals.pop(i + 1)
        return True

    return False


class CompressedSet:
    def __init__(
        self, intervals_or_entries: Optional[Union[List[Tuple[int, int]], List[int]]] = None
    ):
        if intervals_or_entries is None or len(intervals_or_entries) == 0:
            self.intervals = []
        else:
            if isinstance(intervals_or_entries[0], int):
                # convert list of entries to list of intervals
                entries = sorted(set(intervals_or_entries))
                intervals = []
                start = entries[0]
                for i in range(1, len(entries)):
                    if entries[i] == entries[i - 1]:
                        # skip duplicates
                        continue
                    if entries[i] != entries[i - 1] + 1:
                        intervals.append((start, entries[i - 1] + 1))
                        start = entries[i]
                intervals.append((start, entries[-1] + 1))
                self.intervals = intervals
            elif (
                isinstance(intervals_or_entries[0], Sequence) and len(intervals_or_entries[0]) == 2
            ):
                # copy the list of intervals
                self.intervals = list(intervals_or_entries)
            else:
                raise ValueError(
                    f"Invalid input: must be a list of intervals or entries, got "
                    f"{intervals_or_entries} of type {type(intervals_or_entries)}"
                )

    def add(self, x: int) -> None:
        # search for the position to insert x
        i = 0
        while i < len(self.intervals) and self.intervals[i][0] <= x:
            i += 1
        i = max(0, i - 1)  # the previous interval might contain x

        if i >= len(self.intervals):
            # x is greater than all existing intervals
            # -> append a new interval
            self.intervals.append((x, x + 1))
        else:
            left, right = self.intervals[i]
            if left <= x < right:
                # x is already in the set
                return
            elif x < left:
                self.intervals.insert(i, (x, x + 1))
            else:
                self.intervals.insert(i + 1, (x, x + 1))
                i += 1

        # merge intervals if necessary
        merged = _merge_intervals(self.intervals, i - 1)
        if merged:
            _merge_intervals(self.intervals, i - 1)
        else:
            _merge_intervals(self.intervals, i)

    def union(self, other: Union[CompressedSet, List[int], List[Tuple[int, int]]]) -> CompressedSet:
        if isinstance(other, CompressedSet):
            other_intervals = other.intervals
        elif isinstance(other, list):
            if len(other) == 0:
                return CompressedSet(self.intervals)

            first = other[0]
            if isinstance(first, int):
                other_intervals = CompressedSet(other).intervals
            elif isinstance(first, tuple) and len(first) == 2:
                other_intervals = other
            else:
                raise ValueError(
                    f"Invalid input: must be a CompressedSet or a list of integers or intervals, "
                    f"got {other}"
                )
        else:
            raise ValueError(
                f"Invalid input: must be a CompressedSet or a list of integers, got {other}"
            )

        # merge the intervals from both sets
        i = 0
        j = 0
        merged_intervals = []
        while i < len(self.intervals) or j < len(other_intervals):
            if i < len(self.intervals) and (
                j == len(other_intervals) or (self.intervals[i][0] <= other_intervals[j][0])
            ):
                merged_intervals.append(tuple(self.intervals[i]))
                i += 1
            else:
                merged_intervals.append(tuple(other_intervals[j]))
                j += 1
            _merge_intervals(merged_intervals, len(merged_intervals) - 2)

        return CompressedSet(merged_intervals)

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

    @classmethod
    def __get_pydantic_core_schema__(cls, source, handler: GetCoreSchemaHandler):
        def _validate(
            v: List[Tuple[int, int]],
            info: ValidationInfo,
        ) -> CompressedSet:
            if isinstance(v, cls):
                return v
            if isinstance(v, list):
                return cls(v)
            raise TypeError(f"Expected a CompressedSet or a list of intervals, got {type(v)}")

        return with_info_plain_validator_function(
            _validate,
            serialization=plain_serializer_function_ser_schema(
                lambda v: v.to_intervals(),
                return_schema=handler(List[Tuple[int, int]]),
            ),
        )
