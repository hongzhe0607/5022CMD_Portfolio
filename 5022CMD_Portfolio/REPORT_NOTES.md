# Report Notes – 5022CMD Portfolio

These are study notes for writing your PDF report. Rewrite them in your own
words, add your own screenshots, and use your own timing numbers. You will be
asked about this in the VIVA (40% of the mark), so make sure you can explain
every point without reading it.

---

## Question 1 – Hashing

### i. Slot/bucket structure (screenshot `_Slot` class + `_probe`/`insert` in `hash_table.py`)
- Each slot is either `None` (never used) or a `_Slot` object with `key`, `value`, `deleted`.
- **Why open addressing with a flat array:** all records sit in one contiguous Python list,
  so there are no extra linked lists/pointers per bucket (unlike separate chaining). Simple to
  implement and memory-efficient.
- **Why linear probing (`(h + i) % capacity`):** simplest probe sequence, guaranteed to visit every
  slot once, and neighbouring slots are checked in order (good cache locality).
- **Weakness and how it's handled:** linear probing causes *primary clustering* (runs of filled
  slots get longer). We keep the **load factor ≤ 0.7** and double the table to the next prime when
  it is exceeded, so probe chains stay short.
- **Why the `deleted` flag (tombstone):** if we simply set a deleted slot to `None`, a later search
  for a key further along the same probe chain would stop early at that empty slot and wrongly say
  "not found". The tombstone keeps the chain intact, and `insert` reuses tombstone slots.
- **Hash function:** division method `key % capacity` with a prime capacity (101) so integer IDs
  spread evenly. Strings use a polynomial hash (×31) because Python's built-in `hash()` for strings
  changes every run.
- **Collision example to show:** IDs 1042 and 1143 both hash to slot 32 (1042 % 101 = 32,
  1143 % 101 = 32). 1042 goes in slot 32, 1143 is probed to slot 33. Screenshot option 5 (List)
  and a search for 1143 to prove it.

### ii. Entity class (screenshot `Medicine` in `product.py`)
| Attribute | Type | Reason |
|---|---|---|
| product_id | int | Unique key; integers are fast to hash and compare |
| name | str | Includes strength, e.g. "Paracetamol 500mg" |
| category | str | Grouping, e.g. Analgesic, Antibiotic |
| price | float | Money with decimals (RM) – mention `Decimal` would avoid rounding errors in a real system |
| stock | int | Whole units only, cannot be fractional |
| prescription | bool | Only two states: needs a prescription or not |

### iii. Experiment (screenshot `performance_test.py` code + output)
- Method: same records inserted into both structures; search the front, middle, end, and a missing
  key; each search repeated 2,000 times and averaged (one lookup is shorter than timer resolution);
  sizes 100, 1,000, 10,000, 50,000; fixed random seed so results are repeatable.
- Sample result on the test machine:

| Records | Target | Hash table (ns) | Array (ns) |
|---|---|---|---|
| 100 | end | 376 | 2,621 |
| 1,000 | end | 849 | 28,297 |
| 10,000 | end | 410 | 262,324 |
| 50,000 | end | 556 | 1,395,006 |

- **Analysis:** hash table time stays ~flat (≈300–1,100 ns) regardless of size → average **O(1)**:
  compute hash, jump to slot, maybe probe a few neighbours. Array time grows ~10× when data grows
  10× → **O(n)** linear search. Missing keys are the array's worst case (must check every element).
- **Honest point (good for marks):** for the *first* element, the array is faster (~90 ns vs ~400 ns)
  because it finds it on the first comparison, while the hash table always pays the cost of calling
  the hash function. With very small data, the difference is tiny.
- **Conclusion:** for an inventory searched by product ID, the hash table is superior because its
  search time doesn't depend on the number of products. Trade-offs: uses extra empty slots (load
  factor), can't search by name/range efficiently, and worst case is O(n) if many keys collide.

---

## Question 2 – Graph

**Design:** adjacency list using two dictionaries of sets: `_out[v]` (edges leaving v) and `_in[v]`
(edges entering v). Edge direction = **prerequisite → course it unlocks** (CS101 → CS201).
- Prerequisites of X = **incoming** vertices of X → `listIncomingAdjacentVertex`, O(in-degree).
- Courses unlocked by X = **outgoing** vertices → `listOutgoingAdjacentVertex`.
- Storing `_in` costs a little extra memory but avoids scanning every vertex (O(V+E)).
- Sets prevent duplicate edges and give O(1) add/remove.
- **Abstraction:** `graph.py` never imports `Course`; vertices can be any hashable object.
  `CourseRegistry` is the "glue" between the domain and the graph. The Course objects themselves
  are the vertices; a `code → Course` dictionary gives O(1) lookup by code.

**Features to screenshot and explain:**
1. View all courses – `view_all` (sorted by code).
2. View details – `view_details` uses `full_details()` (ignores visibility).
3. Prerequisites – `view_prereqs` → `listIncomingAdjacentVertex`.
4. Unlocked courses – `view_unlocked` → `listOutgoingAdjacentVertex`.
5. Advanced (a) add course → `addVertex`.
6. Advanced (b) core/elective profile → `Course.profile()`.
7. Advanced (c) add prerequisite → `addEdge(Y, X)`. **Extra:** refuses a cycle using DFS
   `hasPath(X, Y)`, e.g. making CS401 a prerequisite of CS101 is rejected because CS101 already
   leads to CS401 (nobody could ever take either course).
