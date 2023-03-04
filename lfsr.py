class LFSR:
    taps = {
        5 : (5, 4, 3, 2),
        6 : (6, 5, 3, 2),
        7 : (7, 6, 5, 4),
        8 : (8, 6, 5, 4),
        9 : (9, 8, 6, 5),
        10: (10, 9, 7, 6),
        11: (11, 10, 9, 7),
        12: (12, 11, 8, 6),
        13: (13, 12, 10, 9),
        14: (14, 13, 11, 9),
        15: (15, 14, 13, 11),
        16: (16, 14, 13, 11),
        17: (17, 16, 15, 14),
        18: (18, 17, 16, 13),
        19: (19, 18, 17, 14),
        20: (20, 19, 16, 14),
        21: (21, 20, 19, 16),
        22: (22, 19, 18, 17),
        23: (23, 22, 20, 18),
        24: (24, 23, 21, 20),
        25: (25, 24, 23, 22),
        26: (26, 25, 24, 20),
        27: (27, 26, 25, 22),
        28: (28, 27, 24, 22),
        29: (29, 28, 27, 25),
        30: (30, 29, 26, 24),
        31: (31, 30, 29, 28),
        32: (32, 30, 26, 25),
        33: (33, 32, 29, 27),
        34: (34, 31, 30, 26),
        35: (35, 34, 28, 27),
        36: (36, 35, 29, 28),
        37: (37, 36, 33, 31),
        38: (38, 37, 33, 32),
        39: (39, 38, 35, 32),
        40: (40, 37, 36, 35),
        41: (41, 40, 39, 38),
        42: (42, 40, 37, 35),
        43: (43, 42, 38, 37),
        44: (44, 42, 39, 38),
        45: (45, 44, 42, 41),
        46: (46, 40, 39, 38),
        47: (47, 46, 43, 42),
        48: (48, 44, 41, 39),
        49: (49, 45, 44, 43),
        50: (50, 48, 47, 46),
        51: (51, 50, 48, 45),
        52: (52, 51, 49, 46),
        53: (53, 52, 51, 47),
        54: (54, 51, 48, 46),
        55: (55, 54, 53, 49),
        56: (56, 54, 52, 49),
        57: (57, 55, 54, 52),
        58: (58, 57, 53, 52),
        59: (59, 57, 55, 52),
        60: (60, 58, 56, 55),
        61: (61, 60, 59, 56),
        62: (62, 59, 57, 56),
        63: (63, 62, 59, 58),
        64: (64, 63, 61, 60)
        }

    def __init__(self, register_size=32, stop=False, seed=8):
        assert seed != 0, "seed cannot be 0"
        assert register_size > 4, "LFSR uses 4-taps, bitsize must be larger than 4"
        assert register_size < 64, "only supports registers up to 64 bits"
        
        self.register_size = register_size
        self.max_period = 2**self.register_size

        # Mask seed up to bitsize of register - 1
        # ensure that the last bit is 1 for reasons
        self.register = (seed & self.register_size-2) | 1
        
        self.stop = stop
        self.n_generated = 0

    def _step(self):
        newbit = (
            self.register 
            ^ (self.register >> LFSR.taps[self.register_size][0])
            ^ (self.register >> LFSR.taps[self.register_size][1])
            ^ (self.register >> LFSR.taps[self.register_size][2])
            ^ (self.register >> LFSR.taps[self.register_size][3])
            ) & 1
        self.register = (self.register >> 1) | (newbit << self.register_size-1)
    
    def __iter__(self):
        return self

    def __next__(self):
        if self.stop and (self.n_generated >= self.max_period):
            raise StopIteration

        self._step()
        self.n_generated +=1
        return self.register
    
    def gen(self):
        return next(self)

    @staticmethod
    def get_period_size(bits):
        return 2**bits


if __name__ == "__main__":

    # Validate period size
    print("Testing Period Size...")
    assert LFSR.get_period_size(6) == 64, "get_period_size failed"

    # Validate Periodicity
    print("Testing Periodicity...")
    lfsr6 = LFSR(register_size=6)
    generated = []
    for i in range(100):
        n = next(lfsr6)
        if n in generated:
            assert i == 64-1, "period is incorrect"
            break
    
    # Validate Deterministic
    print("Testing Determinism...")
    lfsr6_a = LFSR(register_size=6, seed=10)
    lfsr6_b = LFSR(register_size=6, seed=10)
    lfsr6_c = LFSR(register_size=6, seed=12)
    gen_a = [next(lfsr6_a) for _ in range(100)]
    gen_b = [next(lfsr6_b) for _ in range(100)]
    gen_c = [next(lfsr6_c) for _ in range(100)]

    assert gen_a == gen_b, "not deterministic"
    assert gen_a != gen_c, "seed not setting different state"

    # gen vs next
    print("Testing Generation...")
    lfsr6_gen = LFSR(register_size=6, seed=15)
    lfsr6_next = LFSR(register_size=6, seed=15)
    assert lfsr6_gen.gen() == next(lfsr6_next), "generation functions are wrong"

    # Test Stop
    print("Testing stop...")
    lfsr6_stop = LFSR(register_size=6, stop=True)

    for i in range(50):
        try:
            next(lfsr6_stop)
        except StopIteration:
            assert i == 64, "Generator not stopping at end of period"