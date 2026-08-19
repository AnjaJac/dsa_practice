"""
P-6.36: FIFO capital gain calculator.
Reads a sequence of stock transactions form standard input, one per line,
in the form:
    buy x share(s) at $y each
    sell x share(s) at $y each

(x and y are both integers; "share"/"shares" are both accepted.)
Transactions are assumed to occur on consecutive days, in the order given. Using
the FIFO protocol: shares sold are the ones that have been held the longest.
The program computes and prints the total capital gain (or loss/negative gain)
for the whole sequence.

The FIFObehavior is exactly what a Queue ADT provides, so purchase lots
are enqueued as they're bought and dequeued (oldest first) as they're sold.
The queue itself is a hand-rolled, array-based circular queue (the same design
as Code Fragment 6.6), not Python's built-in collections.deque.
"""

import re
import sys

# Array-based circular Queue ADT

class Empty(Exception):
    """Error raised when and operation is performed on an empty queue."""
    pass

class ArrayQueue:
    """FIFO queue implementation using a Python list as an underlying
    circular array, with dynamic resizing (amortized O(1) enqueue and dequeue).
    """

    DEFAULT_CAPACITY = 10       # moderate capacity for all new queues

    def __init__(self):
        self._data = [None] * ArrayQueue.DEFAULT_CAPACITY
        self._size = 0
        self._front = 0

    def __len__(self):
        return self._size

    def is_empty(self):
        return self._size == 0

    def first(self):
        """
        Return (but do not remove) the element at the front of the queue.
        This returns the actual object, so callers may mutate it
        in place (used here to partially consume a lot).
        """
        if self.is_empty():
            raise Empty("Queue is empty")
        return self._data[self._front]

    def dequeue(self):
        """Remove and return the first element of the queue."""
        if self.is_empty():
            raise Empty("Queue is empty")
        answer = self._data[self._front]
        self._data[self._front] = None      # help garbage collection
        self._front = (self._front + 1) % len(self._data)
        self._size -=1
        if 0 < self._size < len(self._data) // 4: # shrink if too sparse
            self._resize(len(self._data)//2)
        return answer

    def enqueue(self, e):
        """ Add an element to the back of the queue."""
        if self._size == len(self._data):
            self._resize(2*len(self._data))     #double the array
        avail = (self._front + self._size) % len(self._data)
        self._data[avail] = e
        self._size += 1

    def _resize(self, cap):
        """
        Resize the underlying array to a new capacity >= current size.
        """
        old = self._data
        self._data = [None] * max(cap, 1)
        walk = self._front
        for k in range(self._size):
            self._data[k] = old[walk]
            walk = (walk + 1) % len(old)
        self._front = 0

# Domain model: a purchase lot

class Lot:
    """
    A block of shares bought together as the same price.
    Mutable so that a sell can partially consume it ( shrink "shares")
    without dequeuing/re-enqueuing
    """
    def __init__(self, shares, price):
        self.shares = shares
        self.price = price

    def __repr__(self):
        return f"Lot ({self.shares} @${self.price})"

# Transaction parsing
_TRANSACTION_RE = re.compile(
    r"^\s*(buy|sell)\s+(\d+)\s+shares?\s+at\s+\$(\d+(?:\.\d+)?)\s+each\.?\s*$",
    re.IGNORECASE,
)

def parse_transaction(line):
    """
    Parse a line like 'buy 100 shares ant $20 each' into 
    (action, shares, price)> Returns None for a blank lines.
    Raises Value Error for anything else that doesn't match the expected format.
    """
    if not line.strip():
        return None
    match = _TRANSACTION_RE.match(line)
    if not match:
        raise ValueError(f"Could not parse transaction: {line!r}")
    action, shares, price = match.groups()
    return action.lower(), int(shares), float(price)

# FIFO capital gain calculation

def compute_capital_gain(transactions):
    """Given an iterable of (action, shares, price) transactions, in
    order, compute the total capital gain (or loss) using the FIFO
    protocol. Returns a float."""
    lots = ArrayQueue()
    total_gain = 0.0
 
    for action, shares, price in transactions:
        if action == "buy":
            lots.enqueue(Lot(shares, price))
 
        elif action == "sell":
            remaining = shares
            while remaining > 0:
                if lots.is_empty():
                    raise ValueError(
                        "Trying to sell more shares than have been bought."
                    )
                lot = lots.first()
                taken = min(remaining, lot.shares)
                total_gain += taken * (price - lot.price)
                lot.shares -= taken
                remaining -= taken
                if lot.shares == 0:
                    lots.dequeue()
 
        else:
            raise ValueError(f"Unknown action: {action!r}")
 
    return total_gain

# Driver: read transactions from stdin until EOF
def main():
    transactions = []
    for line in sys.stdin:
        parsed = parse_transaction(line)
        if parsed is not None:
            transactions.append(parsed)
 
    gain = compute_capital_gain(transactions)
 
    if gain >= 0:
        print(f"Total capital gain: ${gain:,.2f}")
    else:
        print(f"Total capital loss: ${-gain:,.2f}")
 
 
if __name__ == "__main__":
    main()