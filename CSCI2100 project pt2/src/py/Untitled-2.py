import math
import sys
import heapq
import os
from toy_memory import BufferPool, BufferPoolManager, SecStore, SecStoreManager
import struct
import random
import matplotlib.pyplot as plt
import numpy as np

def minimum(arr,size):
    mini=10000
    temp=None
    for i in range (size):
        if arr[i]!=None:
            if(arr[i][0]<mini):
                mini=arr[i][0]
                temp=arr[i]
    if temp!=None:
        return temp
    print(arr)

def k_way_merge(sec_man, pool_man, B, N, b, total_num_of_sublist):
    pool = pool_man.buffer_pool.buffer_pool
    block_per_sublist = math.floor(B/((total_num_of_sublist+1)*b))    #number of blocks we will allocate to each sublist
    num_of_sublist = total_num_of_sublist            
    word_per_sublist_in_pool = block_per_sublist * b
    for i in range(num_of_sublist):
        sublist_pos = pool_man.allocate(block_per_sublist)
        sec_man.read('sorted_chunks', i * (B // 2), word_per_sublist_in_pool, sublist_pos)
    heap_pos=block_per_sublist * num_of_sublist*b
    remaining_blocks = B // b - block_per_sublist * num_of_sublist - 1  # Use the remaining part to store partially merged result
    result_start_pos = pool_man.allocate(remaining_blocks) + b
    '''x=[]
    for byte_str in pool[i*b*block_per_sublist:(i+1)*b*block_per_sublist]:
        x.append(struct.unpack('d', byte_str)[0])
        if x!=sorted(x):
            print(x)'''
        
    for i in range(num_of_sublist):  # Initialize min heap(in sec store)
        start_index = i * word_per_sublist_in_pool  # Index of the first number of each chunk
        if start_index < len(pool): 
            pool[heap_pos+i]=(struct.unpack('d', pool[start_index])[0],i,0)
        else:
            print("k-way-merge error: failed to initialize min-heap")
        #self.H+=

    
    index = 0
    x = 0  # Use to trace how many numbers are put into SecStore

    while not all(x is None for x in pool[heap_pos:heap_pos + num_of_sublist]):
        value, sublist_index, element_index = minimum(pool[heap_pos:heap_pos+num_of_sublist],num_of_sublist)
        min_pos=pool[heap_pos:heap_pos+num_of_sublist].index((value, sublist_index, element_index))
        pool[heap_pos+min_pos]=None
        pool[result_start_pos+index]=struct.pack('d', value)
        index += 1
        if index >= remaining_blocks * b:  # If pool is full, write all sorted numbers in pool into SecStore
            '''y=[]
            for byte_str in pool[result_start_pos:]:
                y.append(struct.unpack('d', byte_str)[0])
                if y!=sorted(y) and x==0:
                    print(y)'''
            sec_man.write('output', x, remaining_blocks*b, result_start_pos) 
            pool_man.free(result_start_pos,remaining_blocks)
            x += remaining_blocks * b
            index = 0  # Reset
    
        next_element_index = element_index + 1
        if next_element_index % word_per_sublist_in_pool == 0:
            pool_man.free(sublist_index * word_per_sublist_in_pool, block_per_sublist)  # Free the sublist that all of the elements are in output
            if next_element_index + word_per_sublist_in_pool <= B // 2:  # Check if there are still enough elements in SecStore to read to fill allocated blocks
                #we use fixed blocks for each sublist to better track each sublist
                sec_man.read('sorted_chunks', sublist_index * (B // 2) + next_element_index, word_per_sublist_in_pool, sublist_index * word_per_sublist_in_pool)
            else:
                try:
                    remaining_numbers = B // 2 - next_element_index  #number of remaining numbers of the sublist (in words)
                    sec_man.read('sorted_chunks', sublist_index * (B // 2) + next_element_index, remaining_numbers, sublist_index * word_per_sublist_in_pool)
                except:
                    #print('error here')
                    pass

        if next_element_index < B//2:  # Check if there is a next element in the current sublist
            try:#if there is one, push it into heap
                next_value = struct.unpack('d', pool[sublist_index * word_per_sublist_in_pool + next_element_index % word_per_sublist_in_pool])[0]
                pool[heap_pos+min_pos]=(next_value,sublist_index, next_element_index)
            except Exception as e:
                print(e)
                print(pool[sublist_index*word_per_sublist_in_pool:(sublist_index+1)*word_per_sublist_in_pool])
                print(sublist_index * b * block_per_sublist + next_element_index % word_per_sublist_in_pool)
                print(next_value, sublist_index, next_element_index)

        else:   #the whole sublist is sorted into result, we won't push anything into min-heap
            #print(f"sublist {sublist_index} is all used")
            pass

    #last numbers in buffer pool，write all to output
    sec_man.write('output', x, N - x, result_start_pos) 
    pool_man.free(result_start_pos,remaining_blocks)
    
    '''total_num_of_sublist-=num_of_sublist
    if total_num_of_sublist>0:
        total_num_of_sublist+=1  # +1 for the result from this round of merge
        sec_man.sec_store.symbols['sorted_chunks'][0:x]=sec_man.sec_store.symbols['output'][0:x]
        k_way_merge(sec_man,pool_man,B,N,b,total_num_of_sublist)'''

def merge(arr, temp_start, left, mid, right):
    """
    Perform merge step and write the result back into `arr`.
    `temp_start` is the starting index of the temporary buffer in `arr`.
    """
    # Create references to the left and right subarrays
    arr1 = arr[left:mid+1]
    arr2 = arr[mid+1:right+1]
    i, j = 0, 0
    k = temp_start  # Start writing into the temp area

    # Merge the two subarrays into the temp area
    while i < len(arr1) and j < len(arr2):
        if struct.unpack('d', arr1[i])[0] <= struct.unpack('d', arr2[j])[0]:
            arr[k] = arr1[i]
            i += 1
        else:
            arr[k] = arr2[j]
            j += 1
        k += 1

    # Copy any remaining elements from the left subarray
    while i < len(arr1):
        arr[k] = arr1[i]
        i += 1
        k += 1

    # Copy any remaining elements from the right subarray
    while j < len(arr2):
        arr[k] = arr2[j]
        j += 1
        k += 1

    # Copy the sorted data from the temp area back into the original array
    for i in range(left, right + 1):
        arr[i] = arr[temp_start + (i - left)]

def merge_sort(arr, temp_start, left, right):
    """
    Perform merge sort on `arr` using the temporary buffer starting at `temp_start`.
    """
    if left < right:
        mid = math.floor((left + right) / 2)

        # Sort the left half
        merge_sort(arr, temp_start, left, mid)

        # Sort the right half
        merge_sort(arr, temp_start, mid + 1, right)

        # Merge the two halves
        merge(arr, temp_start, left, mid, right)
        '''x=[]
        for byte_str in arr[left:right+1]:
            x.append(struct.unpack('d', byte_str)[0])
        if x!=sorted(x):
            print('error')'''


                            
def external_merge_sort(B, b, N, T, input_file, output_file):
    """Main function to perform external merge sort."""

    #############################
    # Initialization
    #############################

    # Initialize buffer pool and managers
    buffer_pool = BufferPool(B, b)
    buffer_pool_manager = BufferPoolManager(buffer_pool)
    sec_store = SecStore(N)
    sec_man = SecStoreManager(sec_store, buffer_pool, buffer_pool_manager, b, T)

    # Read input file and store in secStore
    sec_store.read_file(input_file)
    
    #step 1 to 3(split the numbers, merge, write them )
    total_blocks=B//b
    size_per_grp=total_blocks//2  #the size of 1 group of data (in blocks)
    #note that we assumed N is divisble by B//2 here, if not, error will occur
    for i in range (0,N,B//2):   #each time we throw in B/2 numbers to sort
        sec_man.read('input', i, size_per_grp*b, 0)
        merge_sort(buffer_pool.buffer_pool, B//2, 0, B // 2 - 1)
        sec_man.write('sorted_chunks', i, size_per_grp*b, B//2)
        buffer_pool_manager.free(0,B//b)

    #step 4:merging the chunks
    #total of 2N/B chunks of data, each with size B/2
    k_way_merge(sec_man, buffer_pool_manager,B,N,b,2*N//B)

    # Write sorted data to output file
    sorted_data = sec_store.symbols['output']
    #print(sorted_data)
    with open('outputs/sorted.txt', 'w') as f:
        for value in sorted_data:
            f.write(f"{value}\n")
    sec_store.write_file(output_file)

    # Print overhead and statistics
    print(f"Total overhead H: {sec_man.H}")
    return sec_man.H
    

def plot_H_vs_T(H_data, T_values, B, b_values):

    plt.figure(figsize=(10, 6))
    for b in b_values:
        plt.plot(np.log2(T_values), H_data[B][b], label=f'B={B}, b={b}')
    
    plt.yscale('log')  
    
    plt.xlabel('T (in log_2 scale)')
    plt.ylabel('H (in log_10 scale)')
    plt.title(f'Total Overhead H vs Relative Time T for B={B}')
    plt.legend()
    plt.grid(True, which='both', ls='--') 
    plt.savefig('H_vs_T_plot.png')
    plt.show()

# Example usage:
if __name__ == "__main__":
    # Parameters
    B = 10000  # Buffer pool size in words
    b = 200    # Block size in words
    N = 200000  # Number of records
    T = 64     # Relative time taken for secStore access
    # TODO: read from the command line instead of hardcoding
    input_file = "inputs/inputs.txt"
    output_file = "outputs/test_sorted.txt"
    external_merge_sort(B, b, N, T, input_file, output_file)
