import random
cimport cython
from libc.math cimport sqrt, pow

@cython.boundscheck(False)
@cython.wraparound(False)
def get_S(int x, int y, double alpha):
    cdef int perimeter = (x + y + 2) * 2
    return pow(perimeter, alpha)

@cython.boundscheck(False)
@cython.wraparound(False)
cdef int select_move_mv(int[:] possible_moves, double[:] weights, int length):
    cdef double total = 0.0
    cdef int i
    for i in range(length):
        total += weights[i]

    cdef double r = random.uniform(0, total)
    cdef double upto = 0.0
    for i in range(length):
        upto += weights[i]
        if upto >= r:
            return possible_moves[i]
    return possible_moves[length - 1]  # fallback (should not happen in theory)

cdef class Diagram:
    cdef int[:] columns
    cdef int[:] moves_col
    cdef double[:] moves_weight
    cdef int len
    cdef int max_len

    def __cinit__(self, int max_len):
        self.columns = cython.view.array(shape=(max_len,), itemsize=cython.sizeof(cython.int), format="i")
        self.columns[0] = 1
        self.len = 1
        self.max_len = max_len
        self.moves_col = cython.view.array(shape=(max_len,), itemsize=cython.sizeof(cython.int), format="i")
        self.moves_weight = cython.view.array(shape=(max_len,), itemsize=cython.sizeof(cython.double), format="d")

    cpdef int simulate_young_diagram(self, int n, double alpha):
        cdef int x, i, poss_len
        for i in range(n):
            poss_len = 0
            for x in range(self.len):
                if x == 0 or self.columns[x-1] > self.columns[x]:
                    self.moves_col[poss_len] = x
                    self.moves_weight[poss_len] = get_S(x, self.columns[x], alpha)
                    poss_len += 1
            x = self.len
            self.moves_col[poss_len] = x
            self.moves_weight[poss_len] = get_S(x, 0, alpha)
            poss_len += 1

            x = select_move_mv(self.moves_col, self.moves_weight, poss_len)

            if x >= self.max_len:
                break
            if x == self.len:
                self.len += 1
            self.columns[x] += 1
        return self.len