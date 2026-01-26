n = int(input())
nlist = list(map(int,input().split()))
curr = nlist[0]
maxxx = nlist[0]
for i in range(1,n):
    temp = max(curr + nlist[i], nlist[i]  )
    curr = temp
    maxxx = max(maxxx,curr)
print(maxxx)