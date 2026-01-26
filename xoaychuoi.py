a = input()
cdau = sorted(a)
res = ''

for i in range(len(a)):
    if a[0] == cdau[0]:
        break
    else:
        a = a[1:] + a[0]
print(a)