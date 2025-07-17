import math
from diagram import Diagram

def run_simulation(args):
    n, alpha, max_len = args
    d = Diagram(max_len)
    l = d.simulate_young_diagram(n, alpha)
    return l