A,B,S = map(int,input().split())
cnt = 0


for i in range(A  , B+1):
    if sum(int(d) for d in str(i)):
        print(i)