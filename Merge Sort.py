#Merge Sort
def merge_sort(arr):
    def merge(arr, left, mid, right):
        n1 = mid - left + 1
        n2 = right - mid

        L = [0] * n1
        R = [0] * n2

        for i in range(n1):
            L[i] = arr[left + i]
        for j in range(n2):
            R[j] = arr[mid + 1 + j]

        i = j = 0
        k = left

        while i < n1 and j < n2:
            if L[i] <= R[j]:
                arr[k] = L[i]
                i += 1
            else:
                arr[k] = R[j]
                j += 1
            k += 1

        while i < n1:
            arr[k] = L[i]
            i += 1
            k += 1

        while j < n2:
            arr[k] = R[j]
            j += 1
            k += 1

    def merge_sort_helper(arr, left, right):
        if left < right:
            mid = (left + right) // 2
            merge_sort_helper(arr, left, mid)
            merge_sort_helper(arr, mid + 1, right)
            merge(arr, left, mid, right)

    merge_sort_helper(arr, 0, len(arr) - 1)


reverse_sorted_10 = [10, 9, 8, 7, 6, 5, 4, 3, 2, 1]
almost_sorted_10 = [1, 2, 3, 4, 5, 6, 10, 9, 8, 7]
reverse_sorted_100 = list(range(100, 0, -1))
almost_sorted_100 = list(range(1, 51)) + list(range(100, 50, -1))
reverse_sorted_1000 = list(range(1000, 0, -1))
almost_sorted_1000 = list(range(1, 501)) + list(range(1000, 500, -1))