8. Advanced (d) remove prerequisite → `removeEdge(Y, X)`.

**Test data:** CS101→CS201, CS102→CS201, CS101→CS202, CS201→CS301, CS102→CS301, CS201→CS302,
CS202→CS303, CS302→CS303, CS301→CS401, CS302→CS401. Show: a course with 0 prerequisites (CS101),
a course with 2, a course that unlocks nothing (CS401), an elective vs core profile, an invalid code.

---

## Question 3 – Concurrency

### 1. Concurrent or parallel?
- Standard Python (CPython) has the **Global Interpreter Lock (GIL)**: only one thread can execute
  Python bytecode at a time. So multithreading in Python is **concurrent** (threads take turns,
  interleaved) but **not parallel** for CPU-bound Python code.
- Threads *do* run at the same time while waiting on I/O (file, network, `time.sleep`) because the
  GIL is released while waiting.
- For true parallelism: `multiprocessing` / `ProcessPoolExecutor` (separate processes, each with its
  own GIL). Note: Python 3.13+ offers an experimental *free-threaded* build without the GIL, but the
  normal installer still has the GIL (the program prints "GIL enabled: True").

### 2/5i. Big-O of recursive Fibonacci (screenshot `fibonacci`)
Count primitive operations per call:
- Base case (n ≤ 1): 1 comparison + 1 return = **2**
- Recursive case: 1 comparison + 2 subtractions + 2 calls + 1 addition + 1 return = **7** (+ the work
  of the two calls)

Recurrence: **T(n) = T(n−1) + T(n−2) + 7**, T(0)=T(1)=2.
- Since T(n−1) ≥ T(n−2): T(n) ≤ 2T(n−1) + 7 → expanding gives T(n) ≤ 2ⁿ·c → **O(2ⁿ)**.
- Number of calls = 2·Fib(n+1) − 1, which grows like φⁿ (φ ≈ 1.618), so the tight bound is
  **Θ(1.618ⁿ)**, still exponential and conventionally written O(2ⁿ).
- Meaning: each +1 to n multiplies time by ~1.6. Fib(40) ≈ 1.6⁵ ≈ 11× slower than Fib(35) – check
  this against your own timings. Reason: the same sub-problems are recomputed many times
  (Fib(38) is computed twice inside Fib(40), Fib(37) three times…).
- Mention: an iterative loop or memoization would make it O(n) – but the slow version is useful
  for this experiment because it gives a heavy CPU load.

### 5ii. Comparison (fill in your own numbers)
| | Average T |
|---|---|
| With multithreading | ________ ns (test machine: 20,454,730,050 ns) |
| Without multithreading | ________ ns (test machine: 20,214,650,544 ns) |

On the test machine multithreading was 1.2% *slower*. Replace with your own run
(see `Q3_Concurrency/sample_output.txt` for the full test-machine output).

Expected finding: times are almost the same (threaded is often slightly slower). The sample output
in the brief shows a 49.9% reduction – that would only happen without a GIL or with processes, so
explain why your result is different.

### 5iii. Multithreading code (screenshot `worker` + `run_with_threads`)
- One `threading.Thread` per number (3 threads), `target=worker`.
- Each thread records its own start time, computes, records its end time.
- `start()` launches all three; `join()` makes the main thread wait for all to finish.
- **T = max(end times) − min(start times)**, matching the brief's diagram (t2 − t1).
- `time.perf_counter_ns()` is used (nanoseconds, monotonic – not affected by clock changes).
- **Data consistency:** each thread writes only to its own index in the shared lists, so no two
  threads write the same location → no race condition and no lock needed. If they updated one shared
  counter (e.g. `total += x`), a `threading.Lock` would be needed.

### 5iv. Why no speed-up + where threads help
- Fibonacci is **CPU-bound**: pure computation, never waits. With the GIL the 3 threads take turns
  on one core, so total work is the same as running them one after another, plus overhead for
  creating threads and switching between them (the interpreter switches roughly every 5 ms).
- Threads help when tasks are **I/O-bound**: downloading several web pages, reading many files,
  querying a database, a GUI staying responsive while a download runs. Run with `--io-demo`: three
  1-second simulated downloads take ~3 s sequentially but ~1 s with threads.
- For CPU-bound work, use `multiprocessing` to get real parallel speed-up on multiple cores.

---

## Challenges & Reflection (max 2 pages – must be YOUR experience)
Ideas to write about honestly: understanding tombstones in deletion; why timing a single search
gave 0 or random numbers (needed repetition); choosing edge direction for prerequisites;
preventing circular prerequisites; being surprised that threads did not speed things up; managing
time around other modules.

## AI acknowledgement (required by the brief)
State that you used Claude (Anthropic) and for what, e.g. "to help generate initial code and
explanations, which I then tested, modified and studied".
