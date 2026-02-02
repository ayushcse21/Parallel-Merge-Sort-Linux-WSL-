import multiprocessing as mp
import random
import time
import math
import sys

# --- Utility functions (top-level so they are picklable) ---
def merge(left, right):
    result = []
    i = j = 0
    while i < len(left) and j < len(right):
        if left[i] < right[j]:
            result.append(left[i]); i += 1
        else:
            result.append(right[j]); j += 1
    if i < len(left):
        result.extend(left[i:])
    if j < len(right):
        result.extend(right[j:])
    return result

def merge_sort_serial(arr):
    if len(arr) <= 1:
        return arr
    mid = len(arr) // 2
    left = merge_sort_serial(arr[:mid])
    right = merge_sort_serial(arr[mid:])
    return merge(left, right)

# Wrapper target for Process: must be top-level for pickling
def parallel_sort_process(arr, depth, max_depth, conn, threshold):
    try:
        sorted_arr = parallel_merge_sort(arr, depth, max_depth, threshold)
        conn.send(sorted_arr)
    except Exception as e:
        conn.send(('__EXCEPTION__', str(e)))
    finally:
        try:
            conn.close()
        except Exception:
            pass

def parallel_merge_sort(arr, depth, max_depth, threshold):
    if len(arr) <= 1:
        return arr
    if depth >= max_depth or len(arr) <= threshold:
        return merge_sort_serial(arr)

    mid = len(arr) // 2
    left = arr[:mid]
    right = arr[mid:]

    parent_l, child_l = mp.Pipe(duplex=False)
    parent_r, child_r = mp.Pipe(duplex=False)

    p1 = mp.Process(target=parallel_sort_process, args=(left, depth+1, max_depth, child_l, threshold))
    p2 = mp.Process(target=parallel_sort_process, args=(right, depth+1, max_depth, child_r, threshold))

    p1.start()
    p2.start()

    left_sorted = parent_l.recv()
    right_sorted = parent_r.recv()

    p1.join()
    p2.join()

    if isinstance(left_sorted, tuple) and left_sorted[0] == '__EXCEPTION__':
        raise RuntimeError(f'Child exception (left): {left_sorted[1]}')
    if isinstance(right_sorted, tuple) and right_sorted[0] == '__EXCEPTION__':
        raise RuntimeError(f'Child exception (right): {right_sorted[1]}')

    return merge(left_sorted, right_sorted)

# --- Benchmarking harness ---
def cores_to_depth(cores):
    if cores < 1:
        return 0
    return int(math.floor(math.log2(cores)))

def run_benchmarks(dataset_sizes, core_targets, threshold=50000, runs=1):
    results = {}
    for size in dataset_sizes:
        print(f"\n=== Dataset = {size} ===")
        data_master = [random.randint(0, 10**6) for _ in range(size)]
        results[size] = {}
        for cores in core_targets:
            depths = cores_to_depth(cores)
            times = []
            for r in range(runs):
                data = list(data_master)
                start = time.time()
                sorted_arr = parallel_merge_sort(data, 0, depths, threshold)
                elapsed = time.time() - start
                times.append(elapsed)
            avg_time = sum(times) / len(times)
            results[size][cores] = avg_time
            print(f"Cores: {cores:2d}  (depth={depths}) -> {avg_time:.3f} sec over {runs} run(s)")
    return results

def print_results_table(results):
    print("\n--- Summary ---")
    dataset_sizes = sorted(results.keys())
    core_targets = sorted(next(iter(results.values())).keys())
    header = "Size\Cores\t" + "\t".join(str(c) for c in core_targets)
    print(header)
    for size in dataset_sizes:
        row = [f"{size}"]
        for c in core_targets:
            row.append(f"{results[size][c]:.3f}")
        print("\t".join(row))

if __name__ == "__main__":
    try:
        if sys.platform != "win32":
            mp.set_start_method('fork')
    except RuntimeError:
        pass

    dataset_sizes = [100000, 250000, 500000, 1000000]
    core_targets = [2, 4, 6, 8]
    threshold = 50000
    runs = 1

    print("Machine reported CPU count:", mp.cpu_count())
    print("Running fully recursive parallel merge-sort (paper-like).")
    print("IMPORTANT: For results matching the paper, run on Linux (native) or WSL with enough cores.\n")

    results = run_benchmarks(dataset_sizes, core_targets, threshold=threshold, runs=runs)
    print_results_table(results)