# 5022CMD Advanced Algorithms – Portfolio

Python 3.10+ required. No external libraries needed.

| Folder | Question | Run |
|---|---|---|
| `Q1_Hashing/` | Hash table (open addressing, linear probing) + Pharmacy Inventory System | `python inventory_system.py` |
| | Hash table vs array search experiment | `python performance_test.py` |
| `Q2_Graph/` | Directed graph + University Course Prerequisite System | `python course_system.py` |
| `Q3_Concurrency/` | Fibonacci with / without multithreading (10 rounds) | `python fibonacci_threads.py` |
| | Quick version (small numbers) | `python fibonacci_threads.py --quick` |
| | Plus I/O-bound threading demo | `python fibonacci_threads.py --io-demo` |

## Files
- `Q1_Hashing/hash_table.py` – generic `HashTable` class (insert, search, delete, auto-resize)
- `Q1_Hashing/product.py` – `Medicine` entity class
- `Q1_Hashing/inventory_system.py` – CLI: insert, search (with timing), edit, delete, list
- `Q1_Hashing/performance_test.py` – timing experiment for 100 to 50,000 records
- `Q2_Graph/graph.py` – generic directed `Graph` (addVertex, addEdge, listIncomingAdjacentVertex, …)
- `Q2_Graph/course.py` – `Course` entity class
- `Q2_Graph/course_system.py` – menu program (4 mandatory + all 4 advanced features)
- `Q3_Concurrency/fibonacci_threads.py` – threading experiment

Note: the full Q3 run takes several minutes because Fibonacci(40) is computed recursively 20 times.
