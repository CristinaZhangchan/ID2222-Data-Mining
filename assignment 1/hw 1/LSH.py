import time

class LSH:
    def __init__(self, band, threshold):
        # initializr band and threshold value
        self.band = band
        self.threshold = threshold

    def hash_segment(self, segment):
        #Use string concatenation to create hash values for segments
        return "-".join(map(str, segment))

    def find_similar_pairs(self, signatures):
        #Store all similar pairs of documents
        similar_pairs_set = set()
        num_rows = len(signatures[0])
        segment_size = num_rows // self.band

        for b in range(self.band):
            bucket = {}
            for doc_id, signature in enumerate(signatures):
                # Calculates a segmented hash of the current band
                segment = signature[b * segment_size: (b + 1) * segment_size]
                segment_hash = self.hash_segment(segment)

                # Put documents with the same hash into the same bucket
                if segment_hash not in bucket:
                    bucket[segment_hash] = []
                bucket[segment_hash].append(doc_id)

            # Find a pair of documents in the same bucket
            for doc_ids in bucket.values():
                if len(doc_ids) > 1:
                    for i in range(len(doc_ids)):
                        for j in range(i + 1, len(doc_ids)):
                            similar_pairs_set.add((doc_ids[i], doc_ids[j]))

        # Perform a similarity filter on the found document pairs
        filtered_pairs = []
        for i, j in similar_pairs_set:
            # calculate Jaccard similarity
            sim = sum(1 for a, b in zip(signatures[i], signatures[j]) if a == b) / float(num_rows)
            if sim >= self.threshold:
                filtered_pairs.append((i, j))

        return filtered_pairs
