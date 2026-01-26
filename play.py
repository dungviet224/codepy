import sys
from collections import deque

def solve():
    # Đọc dữ liệu từ file (giả lập môi trường nộp bài)
    # Nếu chạy trên máy local không có file, bạn có thể comment dòng này
    # và nhập tay.
    try:
        sys.stdin = open('PLAY.INP', 'r')
        sys.stdout = open('PLAY.OUT', 'w')
    except FileNotFoundError:
        pass

    # Đọc N và K
    input_data = sys.stdin.read().split()
    if not input_data:
        return

    iterator = iter(input_data)
    try:
        n = int(next(iterator))
        k = int(next(iterator))
        a = [0] + [int(next(iterator)) for _ in range(n)] # Thêm 0 vào đầu để index từ 1
    except StopIteration:
        return

    # DP array: dp[i] là tổng tiền lớn nhất khi dừng tại hộp i
    # Trace array: trace[i] lưu vị trí trước đó nhảy tới i để truy vết
    dp = [-float('inf')] * (n + 1)
    trace = [0] * (n + 1)
    
    dp[0] = 0 # Vị trí xuất phát
    
    # Deque lưu trữ index các vị trí tiềm năng: j
    # Luôn duy trì tính chất: dp[dq[0]] >= dp[dq[1]] ... (giảm dần)
    dq = deque([0]) 

    for i in range(1, n + 1):
        # 1. Loại bỏ các index quá xa (ngoài phạm vi K bước nhảy)
        while dq and dq[0] < i - k:
            dq.popleft()
        
        # 2. Tính DP[i] dựa trên max DP trước đó (nằm tại dq[0])
        best_prev = dq[0]
        dp[i] = dp[best_prev] + a[i]
        trace[i] = best_prev
        
        # 3. Duy trì tính chất đơn điệu giảm của Deque khi thêm i vào
        # Nếu dp[i] lớn hơn dp của các phần tử cuối deque, các phần tử đó trở nên vô dụng
        while dq and dp[dq[-1]] <= dp[i]:
            dq.pop()
        dq.append(i)

    # Tìm kết quả lớn nhất
    # Bài toán cho phép dừng bất cứ lúc nào, nên ta tìm max trong toàn bộ mảng dp[1..N]
    max_money = -float('inf')
    end_pos = -1

    for i in range(1, n + 1):
        if dp[i] > max_money:
            max_money = dp[i]
            end_pos = i
            
    # In kết quả dòng 1
    print(max_money)
    
    # Truy vết đường đi dòng 2
    path = []
    curr = end_pos
    while curr != 0:
        path.append(curr)
        curr = trace[curr]
    
    # In ra đường đi theo thứ tự xuôi (từ trái sang phải)
    print(*(path[::-1]))

if __name__ == '__main__':
    solve()