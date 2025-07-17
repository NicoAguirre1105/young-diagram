import time
import math
from multiprocessing import Pool, cpu_count
from run_diagram import run_simulation  # importa tu worker

def main():
    m = int(input("Enter the number of repetitions: "))
    n = int(input("Enter the number of steps: "))
    alpha = float(input("Enter alpha value: "))
    max_len = 5000

    args = [(n, alpha, max_len)] * m  # lista de parámetros por simulación

    start = time.time()

    with Pool(cpu_count()) as pool:
        results = pool.map(run_simulation, args)

    avg = sum(results) / m
    avg /= math.sqrt(n)

    print("Time taken: ", time.time() - start)
    print(f"Average length of the diagram: {avg}")

if __name__ == "__main__":
    main()