import math
import hashlib
import logging


class HyperLogLog:
    def __init__(self, precision=4):
        super().__init__()
        if precision < 4 or precision > 16:
            raise ValueError("Precision must be between 4 and 16")
        self.precision = precision
        self.num_registers = 2 ** precision
        self.registers = [0] * self.num_registers

        if precision == 4:
            self.alpha = 0.673
        elif precision == 5:
            self.alpha = 0.697
        elif precision == 6:
            self.alpha = 0.709
        else:
            self.alpha = 0.7213 / (1 + 1.079 / self.num_registers)

    def add(self, data: str) -> None:
        h = int(hashlib.md5(data.encode()).hexdigest(), 16)
        h = abs(h)  # Ensure positive hash values

        # get the first precision bits of the hash value to determine the register index j.
        j = h & (self.num_registers - 1)
        # get the remaining bits
        w = h >> self.precision
        # count the number of trailing 0s
        self.registers[j] = max(self.registers[j], Utils.count_trailing_zeros(w))

    def estimate_cardinality(self) -> int: # Use HyperLogLog's cardinality estimation formula
        Z = sum(2 ** -m for m in self.registers)
        E = self.alpha * self.num_registers ** 2 / Z

        # Small range correction
        if E <= 5 / 2 * self.num_registers:
            V = self.registers.count(0)
            if V > 0:
                E = self.num_registers * math.log(self.num_registers / V)
        # Large range correction
        elif E > 1 / 30 * (2 ** 32):
            E = -(2 ** 32) * math.log(1 - (E / 2 ** 32))
        
        return int(E)

    def merge(self, other: 'HyperLogLog') -> None:
        for i in range(self.num_registers):
            self.registers[i] = max(self.registers[i], other.registers[i])

#Estimated cardinality: 692172

#bitset to represent the positions of the least significant 1-bit of hash values.
#estimating the number of unique elements i data stream
class FlajoletMartinCounter:
    def __init__(self):
        super().__init__()
        self.bitset = 0 
        self.phi = 0.77351

    def add(self, data: int) -> None:
        hashed_data = abs(int(hashlib.md5(str(data).encode()).hexdigest(), 16)) #using MD5 to produce a deterministic hash value.
        self.bitset |= Utils.lowbit(hashed_data)  
        

    def estimate_cardinality(self) -> int:
        num = self.bitset
        estimate = 1
        while num > 0:
            estimate *= 2
            num >>= 1
        return int(estimate / self.phi)
    
#Estimated cardinality: 5422430


# LogLogN space counter
class FlajoletMartinCounterOptimized:
    def __init__(self):
        super().__init__()
        self.max_bit_position = 0
        self.phi = 0.77351

    def add(self, data: str) -> None:
        hashed_data = abs(int(hashlib.md5(data.encode()).hexdigest(), 16))
        self.max_bit_position = max(self.max_bit_position, Utils.lowbit(hashed_data))

    def estimate_cardinality(self) -> int:
        num = self.max_bit_position
        estimate = 1
        count = 0
        while num > 0:
            count += 1
            estimate *= 2
            num >>= 1
        return int(estimate / self.phi)
#Estimated cardinality: 5422430


class Utils:
    # required by FlajoletMartinCounter
    @staticmethod
    def lowbit(x: int) -> int:
        return x & (-x)

    # required by HyperLogLog
    @staticmethod
    def count_trailing_zeros(x: int) -> int:
        if x == 0:
            return 64
        n = 1
        while (x & 1) == 0:
            n += 1
            x >>= 1
        return n


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    hll_counter = HyperLogLog(precision=4)  # You can adjust `precision` as needed

    with open("web-Google.txt", "r") as f:
        for i, line in enumerate(f):
            if line.startswith("#"):
                continue
            data = line.strip().split()
            if len(data) == 2:
                hll_counter.add(data[0])
                hll_counter.add(data[1])
            if i % 100000 == 0:
                logging.info(f'Processed {i} lines')

    print(f'Estimated cardinality: {hll_counter.estimate_cardinality()}')
    #The HyperLogLog algorithm has processed all the input lines (edges of the graph) and 
    # estimated the total number of distinct nodes (both source and target nodes).
