import itertools
import time
from collections import defaultdict

class Apriori:
    def __init__(self,data_file,support):
        self.data_file = data_file
        self.support = support
        self.candidate_counts = defaultdict(int)
        self.frequent_itemsets = {}

    def count_single_items(self,item):
        # Increment the count of a single item in candidate dict
        self.candidate_counts[item] += 1
        return item
    
    def generate_candidates(self, prev_level, k):
        # ensure all keys in pre_level are converted to tuple format
        prev_items = [item if isinstance(item, tuple) else (item,) for item in prev_level.keys()]
        candidates = {}
        for p in prev_items:
            for q in prev_items:
                #here show if previous key k-2 item same ,then combine p and q
                if p[:k-2] == q[:k-2] and p[k-2]<q[k-2]:
                    candidate = p + (q[k-2],) # ex. candidate = (1, 2) + (3,) = (1, 2, 3)
                    candidates[candidate] = 0

        # Remove the all candidate itemsets which are not in previous level.
        invalid_candidates = [c for c in candidates if any(sub not in prev_level for sub in itertools.combinations(c, k-1))]
        for invalid in invalid_candidates:
            candidates.pop(invalid, None)
        
        return candidates
    
    def filter_candidates(self, candidates, baskets, k):
        # Iterate through each basket, check for candidate itemsets it contains, and count them.
        for basket in baskets:
            for candidate in itertools.combinations(basket, k):
                if candidate in candidates:
                    candidates[candidate] += 1
        
        # Return candidates whose support is greater than or equal to the threshold.
        return {item : count for item, count in candidates.items() if count >= self.support}

    def find_frequent_itemsets(self, verbose=False):
        baskets = []
        # Read baskets from the data file and count the support for single items.
        with open(self.data_file, 'r') as f:
            for line in f:
                basket = [self.count_single_items(int(item)) for item in line.strip().split()]
                baskets.append(basket)
        
        #Generate frequent 1-itemsets
        self.frequent_itemsets[1] = {item if isinstance(item, tuple) else (item,):count for item, count in self.candidate_counts.items() if count >=self.support}
       
        k = 1
        while self.frequent_itemsets.get(k):
            if verbose:
                print(f"Level {k} | Frequent itemsets: {len(self.frequent_itemsets[k])}")
            k += 1
            candidates = self.generate_candidates(self.frequent_itemsets[k-1], k)
            self.frequent_itemsets[k] = self.filter_candidates(candidates, baskets, k)

        #remove the last layers empty frequent itemset
        self.frequent_itemsets.pop(k, None)
        return self.frequent_itemsets
    
class AssociationRules:
    def generate_rules(self, frequent_itemsets, min_confidence, verbose=False):
        rules = []
        for k, itemsets in frequent_itemsets.items():
            if k < 2:
                continue
            
            for itemset,support in itemsets.items():
                for antecedent in itertools.combinations(itemset, k-1):
                    consequent = tuple(set(itemset) - set(antecedent))
                    if not consequent:
                        continue
                    confidence = support / frequent_itemsets[k-1][antecedent]
                    if confidence >= min_confidence:
                        rule = {
                            "rule": f"{antecedent} -> {consequent}",
                            "support": support,
                            "confidence": confidence,
                        }
                        rules.append(rule)
                        if verbose:
                            print(rule["rule"], f"| Support: {rule['support']}, Confidence: {rule['confidence']:.2f}")
        return rules

def main(args):
    t_start = time.time()
    apriori = Apriori(data_file=args.dataset_file, support=args.support)
    frequent_itemsets = apriori.find_frequent_itemsets(verbose=args.verbose)
    if args.verbose:
        print(f"Time for sub-problem 1 (frequent itemsets): {time.time() - t_start:.2f}s")

    # Generate association rules
    t_start = time.time()
    association_rules = AssociationRules()
    rules = association_rules.generate_rules(frequent_itemsets, min_confidence=args.min_confidence, verbose=args.verbose)
    if args.verbose:
        print(f"Time for sub-problem 2 (association rules): {time.time() - t_start:.2f}s")

    print("\nNumber of rules generated:", len(rules))


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Apriori Algorithm with Association Rules")
    parser.add_argument("--dataset_file", type=str, required=True, help="Path to the dataset file (.dat)")
    parser.add_argument("--support", type=int, required=True, help="Minimum support threshold")
    parser.add_argument("--min_confidence", type=float, required=True, help="Minimum confidence threshold")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()

    main(args)
