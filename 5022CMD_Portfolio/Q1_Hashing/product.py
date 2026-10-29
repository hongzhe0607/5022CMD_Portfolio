"""
product.py
Entity class for a pharmacy product (medicine).
"""


class Medicine:
    """
    A medicine sold by the pharmacy.

    Attribute choices:
      product_id   (int)   - unique key used for hashing; integers hash fast
                              and evenly with the division method.
      name         (str)   - display name incl. strength, e.g. "Paracetamol 500mg".
      category     (str)   - e.g. "Analgesic", "Antibiotic" for grouping.
      price        (float) - selling price in RM (2 decimal places).
      stock        (int)   - quantity on hand; whole units only.
      prescription (bool)  - True if a doctor's prescription is required.
    """

    def __init__(self, product_id, name, category, price, stock, prescription=False):
        self.product_id = int(product_id)
        self.name = str(name)
        self.category = str(category)
        self.price = float(price)
        self.stock = int(stock)
        self.prescription = bool(prescription)

    def __str__(self):
        rx = "Yes" if self.prescription else "No"
        return (f"ID: {self.product_id} | Name: {self.name} | Category: {self.category} | "
                f"Price: RM{self.price:.2f} | Stock: {self.stock} | Prescription: {rx}")
