
#Bubble Sort
def bubble_sort(arr):
    n = len(arr)
    for i in range(n):
        for j in range(n - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]








reverse_sorted_10 = [10, 9, 8, 7, 6, 5, 4, 3, 2, 1]
almost_sorted_10 = [1, 2, 3, 4, 5, 6, 10, 9, 8, 7]
reverse_sorted_100 = list(range(100, 0, -1))
almost_sorted_100 = list(range(1, 51)) + list(range(100, 50, -1))
reverse_sorted_1000 = list(range(1000, 0, -1))
almost_sorted_1000 = list(range(1, 501)) + list(range(1000, 500, -1))

print(reverse_sorted_10)
bubble_sort(reverse_sorted_10)
print(reverse_sorted_10)