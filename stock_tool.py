class StockLookup:  # Keep stock lookup separate from conversation rules.
    def __init__(self, stock):  # Receive product names mapped to counts.
        self.stock = stock  # Store the supplied stock dictionary on this tool.

    def find_product(self, text):  # Find the first known product in a message.
        for product in self.stock:  # Examine each stored product name.
            if product.lower() in text.lower():  # Match without case differences.
                return product  # Preserve the dictionary key for count lookup.
        return None  # Tell the caller no known product was mentioned.

    def count_for(self, product):  # Retrieve one product's available quantity.
        if product in self.stock:  # Distinguish an unknown item from zero stock.
            return self.stock[product]  # Return the stored count, including zero.
        return None  # Signal an unknown product instead of guessing a count.
