# you can write to stdout for debugging purposes, e.g.
# print("this is a debug message")
"""
 We are given an array A consisting of N  integers. We would like to sort array A into ascending order using a simple algorithm. First, we divide it into one or more slices (a slice is a contiguous subarray). Then we sort each slice. After that, we join the sorted slices in the same order. Write a function 


"""


def solution(A):
    data = A
    result = 1 
    start_pos = 0
    for x in range(len(data) - 1):
        if max(data[start_pos:x+1]) <= min(data[x+1:]):
            result += 1
            start_pos = x
    return result 


