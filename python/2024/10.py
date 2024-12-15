import sys
from time import perf_counter

alternatives={
    (-1,0),
    (0,1),
    (1,0),
    (0,-1)
}

with open('10.input', 'r') as file:
    din = file.read().splitlines()

p1_start = perf_counter()
def dfs(mat, i,j,t, prev=-1):
    #print("dfs", i,j,prev)
    if i<0 or i>=len(mat) or j<0 or j>=len(mat[i]):
        return set()
    v = mat[i][j]
    if v!= prev+1:
        return set()
    if v == t:
        return {(i,j)}
    r = set()
    for a in alternatives:
        r=r.union(dfs(mat,i+a[0], j+a[1], t,v))
    return r

mat = [[int(x) for x in l.strip()] for l in din]
#print(mat)
s = 0
for i in range(len(mat)):
    for j in range(len(mat[i])):
        if mat[i][j]==0:
            #print("call ",i,j)
            r=dfs(mat, i,j,9)
            #print("r",r)
            s+=len(r)

print(f"Part One: {s}")
p1_end = perf_counter()
p1_elapsed = p1_end - p1_start


# part 2
p2_start = perf_counter()
def dfs(mat, i,j,t, prev=-1):
    #print("dfs", i,j,prev)
    if i<0 or i>=len(mat) or j<0 or j>=len(mat[i]):
        return 0
    v = mat[i][j]
    if v!= prev+1:
        return 0
    if v == t:
        return 1
    r = 0
    for a in alternatives:
        r+=dfs(mat,i+a[0], j+a[1], t,v)
    return r

mat = [[int(x) for x in l.strip()] for l in din]
#print(mat)
s = 0
for i in range(len(mat)):
    for j in range(len(mat[i])):
        if mat[i][j]==0:
            #print("call ",i,j)
            r=dfs(mat, i,j,9)
            #print("r",r)
            s+=r

print(f"Part Two: {s}")
p2_end = perf_counter()
p2_elapsed = p2_end - p2_start





print(f"Elapsed Time (Part One): {p1_elapsed:0.2f}s")
print(f"Elapsed Time (Part Two): {p2_elapsed:0.2f}s")