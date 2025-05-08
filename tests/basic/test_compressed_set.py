from nerdd_backend.util import CompressedSet


def test_constructor_with_intervals():
    intervals = [(2, 4), (5, 7)]
    compressed_set = CompressedSet(intervals)
    assert compressed_set.to_intervals() == [(2, 4), (5, 7)]
    assert compressed_set.count() == 4

def test_constructor_with_entries():
    entries = [2, 3, 5, 6]
    compressed_set = CompressedSet(entries)
    assert compressed_set.to_intervals() == [(2, 4), (5, 7)]
    assert compressed_set.count() == 4

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

def test_add_entries():
    pass

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