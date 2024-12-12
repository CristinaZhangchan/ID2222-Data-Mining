class Shingle:
    def __init__(self, k):
        # k - shingle or k - gram for a document is that the sequence of k tokens
        self.k = k
    
    def shingling(self, document):
        # Create an empty set to store the hashed shingles
        hashed_shingles = set()
        # Iterate over the document to extract each k-shingle
        for i in range(len(document) - self.k + 1):
            # Extract a k-shingle from the document
            shingle = document[i:i + self.k]
            # Hash the k-shingle and add it to the set as an integer
            hashed_shingle = int(hash(shingle) & 0xFFFFFFFF)
            hashed_shingles.add(hashed_shingle)
        return hashed_shingles
