n = int(input())
xau = input()

res = []
for i in range(len(xau)):
    for j in range(i+1,len(xau)+1):
        sub = xau[i:j]
        if xau.count(sub) > 1:
            res.append((sub,xau.count(sub)))

res2 = max(res, key=lambda x:x[1] and len(x[0]))

if res:
    print(len(res2[0]))
else:
    print(0)
