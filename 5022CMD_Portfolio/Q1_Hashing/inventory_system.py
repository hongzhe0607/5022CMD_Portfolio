"""
inventory_system.py
Command-line Pharmacy Inventory System built on the HashTable class.

Run:  python inventory_system.py
"""
import time

from hash_table import HashTable
from product import Medicine

# Pre-defined records loaded at start-up
PREDEFINED = [
    Medicine(1042, "Paracetamol 500mg", "Analgesic", 5.90, 120),
    Medicine(1105, "Ibuprofen 400mg", "Analgesic", 8.50, 80),
    Medicine(2031, "Amoxicillin 250mg", "Antibiotic", 15.00, 40, True),
    Medicine(2147, "Cetirizine 10mg", "Antihistamine", 12.30, 65),
    Medicine(3008, "Omeprazole 20mg", "Antacid", 18.90, 50, True),
    Medicine(3150, "Loratadine 10mg", "Antihistamine", 11.00, 70),
    Medicine(4022, "Metformin 500mg", "Antidiabetic", 9.80, 90, True),
    Medicine(4123, "Vitamin C 1000mg", "Supplement", 25.00, 150),
    Medicine(5013, "Salbutamol Inhaler", "Respiratory", 22.50, 30, True),
    Medicine(5119, "Oral Rehydration Salts", "Electrolyte", 3.50, 200),
    # 1143 % 101 == 32, the same home slot as 1042 -> demonstrates a
    # collision resolved by linear probing (it is placed in slot 33).
    Medicine(1143, "Chlorpheniramine 4mg", "Antihistamine", 6.40, 75),
]


class Inventory:
    """Keeps products in the hash table AND a 1-D array (list) for comparison."""

    def __init__(self, capacity=101):
        self.table = HashTable(capacity)
        self.array = []                     # same data, stored sequentially

    def add(self, med):
        slot = self.table.insert(med.product_id, med)
        # keep array in sync (replace if ID already exists)
        for i, m in enumerate(self.array):
            if m.product_id == med.product_id:
                self.array[i] = med
                break
        else:
            self.array.append(med)
        return slot

    def search_hash(self, pid):
        return self.table.search_with_slot(pid)

    def search_array(self, pid):
        """Linear search through the 1-D array - O(n)."""
        for m in self.array:
            if m.product_id == pid:
                return m
        return None

    def delete(self, pid):
        ok = self.table.delete(pid)
        self.array = [m for m in self.array if m.product_id != pid]
        return ok


# ---------------------------------------------------------------------- #
# Input helpers (validation so the program never crashes on bad input)
# ---------------------------------------------------------------------- #
def read_int(prompt, minimum=0):
    while True:
        try:
            v = int(input(prompt))
            if v >= minimum:
                return v
            print(f"  Please enter a number >= {minimum}.")
        except ValueError:
            print("  Invalid number, try again.")


def read_float(prompt):
    while True:
        try:
            v = float(input(prompt))
            if v >= 0:
                return v
            print("  Price cannot be negative.")
        except ValueError:
            print("  Invalid price, try again.")


def read_text(prompt):
    while True:
        v = input(prompt).strip()
        if v:
            return v
        print("  This field cannot be empty.")


def timed(func, *args, repeats=1000):
    """Run func many times and return (result, average seconds per call).
    A single lookup is too fast to time accurately, so we average many runs."""
    start = time.perf_counter_ns()
    for _ in range(repeats):
        result = func(*args)
    elapsed = time.perf_counter_ns() - start
    return result, elapsed / repeats / 1e9


# ---------------------------------------------------------------------- #
# Menu actions
# ---------------------------------------------------------------------- #
def do_insert(inv):
    pid = read_int("Enter Product ID: ", 1)
    if inv.table.search(pid) is not None:
        print(f"Product ID {pid} already exists - record will be updated.")
    name = read_text("Enter Product Name: ")
    category = read_text("Enter Category: ")
    price = read_float("Enter Price: ")
    stock = read_int("Enter Stock Quantity: ")
    rx = input("Prescription required? (y/n): ").strip().lower() == "y"
    slot = inv.add(Medicine(pid, name, category, price, stock, rx))
    print(f"Product inserted successfully into slot [{slot}]")


def do_search(inv):
    pid = read_int("Enter Product ID to search: ", 1)
    (med, slot), t_hash = timed(inv.search_hash, pid)
    _, t_arr = timed(inv.search_array, pid)
    if med:
        print(f"Product Found in slot [{slot}]!")
        print(med)
    else:
        print("Product not found.")
    print(f"Search completed in {t_hash:.9f} seconds (Hash Table)")
    print(f"Search completed in {t_arr:.9f} seconds (Array - same record)")


def do_edit(inv):
    pid = read_int("Enter Product ID to edit: ", 1)
    med = inv.table.search(pid)
    if not med:
        print("Product not found.")
        return
    print("Current:", med)
    print("Leave blank to keep the current value.")
    name = input(f"Name [{med.name}]: ").strip() or med.name
    price = input(f"Price [{med.price:.2f}]: ").strip()
    stock = input(f"Stock [{med.stock}]: ").strip()
    try:
        med.name = name
        med.price = float(price) if price else med.price
        med.stock = int(stock) if stock else med.stock
        print("Product updated:", med)
    except ValueError:
        print("Invalid value entered - update cancelled.")


def do_delete(inv):
    pid = read_int("Enter Product ID to delete: ", 1)
    print("Product deleted." if inv.delete(pid) else "Product not found.")


def do_list(inv):
    print(f"\n{'Slot':>5}  Product")
    for slot, _, med in sorted(inv.table.slot_items()):
        print(f"[{slot:>3}]  {med}")
    print(f"Records: {len(inv.table)} | Capacity: {inv.table.capacity} | "
          f"Load factor: {inv.table.load_factor:.2f}")


def main():
    inv = Inventory(capacity=101)
    for med in PREDEFINED:
        inv.add(med)

    actions = {"1": do_insert, "2": do_search, "3": do_edit,
               "4": do_delete, "5": do_list}
    while True:
        print("\n==== Pharmacy Inventory System ====")
        print("1. Insert Product\n2. Search Product\n3. Edit Product\n"
              "4. Delete Product\n5. List All Products\n6. Exit")
        choice = input("Enter choice: ").strip()
        if choice == "6":
            print("Exiting Inventory System. Goodbye!")
            break
        action = actions.get(choice)
        if action:
            action(inv)
        else:
            print("Invalid choice, please enter 1-6.")


if __name__ == "__main__":
    main()
