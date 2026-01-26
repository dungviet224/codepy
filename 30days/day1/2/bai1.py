n = int(input())
nlist = [int(input(i)) for i in range(1,n+1)]
cnt = 0
for i in range(n):
    if nlist[i] % 5 == 0:
        if sum(int(i) for i in str(nlist[i])) % 5 == 0:
            cnt +=1
print(cnt)