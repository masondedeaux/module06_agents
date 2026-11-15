class OrderLookup:  # Group order data and lookup actions in a separate tool.
    def __init__(self, orders):  # Receive the dictionary when creating a tool.
        self.orders = orders  # Keep the orders so later methods can read them.

    def find_order_id(self, text):  # Search a message for a known order ID.
        for order_id in self.orders:  # Check each ID in dictionary order.
            if order_id in text.upper():  # Ignore the message's letter case.
                return order_id  # Return the first matching known ID.
        return None  # Signal a failed lookup without inventing an ID.

    def find_status(self, order_id):  # Look up the status for one exact ID.
        if order_id in self.orders:  # Check existence before reading the value.
            return self.orders[order_id]["status"]  # Return the stored status.
        return None  # Report an unknown order without raising KeyError.
    def look_up_order(self, order_id):
        """Look up the status of one order.

        Args:
            order_id: The order ID, like A100.
        """
        found = self.find_order_id(order_id)
        if found is None:
            return "No order with that ID was found. Order IDs look like A100."
        return f"Order {found} is {self.find_status(found)}."

    def change_address(self, order_id, new_address):
        """Change the shipping address on one order. Only an approval calls this."""
        self.orders[order_id]["address"] = new_address