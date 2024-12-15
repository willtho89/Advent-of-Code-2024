from matrix import Matrix

with open('04.input', 'r') as file:
    din = file.read().splitlines()
ans = 0

M = Matrix((len(din), len(din[0])))

for y in range(len(din)):
    for x in range(len(din[0])):
        M[(y, x)] = din[y][x]

# down, right, up, left, 
DOWN = (0, 1)
UP = (0, -1)
LEFT = (-1, 0)
RIGHT = (1, 0)
LU = (-1, -1)
RU = (1, -1)
LD = (-1, 1)
RD = (1, 1)

dirs = [DOWN, RIGHT, UP, LEFT, RD, LD, RU, LU]

for y in range(len(din)):
    for x in range(len(din[0])):
        for dir in dirs:
            build = ""
            for i in range(4):
                n_char = M[(y+dir[0]*i,x+dir[1]*i)]
                if n_char != None:
                    build += M[(y+dir[0]*i,x+dir[1]*i)]
                else:
                    break
            if build == "XMAS":
                ans += 1

print(ans)

# part 2
ans = 0
for y in range(len(din)):
    for x in range(len(din[0])):
        if "A" == M[x, y]:
            if "M" == M[x+LU[0], y+LU[1]] and "S" == M[(x+RD[0], y+RD[1])]:
                # M . .
                # . A .
                # . .  S
                if "M" == M[x+RU[0], y+RU[1]] and "S" == M[(x+LD[0], y+LD[1])]:
                    # M . M
                    # . A .
                    # S .  S
                    ans += 1
                elif "M" == M[x+LD[0], y+LD[1]] and "S" == M[(x+RU[0], y+RU[1])]:
                    # M . S
                    # . A .
                    # M .  S
                    ans += 1
            elif "M" == M[x+RU[0], y+RU[1]] and "S" == M[(x+LD[0], y+LD[1])]:
                # . . M
                # . A .
                # S . .
                if "M" == M[x+LU[0], y+LU[1]] and "S" == M[(x+RD[0], y+RD[1])]:
                    # M . M
                    # . A .
                    # S . S
                    ans += 1
                elif "M" == M[x+RD[0], y+RD[1]] and "S" == M[(x+LU[0], y+LU[1])]:
                    # S . M
                    # . A .
                    # S . M
                    ans += 1
            elif "M" == M[x+RD[0], y+RD[1]] and "S" == M[(x+LU[0], y+LU[1])]:
                # S . .
                # . A .
                # . . M
                if "M" == M[x+LD[0], y+LD[1]] and "S" == M[(x+RU[0], y+RU[1])]:
                    # S . S
                    # . A .
                    # M . M
                    ans += 1
                elif "M" == M[x+RU[0], y+RU[1]] and "S" == M[(x+LD[0], y+LD[1])]:
                    # S . M
                    # . A .
                    # S . M
                    ans += 1
            elif "M" == M[x+LD[0], y+LD[1]] and "S" == M[(x+RU[0], y+RU[1])]:
                # . . S
                # . A .
                # M . .
                if "M" == M[x+LU[0], y+LU[1]] and "S" == M[(x+RD[0], y+RD[1])]:
                    # M . S
                    # . A .
                    # M . S
                    ans += 1
                elif "M" == M[x+RD[0], y+RD[1]] and "S" == M[(x+LU[0], y+LU[1])]:
                    # S . S
                    # . A .
                    # M . M
                    ans += 1

print(ans)
