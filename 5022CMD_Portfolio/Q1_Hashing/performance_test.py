"""
performance_test.py
Experiment: compare search time of the Hash Table vs a 1-D array (Python list).

The SAME medicine records are inserted into both structures. For each data
size we search for:
   - a record near the FRONT of the array  (best case for linear search)
   - a record in the MIDDLE
   - a record at the END                    (worst case for an existing key)
   - a record that does NOT exist           (array must scan every element)
Each search is repeated many times and averaged, because one lookup takes
less time than the timer resolution.

Run:  python performance_test.py
"""
import random
import time

from hash_table import HashTable
from product import Medicine

REPEATS = 2000
SIZES = [100, 1_000, 10_000, 50_000]


def build_data(n, seed=42):
    rng = random.Random(seed)              # fixed seed -> repeatable results
    ids = rng.sample(range(100_000, 1_000_000), n)
    return [Medicine(pid, f"Medicine-{pid}", "General",
                     round(rng.uniform(1, 100), 2), rng.randint(0, 500))
            for pid in ids]


def array_search(array, pid):
    for med in array:                       # linear search O(n)
        if med.product_id == pid:
            return med
    return None


def avg_ns(func, *args):
    start = time.perf_counter_ns()
    for _ in range(REPEATS):
        func(*args)
    return (time.perf_counter_ns() - start) / REPEATS


def run():
    print("=== Search Performance: Hash Table vs 1-D Array ===")
    print(f"(average of {REPEATS} searches each, times in nanoseconds)\n")
    header = f"{'Records':>8} | {'Target':<10} | {'Hash Table':>12} | {'Array':>14} | {'Speed-up':>9}"
    print(header)
    print("-" * len(header))

    for n in SIZES:
        records = build_data(n)
        table = HashTable(capacity=HashTable._next_prime(int(n / 0.5)))
        array = []
        for med in records:
            table.insert(med.product_id, med)
            array.append(med)

        targets = {
            "front": records[0].product_id,
            "middle": records[n // 2].product_id,
            "end": records[-1].product_id,
            "missing": 1,                   # not in data
        }
        for label, pid in targets.items():
            # sanity check: both structures must give the same answer
            assert table.search(pid) is array_search(array, pid)
            t_hash = avg_ns(table.search, pid)
            t_arr = avg_ns(array_search, array, pid)
            print(f"{n:>8} | {label:<10} | {t_hash:>12,.0f} | {t_arr:>14,.0f} | "
                  f"{t_arr / t_hash:>8.1f}x")
        print("-" * len(header))

    print("\nObservation: hash-table search time stays roughly constant as the")
    print("data grows (O(1) average), while array search time grows with the")
    print("number of records (O(n)), especially for 'end' and 'missing' keys.")


if __name__ == "__main__":
    run()
