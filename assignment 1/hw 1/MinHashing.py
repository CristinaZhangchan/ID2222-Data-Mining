import random

class MinHashing:
    def __init__(self, n, max_hash=10000):
        """
        n is the length of signature 
        """
        self.n = n
        self.hash_funcs = [self._generate_hash_function(max_hash) for _ in range(n)]

    def _generate_hash_function(self, max_hash):
        """
        generate a random hash argu
        param:
        max_hash (int): max hash argu
        return:
        function: hash argu
        """
        a = random.randint(1, max_hash)
        b = random.randint(0, max_hash)
        return lambda x: (a * x + b) % max_hash

    def compute_signature(self, shingle_set):
        """
        Generates a MinHash signature for a given set of hash shards
        Para:
        shingle_set (set): a set containing hash shards
        Return:
        list: a MinHash signature of length n
        """
        signature = []
        for hash_func in self.hash_funcs:
            min_hash_val = min(hash_func(shingle) for shingle in shingle_set)
            signature.append(min_hash_val)
        return signature

