def longest_increasing_subsequence(arr):
    if not arr:
        return 0
    
    n = len(arr)
    # Khởi tạo mảng L với tất cả giá trị là 1
    L = [1] * n
    
    # Duyệt từng vị trí i
    for i in range(n):
        # Duyệt các vị trí j đứng trước i
        for j in range(i):
            # Nếu phần tử tại i lớn hơn phần tử tại j
            # Ta có thể nối i vào sau j
            if arr[i] > arr[j]:
                L[i] = max(L[i], L[j] + 1)
                
    # Kết quả là giá trị lớn nhất trong mảng L
    return L

# Test thử
arr = [10, 22, 9, 33, 21, 50, 41, 60]
print(f"Độ dài dãy con tăng dài nhất: {longest_increasing_subsequence(arr)}")