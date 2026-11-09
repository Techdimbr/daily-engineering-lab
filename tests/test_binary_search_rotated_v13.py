from .binary_search_rotated import search_rotated_array

def test_search_rotated():
    nums = [4, 5, 6, 7, 0, 1, 2]
    assert search_rotated_array(nums, 0) == 4
    assert search_rotated_array(nums, 3) == -1
    assert search_rotated_array([1], 0) == -1
    assert search_rotated_array([1], 1) == 0
