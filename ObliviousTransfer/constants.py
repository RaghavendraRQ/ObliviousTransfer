Z = 5
T = 2
C = 3
L = 4
N = 20
SEC_PARAM = 5

class Config:
    TEMPORAL_LOCALITY_WINDOW = 3

    def __init__(self, L, t, Z, temp_window=3):
        self.L = L
        self.t = t
        self.Z = Z
        self.TEMPORAL_LOCALITY_WINDOW = temp_window