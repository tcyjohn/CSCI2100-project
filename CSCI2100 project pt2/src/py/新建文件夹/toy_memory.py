import math
import sys
import heapq
import os
import struct

class BufferPool:

    def __init__(self, B, b):
        # TODO: Implement buffer pool
        self.B = B  # Buffer pool size in words
        self.b = b  # Block size in words
        # TODO: Implement buffer pool
        # Simulate buffer pool with a list
        # Block availability
        self.num_of_blocks=B//b
        self.buffer_pool = [None]*B    #use 1D list
    
    def free_and_used_blocks(self):
        free_cnt = 0
        used_cnt = 0
        for word in self.buffer_pool:
            if word==None:
                free_cnt += 1
            else:
                used_cnt += 1
        return free_cnt,used_cnt

        
class BufferPoolManager:
    # TODO: Implement buffer pool manager
    def __init__(self, buffer_pool):
        self.buffer_pool = buffer_pool
        

    def allocate(self, num_blocks):
        num_of_free_blocks = self.buffer_pool.free_and_used_blocks()[0]
        if num_blocks > num_of_free_blocks:
            print("allocation failed: not enough blocks")
            return -1
        else:
            # Finding consecutive free blocks for allocation
            start_index = -1
            current_free_count = 0
            for i in range(self.buffer_pool.B):
                if self.buffer_pool.buffer_pool[i]==None:
                    current_free_count += 1
                    if current_free_count == num_blocks * self.buffer_pool.b:
                        start_index = i - num_blocks * self.buffer_pool.b + 1
                        break
                else:
                    current_free_count = 0

            if start_index == -1:
                print("allocation failed: not enough blocks!")
                return -1  # Not enough continuous free blocks

        return start_index  # Return starting address in words
    
    '''def allocate_in_word(self, size):
        num_of_free_blocks = self.buffer_pool.free_and_used_blocks()[0]
        if size > num_of_free_blocks* self.buffer_pool.b:
            print("allocation failed: not enough blocks")
            return -1
        else:
            # Finding consecutive free position for allocation
            start_index = -1
            current_free_count = 0
            for i in range(self.buffer_pool.B):
                if self.buffer_pool.buffer_pool[i]==None:
                    current_free_count += 1
                    if current_free_count == size:
                        start_index = i - size + 1
                        break
                else:
                    current_free_count = 0

            if start_index == -1:
                print("allocation failed: not enough blocks!")
                return -1  # Not enough continuous free blocks

        return start_index  # Return starting address in words'''

    def free(self, start_index, num_blocks):
        # Free space in the buffer pool
        for i in range(start_index, start_index + num_blocks * self.buffer_pool.b):
            self.buffer_pool.buffer_pool[i] = None
        
    '''def free_in_word(self, start_index, size):
        # Free space in the buffer pool
        for i in range(start_index, start_index + size):
            self.buffer_pool.buffer_pool[i] = None'''


class SecStore:
    """
    read files from disk and write files to disk
    """

    def __init__(self,N):
        self.N=N
        self.symbols = {'sorted_chunks':[10000]*self.N,'output':[10000]*self.N} #10000 is used as place holder only


    def read_file(self, file_name):
        """
        SecStore is used for the input file inputs.txt, a text file containing
        double-precision floating point numbers to be sorted. 
        """
        try:
            with open(file_name, 'r') as file:
                binary_numbers = []
                for line in file:
                    line = line.strip()  
                    if line:  
                        try:
                            num = float(line)
                            binary_numbers.append(struct.pack('d', num)) 
                        except ValueError:
                            print(f"Cannot convert line to float: '{line}'")
                self.symbols['input'] = binary_numbers
        except FileNotFoundError:
            print(f"File not found: {file_name}!")
        except Exception as e:
            print(f"An error occurred: {e}!")

    #write data from SecStore to file
    def write_file(self, file_name):
        """
        The store is also used for the output file sorted.txt that you output
        (in CSV format). 
        """
        binary_numbers = self.symbols['output']
        with open(file_name, 'w') as file:
            for i, binary_number in enumerate(binary_numbers):
                float_number = struct.unpack('d', binary_number)[0]
                file.write(str(float_number))
                if i < len(binary_numbers) - 1:
                    file.write('\n')



class SecStoreManager:

    def __init__(self, sec_store, buffer_pool, buffer_pool_manager, b, T):
        self.sec_store = sec_store
        self.buffer_pool = buffer_pool
        self.buffer_pool_manager = buffer_pool_manager
        self.b = b
        self.T = T
        self.H = 0  # Total overhead

    #read data in SecStore to buffer pool
    def read(self, name, start, size, buf_address):
        # start is the starting address of data in Secstore
        # buf_address is the starting address of the position in buffer pool
        # where the data will be placed  
        # size is in words, but start and buf_address is in words
        if name not in self.sec_store.symbols.keys():
            print("file/array not found")
            return -1
        if size//self.b> self.buffer_pool.free_and_used_blocks()[0]:
            print("file size too large to fit in buffer pool")
            return -1
        if buf_address < 0 or buf_address + size > self.buffer_pool.B:
            print("buf_address is out of bound")
            return -1

        for i in range(size):
            self.buffer_pool.buffer_pool[buf_address + i] = self.sec_store.symbols[name][start + i]
        self.H += math.ceil(size*self.T/self.b)

    # write data from buffer pool to secstore
    def write(self, name, start, size, buf_address):
        
        if name not in self.sec_store.symbols.keys():
            print("file/array not found")
            return -1
        if size//self.b>self.buffer_pool.free_and_used_blocks()[1]:
            print ("file size too large")
            return -1
        if buf_address<0 or buf_address>self.buffer_pool.B:  # check if buf_address is out of bound
            print("buf_address is out of bound!")
            return -1

        #copying data from buffer pool to secstore one by one
        for i in range(size):
            self.sec_store.symbols[name][start + i] = self.buffer_pool.buffer_pool[buf_address + i]

        self.H+=math.ceil(size*self.T/self.b)
