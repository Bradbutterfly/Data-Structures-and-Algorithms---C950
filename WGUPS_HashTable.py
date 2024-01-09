class HashTable:
    def __init__(self, initial_capacity=20):
        """Initialize the hash table."""
        self.table = [[] for _ in range(initial_capacity)]

    def _get_bucket_index(self, key):
        """Compute the bucket index for the given key."""
        return abs(hash(key)) % len(self.table)

    def insert(self, key, item):
        """Insert or update a key-value pair."""
        index = self._get_bucket_index(key)
        bucket = self.table[index]

        for kv in bucket:
            if kv[0] == key:
                kv[1] = item
                return

        bucket.append([key, item])

    def lookup(self, key):
        """Retrieve an item by key. Return None if not found."""
        index = self._get_bucket_index(key)
        bucket = self.table[index]

        for k, v in bucket:
            if k == key:
                return v

        return None

    def remove(self, key):
        """Remove a key-value pair using the key."""
        index = self._get_bucket_index(key)
        bucket = self.table[index]

        for i, (k, _) in enumerate(bucket):
            if k == key:
                del bucket[i]
                return
