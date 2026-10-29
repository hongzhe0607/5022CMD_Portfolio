"""
hash_table.py
Generic Hash Table using Open Addressing with Linear Probing.

This module knows nothing about pharmacies or products - it stores any
(key, value) pair, so it can be reused in other programs (abstraction).
"""


class _Slot:
    """
    One slot (bucket) of the hash table.

    In open addressing every slot holds at most ONE record, so a slot only
    needs the key, the value, and a flag saying whether the record was deleted.
    The 'deleted' flag (a "tombstone") is needed so that searching does not
    stop early at a slot whose record was removed in the middle of a probe chain.
    """
    __slots__ = ("key", "value", "deleted")

    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.deleted = False


class HashTable:
    """Hash table with open addressing and linear probing."""

    def __init__(self, capacity=101, max_load_factor=0.7):
        # A prime capacity spreads integer keys more evenly across the slots.
        self._capacity = capacity
        self._max_load = max_load_factor
        self._table = [None] * capacity   # None = slot never used
        self._size = 0                     # number of live records

    # ------------------------------------------------------------------ #
    # Internal helpers
    # ------------------------------------------------------------------ #
    def _hash(self, key):
        """Division method: map any hashable key to an index 0..capacity-1."""
        if isinstance(key, int):
            return key % self._capacity
        # For strings / other keys, use a simple polynomial rolling hash so
        # the result is the same every run (Python's hash() for str is random).
        h = 0
        for ch in str(key):
            h = (h * 31 + ord(ch)) % self._capacity
        return h

    def _probe(self, key):
        """
        Yield slot indexes in linear probing order: h, h+1, h+2, ... (wrapping).
        Visits each slot at most once.
        """
        start = self._hash(key)
        for i in range(self._capacity):
            yield (start + i) % self._capacity

    def _resize(self):
        """Double the capacity (to the next prime) and re-insert all records."""
        old_items = list(self.items())
        self._capacity = self._next_prime(self._capacity * 2)
        self._table = [None] * self._capacity
        self._size = 0
        for k, v in old_items:
            self.insert(k, v)

    @staticmethod
    def _next_prime(n):
        def is_prime(x):
            if x < 2:
                return False
            i = 2
            while i * i <= x:
                if x % i == 0:
                    return False
                i += 1
            return True
        while not is_prime(n):
            n += 1
        return n

    # ------------------------------------------------------------------ #
    # Public operations
    # ------------------------------------------------------------------ #
    def insert(self, key, value):
        """
        Insert or update a record. Returns the slot index used.
        Average O(1); worst case O(n) when many keys collide.
        """
        if (self._size + 1) / self._capacity > self._max_load:
            self._resize()

        first_tombstone = None
        for idx in self._probe(key):
            slot = self._table[idx]
            if slot is None:
                # Empty slot: key is not in table. Reuse a tombstone if we saw one.
                target = first_tombstone if first_tombstone is not None else idx
                self._table[target] = _Slot(key, value)
                self._size += 1
                return target
            if slot.deleted:
                if first_tombstone is None:
                    first_tombstone = idx
            elif slot.key == key:
                slot.value = value          # update existing record
                return idx

        # Table had no empty slot but had a tombstone
        if first_tombstone is not None:
            self._table[first_tombstone] = _Slot(key, value)
            self._size += 1
            return first_tombstone
        raise OverflowError("Hash table is full")

    def search(self, key):
        """Return the value for key, or None if not found."""
        idx = self._find_index(key)
        return None if idx is None else self._table[idx].value

    def search_with_slot(self, key):
        """Return (value, slot_index) or (None, None)."""
        idx = self._find_index(key)
        return (None, None) if idx is None else (self._table[idx].value, idx)

    def delete(self, key):
        """Mark the record as deleted (tombstone). Returns True if removed."""
        idx = self._find_index(key)
        if idx is None:
            return False
        self._table[idx].deleted = True
        self._size -= 1
        return True

    def _find_index(self, key):
        for idx in self._probe(key):
            slot = self._table[idx]
            if slot is None:            # reached an empty slot -> key absent
                return None
            if not slot.deleted and slot.key == key:
                return idx
        return None

    def items(self):
        """Yield every live (key, value) pair."""
        for slot in self._table:
            if slot is not None and not slot.deleted:
                yield slot.key, slot.value

    def slot_items(self):
        """Yield (slot_index, key, value) for every live record."""
        for i, slot in enumerate(self._table):
            if slot is not None and not slot.deleted:
                yield i, slot.key, slot.value

    def __len__(self):
        return self._size

    @property
    def capacity(self):
        return self._capacity

    @property
    def load_factor(self):
        return self._size / self._capacity
