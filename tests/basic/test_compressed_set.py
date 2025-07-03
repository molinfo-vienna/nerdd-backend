import random

from nerdd_backend.util import CompressedSet


def test_constructor_with_intervals():
    # simple and easily verifiable example
    intervals = [(2, 4), (5, 7)]
    compressed_set = CompressedSet(intervals)
    assert compressed_set.to_intervals() == [(2, 4), (5, 7)]
    assert compressed_set.count() == 4

    # test with one interval
    intervals = [(1, 1000)]
    compressed_set = CompressedSet(intervals)
    assert compressed_set.to_intervals() == [(1, 1000)]
    assert compressed_set.count() == 999

def test_constructor_with_empty_list():
    compressed_set = CompressedSet([])
    assert compressed_set.to_intervals() == []
    assert compressed_set.count() == 0

    # test with None
    compressed_set = CompressedSet(None)
    assert compressed_set.to_intervals() == []
    assert compressed_set.count() == 0

    # test with empty CompressedSet
    empty_set = CompressedSet()
    assert empty_set.to_intervals() == []
    assert empty_set.count() == 0

def test_constructor_with_entries():
    entries = [2, 3, 5, 6]
    compressed_set = CompressedSet(entries)
    assert compressed_set.to_intervals() == [(2, 4), (5, 7)]
    assert compressed_set.count() == 4

    # test with a large number of entries
    entries = list(range(1, 1000))
    random.shuffle(entries)
    compressed_set = CompressedSet(entries)
    assert compressed_set.to_intervals() == [(1, 1000)]
    assert compressed_set.count() == 999

    # skip some entries
    entries = list(range(1, 1000))
    random.shuffle(entries)
    entries = entries[:-100]
    compressed_set = CompressedSet(entries)
    for i in entries:
        assert i in compressed_set
    assert compressed_set.count() == len(entries)

def test_constructor_with_compressed_set():
    original_set = CompressedSet([(2, 4), (5, 7)])
    compressed_set = CompressedSet(original_set)
    assert compressed_set.to_intervals() == original_set.to_intervals()
    assert compressed_set.count() == original_set.count()

    # test with a large number of intervals
    original_set = CompressedSet([(1, 1000)])
    compressed_set = CompressedSet(original_set)
    assert compressed_set.to_intervals() == original_set.to_intervals()
    assert compressed_set.count() == original_set.count()

def test_constructor_with_invalid_arg():
    try:
        CompressedSet("invalid")
    except ValueError as e:
        assert str(e) == "Invalid input: must be a list of intervals or entries, got invalid of type <class 'str'>"
    else:
        assert False, "Expected ValueError not raised"

def test_constructor_with_entries_duplicate():
    entries = [2, 2, 3, 5, 6]
    compressed_set = CompressedSet(entries)
    assert compressed_set.to_intervals() == [(2, 4), (5, 7)]
    assert compressed_set.count() == 4

    # test with a large number of entries with duplicates
    entries = list(range(1, 1000)) * 2
    random.shuffle(entries)
    compressed_set = CompressedSet(entries)
    assert compressed_set.to_intervals() == [(1, 1000)]
    assert compressed_set.count() == 999

def test_add_entries():
    compressed_set = CompressedSet([(2, 4), (5, 7)])
    compressed_set.add(4)
    compressed_set.add(7)
    compressed_set.add(1)
    assert compressed_set.to_intervals() == [(1, 8)]
    assert compressed_set.count() == 7

    # test with a large number of entries
    entries = list(range(1, 1000))
    random.shuffle(entries)
    compressed_set = CompressedSet()
    for entry in entries:
        compressed_set.add(entry)
    assert compressed_set.to_intervals() == [(1, 1000)]
    assert compressed_set.count() == 999

def test_add_entries_with_duplicates():
    compressed_set = CompressedSet([(2, 4), (5, 7)])

    # adding an entry that is already present
    compressed_set.add(6)
    assert compressed_set.to_intervals() == [(2, 4), (5, 7)]
    assert compressed_set.count() == 4

    compressed_set.add(3)
    assert compressed_set.to_intervals() == [(2, 4), (5, 7)]
    assert compressed_set.count() == 4

def test_contains():
    compressed_set = CompressedSet([(2, 4), (5, 7)])
    assert compressed_set.contains(3) is True
    assert compressed_set.contains(4) is False
    assert compressed_set.contains(5) is True
    assert compressed_set.contains(8) is False

    # notation test
    assert 3 in compressed_set
    assert 4 not in compressed_set
    assert 5 in compressed_set
    assert 8 not in compressed_set

def test_union_with_compressed_set():
    set1 = CompressedSet([(2, 4), (5, 7)])
    set2 = CompressedSet([(3, 6), (8, 10)])
    union_set = set1.union(set2)
    assert union_set.to_intervals() == [(2, 7), (8, 10)]
    assert union_set.count() == 7