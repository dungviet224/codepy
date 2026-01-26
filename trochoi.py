t = int(input())
debai = []

for i in range(t):
    n, k = map(int, input().split())
    debai.append((n, k))

def timnguoi(n,k):
    if n == 1:
        return
    