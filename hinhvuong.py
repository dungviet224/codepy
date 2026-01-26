n,m = map(int,input().split())
matrix = []
dp = [[0] * m for _ in range(n)]
max_side = 0
for i in range(n):
    matrix.append(list(map(int,input().split())))
for i in range(n):
    for j in range(m):
        if matrix[i][j] == 0:
            if j == 0 or i == 0:
                dp[i][j] = 1
            else:
                dp[i][j] = min(dp[i-1][j], dp[i][j-1], dp[i-1][j-1]) + 1
            max_side = max(max_side, dp[i][j])
print(max_side*max_side)
