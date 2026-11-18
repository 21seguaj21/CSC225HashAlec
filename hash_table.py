"""CSC 225 - Hash table starter. Complete the TODO sections."""

# These prime sizes are provided; you do not need to test for prime numbers.
SIZES = [11, 23, 47, 97, 197, 397]


class HashTable:
    def __init__(self, method="linear", hash_method="mod"):
        self.method = method           # linear, quadratic, or chaining
        self.hash_method = hash_method # mod or digit
        self.capacity = 11
        self.count = 0

        if method == "chaining":
            # Each position must have its OWN list.
            # [[]] * 11 would repeat references to the SAME list.
            self.table = [[] for i in range(self.capacity)]
        else:
            self.table = [None] * self.capacity

    def hash_key(self, key):
        # These two hash functions are already provided.
        if self.hash_method == "mod":
            return key % self.capacity
        total = 0
        for digit in str(abs(key)):
            total += int(digit)
        return total % self.capacity

    def insert(self, key):
        if self.search(key):
            return

        limits = {"linear": 0.70, "quadratic": 0.50, "chaining": 0.75}
        if (self.count + 1) / self.capacity > limits[self.method]:
            self.resize()

        start = self.hash_key(key)

        if self.method == "chaining":
            self.table[start].append(key)
            self.count += 1
            return

        for i in range(self.capacity):
            if self.method == "linear":
                idx = (start + i) % self.capacity
            else:  # quadratic
                idx = (start + i * i) % self.capacity

            if self.table[idx] is None:
                self.table[idx] = key
                self.count += 1
                return

        print("Table is full; cannot insert", key)

    def search(self, key):
        start = self.hash_key(key)

        if self.method == "chaining":
            return key in self.table[start]

        for i in range(self.capacity):
            if self.method == "linear":
                idx = (start + i) % self.capacity
            else:  # quadratic
                idx = (start + i * i) % self.capacity

            if self.table[idx] is None:
                return False
            if self.table[idx] == key:
                return True
        return False

    def resize(self):
        old_table = self.table
        old_method = self.method

        current_index = SIZES.index(self.capacity)
        if current_index + 1 >= len(SIZES):
            print("Maximum table size reached.")
            return
        self.capacity = SIZES[current_index + 1]

        if old_method == "chaining":
            self.table = [[] for _ in range(self.capacity)]
        else:
            self.table = [None] * self.capacity

        self.count = 0

        if old_method == "chaining":
            for bucket in old_table:
                for key in bucket:
                    self.insert(key)
        else:
            for key in old_table:
                if key is not None:
                    self.insert(key)

    def show(self):
        print("\nMethod:", self.method, "| Hash:", self.hash_method)
        print("Size:", self.capacity, "| Values:", self.count)
        print("Load factor:", round(self.count / self.capacity, 2))
        for i in range(self.capacity):
            print(i, ":", self.table[i])
