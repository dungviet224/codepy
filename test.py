n = int(input())
a = list(map(int, input().split()))
b = list(map(int, input().split()))
dp = [0] * (n+1)

r = [0] * (n+1)
t = [0] * (n+1)
for i in range(1, n+1):
    t[i] = a[i-1]

for i in range(2,n+1):
    r[i] = b[i-2]
dp[1] = t[1]
for i in range(n):
    o1 = dp[i-1] + t[i]
    o2 = dp[i-2] + r[i]
    dp[i] = min(o1, o2)

print(dp)