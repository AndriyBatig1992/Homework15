import multiprocessing
from time import time
from typing import Tuple, List, Any


def factorize(*numbers: Tuple[int, ...]) -> List[List[int]]:
    return [[i for i in range(1, number + 1) if number % i == 0] for number in numbers]


def factorize_new(args: Tuple[int, int, int]) -> List[int]:
    start, end, number = args
    return [i for i in range(start, end + 1) if number % i == 0]

def parallel_factorize(*numbers: Tuple[int, ...]) -> List[List[int]]:
    results = []

    with multiprocessing.Pool() as pool:
        for number in numbers:
            num_cores = multiprocessing.cpu_count()
            initial_chunk_size = max(1, number // num_cores)
            chunk_size = initial_chunk_size

            if number < 1000:
                chunk_size = min(chunk_size, 10)
            elif number > 1000000:
                chunk_size = max(chunk_size, 10000)

            start_end_pairs = [(i * chunk_size + 1, (i + 1) * chunk_size if i != num_cores - 1 else number) for i in
                               range(num_cores)]
            factors_lists = pool.map(factorize_new, [(start, end, number) for start, end in start_end_pairs])
            factors = [factor for factors_list in factors_lists for factor in factors_list]
            results.append(factors)

    return results

if __name__ == '__main__':
    start_time1 = time()
    a1, b1, c1, d1 = parallel_factorize(128, 255, 99999, 10651060)
    print(a1)
    print(b1)
    print(c1)
    print(d1)
    end_time1 = time()
    elapsed_time1 = end_time1 - start_time1
    print("Паралельно витрачений час:", elapsed_time1, "секунд")

    start_time = time()
    a, b, c, d = factorize(128, 255, 99999, 10651060)
    print(a)
    print(b)
    print(c)
    print(d)
    end_time = time()
    elapsed_time = end_time - start_time
    print("Синхронно витрачений час:", elapsed_time, "секунд")
