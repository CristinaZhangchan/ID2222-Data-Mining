class CompareSignatures:
    @staticmethod
    def estimate_similarity(signature1, signature2):
        if len(signature1) != len(signature2):
            raise ValueError("Signatures must be of the same length")
        
        matches = sum(1 for a, b in zip(signature1, signature2) if a == b)
        return matches / len(signature1)

