# Parallel-Merge-Sort-Linux-WSL-
Implemented and benchmarked parallel Merge Sort on Linux to analyze real multi-core performance and scalability.

# Overview

This project implements and analyzes a parallel version of Merge Sort to demonstrate how multi-core processors can be used to improve performance for large datasets. Merge sort naturally follows a divide-and-conquer strategy, making it well-suited for parallel execution.

The project focuses on practical performance analysis rather than theoretical speedup, highlighting how operating system behavior and process management affect real-world parallel execution.

# Approach

The algorithm works as follows:

The input array is recursively divided into two halves.

At each recursion level, the left and right subarrays are sorted in parallel using separate processes.

A threshold-based optimization is applied so that small subarrays are sorted serially, avoiding excessive process creation.

Once both halves are sorted, they are merged to produce the final sorted output.

This recursive parallel strategy allows the algorithm to efficiently scale with the number of available CPU cores.

# Implementation Details

Language: Python

Parallelism: multiprocessing with fork-based execution (Linux/WSL)

Optimization: Threshold-based fallback to serial merge sort

Environment: Linux (WSL) to enable true multi-core execution

Performance Evaluation

The implementation was benchmarked on large datasets (up to hundreds of thousands of elements) while varying the number of CPU cores. Results show a clear reduction in execution time as the number of cores increases, demonstrating effective parallel scalability.

Execution-time data is collected and visualized using plots, and results are exported in CSV format for further analysis.

# Key Learnings

Parallel algorithms must be designed with OS-level behavior in mind.

Windows and Linux handle multiprocessing very differently, impacting scalability.

Process creation overhead can negate parallel benefits if not carefully managed.

Threshold-based optimizations are essential for efficient parallel recursion.

# Conclusion

This project demonstrates how parallel merge sort can significantly improve sorting performance on multi-core systems when implemented and executed in an appropriate environment. It provides hands-on insight into parallel computing, process management, and performance optimization on real hardware.
