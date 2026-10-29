"""
fibonacci_threads.py
Compare computing Fibonacci(35), Fibonacci(38), Fibonacci(40)
  (a) with multithreading - one thread per number
  (b) without multithreading - one after another
over 10 rounds, timing in nanoseconds.

Run:  python fibonacci_threads.py
Quick test with smaller numbers:  python fibonacci_threads.py --quick
Extra I/O-bound demo:             python fibonacci_threads.py --io-demo
"""
import sys
import threading
import time

NUMBERS = [35, 38, 40]
ROUNDS = 10


def fibonacci(n):
    """Naive recursive Fibonacci.
    T(n) = T(n-1) + T(n-2) + c   ->   O(2^n)  (tight bound O(1.618^n))."""
    if n <= 1:                  # 1 comparison
        return n                # 1 return
    return fibonacci(n - 1) + fibonacci(n - 2)   # 2 subtractions, 2 calls, 1 addition, 1 return


# ---------------------------------------------------------------------- #
# Worker used by each thread: records its own start/end time and result.
# Each thread writes ONLY to its own index of the shared lists, so no two
# threads write the same memory location -> no lock is needed (no race).
# ---------------------------------------------------------------------- #
def worker(index, n, results, starts, ends):
    starts[index] = time.perf_counter_ns()
    results[index] = fibonacci(n)
    ends[index] = time.perf_counter_ns()


def run_with_threads(numbers):
    k = len(numbers)
    results, starts, ends = [None] * k, [0] * k, [0] * k
    threads = [threading.Thread(target=worker, args=(i, n, results, starts, ends))
               for i, n in enumerate(numbers)]
    for t in threads:
        t.start()               # all 3 threads begin running
    for t in threads:
        t.join()                # main thread waits until every thread is done
    # T = end time of thread that finished LAST - start time of thread that started FIRST
    elapsed = max(ends) - min(starts)
    return results, elapsed


def run_without_threads(numbers):
    start = time.perf_counter_ns()
    results = [fibonacci(n) for n in numbers]
    elapsed = time.perf_counter_ns() - start
    return results, elapsed


def experiment(title, runner, numbers, rounds):
    print(f"\n=== Fibonacci Computation ({title}) ===")
    times = []
    for r in range(1, rounds + 1):
        results, t = runner(numbers)
        times.append(t)
        values = ", ".join(f"Fib({n})={v}" for n, v in zip(numbers, results))
        print(f"Round {r:>2}: {values} | T = {t:,} ns", flush=True)
    avg = sum(times) / len(times)
    print(f"Average T ({title}): {avg:,.0f} ns  ({avg / 1e9:.3f} s)")
    print(f"Fastest: {min(times):,} ns | Slowest: {max(times):,} ns")
    return avg


def io_demo():
    """Shows a case where threads DO help: waiting (I/O), not computing.
    time.sleep releases the GIL, just like waiting for a network/disk reply."""
    def fake_download(seconds):
        time.sleep(seconds)

    jobs = [1.0, 1.0, 1.0]
    print("\n=== Extra demo: I/O-bound task (simulated 1-second downloads) ===")
    start = time.perf_counter_ns()
    for s in jobs:
        fake_download(s)
    seq = time.perf_counter_ns() - start

    start = time.perf_counter_ns()
    ts = [threading.Thread(target=fake_download, args=(s,)) for s in jobs]
    for t in ts:
        t.start()
    for t in ts:
        t.join()
    par = time.perf_counter_ns() - start
    print(f"Without threads: {seq:,} ns")
    print(f"With threads   : {par:,} ns")
    print(f"Multithreading reduced the time by {(seq - par) / seq * 100:.1f}%")


def main():
    numbers, rounds = NUMBERS, ROUNDS
    if "--quick" in sys.argv:
        numbers, rounds = [20, 22, 25], 3

    gil = getattr(sys, "_is_gil_enabled", lambda: True)()
    print(f"Python {sys.version.split()[0]} | GIL enabled: {gil}")

    avg_mt = experiment("With Multithreading", run_with_threads, numbers, rounds)
    avg_st = experiment("Without Multithreading", run_without_threads, numbers, rounds)

    diff = (avg_st - avg_mt) / avg_st * 100
    print("\n=== Summary ===")
    print(f"Average with multithreading   : {avg_mt:,.0f} ns")
    print(f"Average without multithreading: {avg_st:,.0f} ns")
    if diff > 0:
        print(f"Observation: Multithreading reduced the average time by {diff:.1f}%.")
    else:
        print(f"Observation: Multithreading was {-diff:.1f}% SLOWER on average "
              f"(CPU-bound work + GIL = no parallel speed-up).")

    if "--io-demo" in sys.argv:
        io_demo()


if __name__ == "__main__":
    main()
