
from typing import Any, List
from itertools import permutations
import random


class Queue():
    def __init__(self) -> None:
        self.queue = []

    def push(self, node: dict) -> None:
        self.queue.append(node)

    def pop(self) -> dict:
        if self.get_size() > 0:
            return self.queue.pop(0)
        else:
            return None

    def clear(self) -> None:
        self.queue = []

    def as_list(self) -> List[dict]:
        return self.queue

    def get_size(self) -> int:
        return len(self.queue)

    def shuffle(self) -> None:
        shuffled_queue = list(permutations(self.queue))
        random_index = random.randint(0, len(shuffled_queue))
        self.queue = list(shuffled_queue[random_index])

    def skip_to(self, index: int) -> bool:
        if index <= self.get_size():
            self.queue = self.queue[index-1:]
            return True
        return False

    def push_to_start(self, node: dict) -> None:
        self.queue.insert(0, node)
