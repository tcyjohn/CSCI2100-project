def selection_sort(S: list):
    n = len(S)
    for i in range(n):
        # 假设当前索引 i 是最大值的索引
        max_index = 0
        # 在未排序的部分寻找最大值
        for j in range(1, n - i):
            if S[j] > S[max_index]:
                max_index = j
        # 将当前最大值放到未排序部分的最后
        S[i], S[max_index] = S[max_index], S[i]
    return S

numbers = [5, 2, 9, 1, 5, 6]
sorted_numbers = selection_sort(numbers)
print(sorted_numbers)  # 输出: [1, 2, 5, 5, 6, 9]