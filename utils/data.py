import heapq
from typing import NamedTuple, Union


class PriorityQueue:
    """
    DEPRECATED use Pythons `queue.PriorityQueue`

    A subclass of Queue; retrieves entries in priority order (lowest first).
    Entries are typically tuples of the form: (priority number, data).
    """

    def __init__(self):
        self._queue = []

    def __bool__(self):
        return not self.empty()

    def put(self, item):
        heapq.heappush(self._queue, item)

    def get(self):
        return heapq.heappop(self._queue)

    def empty(self):
        return len(self._queue) == 0


def slice(text: str, chunk_size: int, overlap=0):
    while len(text) >= chunk_size:
        to_send, text = text[:chunk_size], text[chunk_size - overlap:]
        yield to_send


# yield all possible partitions of a list into k subsets
def subsets_k(collection, k):
    """

    Source: https://github.com/ChrisWojcik/advent-of-code-2022/blob/dde48d7b47dddc1225765d2759ea74a66b3bbc86/16/2.py#L37

    :param collection: List of options
    :param k: number of partitions
    :return: any combination how to split the list
    """
    yield from _partition_k(collection, k, k)


def _partition_k(collection, min, k):
    if len(collection) == 1:
        yield [collection]
        return

    first = collection[0]
    for smaller in _partition_k(collection[1:], min - 1, k):
        if len(smaller) > k:
            continue

        if len(smaller) >= min:
            for n, subset in enumerate(smaller):
                yield smaller[:n] + [[first] + subset] + smaller[n + 1:]

        if len(smaller) < k:
            yield [[first]] + smaller


class Range(NamedTuple):
    """1 dimensional range"""
    start: int
    end: int

    def __len__(self):
        return abs(self.end - self.start)

    def __repr__(self):
        return f"[{self.start}->{self.end}]"

    @staticmethod
    def parse(text: str):
        a, b = text.split("-")
        return Range(int(a), int(b))

    def subrange_of(self, other: "Range"):
        return self.start >= other.start and self.end <= other.end

    def __contains__(self, other: Union[int, "Range"]):
        if isinstance(other, int):
            return self.start <= other <= self.end
        else:
            return other.start >= self.start and other.end <= self.end

    def overlap(self, other: "Range"):
        """Check if ranges overlap each other, this could be full or partially"""
        if other.start <= self.start <= other.end:
            return True

        if other.start <= self.end <= other.end:
            return True

        if self.start <= other.start <= self.end:
            return True

        if self.start <= other.end <= self.end:
            return True

        return False
