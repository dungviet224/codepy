n = int(input())
nlist = list(map(int, input().split()))
cnt = 0
sun = 0
a = []
for i in range(n):
    for j in range(i - 1, -1, -1):
        if nlist[i] == nlist[j]:
            a.append((nlist[j:i+1]))
            break
for i in range(len(a)):
    if  a[i-1][len(a[i-1])-1] == a[i][0]:
        new_element = a[i-1] + a[i][1:]
        print(new_element)
        a.append(new_element)
for i in a:
    if len(i) > cnt:
        cnt = len(i)
        sun = sum(i)
    elif len(i) == cnt:
        if sum(i) >= sun:
            cnt = len(i)    
            sun = sum(i)
print(cnt,sun)