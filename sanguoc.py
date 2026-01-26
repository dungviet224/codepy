
s,t = map(int,input().split())
req = 10000

listtt = [0] *(req+1)
res = []
for i in range(1,req+1):
    for j in range(i,req+1,i):
        listtt[j] += i


for i in range(s,t+1):
    if listtt[i] > i*2:
        res.append(listtt[i])
print(len((res)))
