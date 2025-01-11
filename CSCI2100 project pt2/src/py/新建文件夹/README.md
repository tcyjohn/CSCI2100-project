# External Merge Sort Program

This repository contains a Python program designed to perform an external merge sort on large datasets that cannot fit entirely into memory. The program utilizes a buffer pool and a secondary storage (SecStore) to manage data efficiently.

## Structure

The program consists of two main Python files:

1. `main.py` - The main driver of the program, which initializes the buffer pool, reads input from a file, performs the external merge sort, and writes the sorted output to a file.
2. `toy_memory.py` - A supporting module that simulates the buffer pool and secondary storage, providing the necessary functionality for data management.

## How to Run the Program

### Prerequisites

- Python 3.x
- NumPy and Matplotlib libraries for data handling and plotting (install using `pip install numpy matplotlib` if not already installed)

### Steps

1. **Prepare the Input File**: Ensure you have an input file named `inputs/inputs.txt` in the correct directory. This file should contain double-precision floating-point numbers, one per line.

2. **Run the Program**:
   - Open your terminal or command prompt.
   - Navigate to the directory containing `main.py`.
   - Execute the program by running the command: `python main.py`.

3. **View the Output**: The sorted output will be written to `outputs/test_sorted.txt`. You can view this file to see the sorted results.

### Parameters

The program uses several parameters that can be adjusted within `main.py`:

- `N`: The total number of elements to sort.
- `B`: The buffer pool size in words.
- `b`: The block size in words.
- `T`: The relative time for secondary storage access.
- `input_file` and `output_file`: The paths to the input and output files, respectively.

### Plotting Overhead vs Time

The program also includes functionality to plot the total overhead `H` versus relative time `T`. This plot is generated automatically when the program runs and is saved as `H_vs_T_plot.png`.

## Understanding the Code

- **Buffer Pool**: Managed by `BufferPool` and `BufferPoolManager` classes in `toy_memory.py`, simulating the buffer pool's behavior.
- **Secondary Storage**: Managed by `SecStore` and `SecStoreManager` classes in `toy_memory.py`, simulating read and write operations to disk.
- **External Merge Sort**: Implemented in `external_merge_sort` function in `main.py`, which orchestrates the sorting process using the buffer pool and secondary storage.
