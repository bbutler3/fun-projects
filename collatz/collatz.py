import numpy as np

maxiterfile = 'collatz_itermax'

start = 2e6
end = 3e6

start = int(start)
end = int(end)

def collatz(n):
    if (n % 2) == 0:
        return n/2
    else:
        return 3*n + 1

#f = open(filename, 'w')

itercounts = []

for j in range(start,end+1):
    flag = False
    n = j
    for i in range(600):
        n = collatz(n)
        if n==1:
            itercounts.append(i+1)
            flag = True
            break
    if not flag:
        print(j,'failed!')
        
maxiter_new = max(itercounts)
print(maxiter_new)

f = open(maxiterfile,'r+')
maxiter_prev = int(f.readline())
if maxiter_new > maxiter_prev:
    f.seek(0)
    f.truncate()
    f.write(str(maxiter_new))
f.close()
