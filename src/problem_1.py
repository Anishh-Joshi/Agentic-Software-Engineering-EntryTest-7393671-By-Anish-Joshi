"""Problem 1: Two Sum."""

from collections.abc import Sequence


def two_sum(nums: Sequence[int], target: int) -> tuple[int, int] | None:
    """Return the indices (i, j), i < j, of two numbers that add up to ``target``.

    Runs in O(n) time and O(n) space by remembering, for every number seen so
    far, the index where it occurred. Returns ``None`` if no pair exists.
    """
    seen: dict[int, int] = {}  # value -> index where we saw it
    for j, value in enumerate(nums):
        complement = target - value
        if complement in seen:
            return seen[complement], j
        seen[value] = j
    return None


if __name__ == "__main__":
    print(two_sum([2, 7, 11, 15], 9))
