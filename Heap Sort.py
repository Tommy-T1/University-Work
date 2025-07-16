#Heap Sort
def heap_sort(arr):
    def heapify(arr, n, i):
        largest = i
        left = 2 * i + 1
        right = 2 * i + 2
        
        if left < n and arr[i] < arr[left]:
            largest = left
        if right < n and arr[largest] < arr[right]:
            largest = right
        
        if largest != i:
            arr[i], arr[largest] = arr[largest], arr[i]
            heapify(arr, n, largest)
    
    n = len(arr)
    for i in range(n // 2 - 1, -1, -1):
        heapify(arr, n, i)
    
    for i in range(n - 1, 0, -1):
        arr[i], arr[0] = arr[0], arr[i]
        heapify(arr, i, 0)

reverse_sorted_10 = [10, 9, 8, 7, 6, 5, 4, 3, 2, 1]
almost_sorted_10 = [1, 2, 3, 4, 5, 6, 10, 9, 8, 7]
reverse_sorted_100 = list(range(100, 0, -1))
almost_sorted_100 = list(range(1, 51)) + list(range(100, 50, -1))
reverse_sorted_1000 = list(range(1000, 0, -1))
almost_sorted_1000 = list(range(1, 501)) + list(range(1000, 500, -1))
