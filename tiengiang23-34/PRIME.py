n = int(input())
nlist = list(map(int, input().split()))
import math
res = 0
ma = 0
def checkisprime(n):
    cnt = 0
    for i in n:
        if i < 2:
            continue
        for j in range(2, int(math.sqrt(i)) + 1):
            if i % j == 0:
                break
        else:
            cnt += 1
       
    return cnt

def tim_uoc(n):
    s = []
    for i in range(1, int(math.sqrt(n)) + 1):
        if n % i == 0:
            s.append(i)
            if i * i != n:
                s.append(n//i)
    s.sort()
    print(s)
    return checkisprime(s)
   

for i in nlist:
    kq = tim_uoc(i)
    if kq > ma:
        ma = kq
        res = i
    
print(res)
