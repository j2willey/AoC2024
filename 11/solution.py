
testinput = "125 17"

input = "2 77706 5847 9258441 0 741 883933 12"

memo = {}

def transformMemo(istone, iterations):
    if (istone, iterations) in memo:
        return memo[(istone, iterations)]
    if iterations == 0:
        return 1
    if istone == 0:
        memo[(0, iterations)] = transformMemo(1, iterations-1)
        return memo[(0, iterations)]
    stone = str(istone)
    ilen = len(stone)
    if ilen %2 == 0:
        memo[istone, iterations] = transformMemo(int(stone[:ilen//2]), iterations-1) \
            + transformMemo(int(stone[ilen//2:]), iterations-1)
        return memo[istone, iterations]
    memo[(istone, iterations)] = transformMemo(istone * 2024, iterations-1)
    return memo[(istone, iterations)]

stones = 0
for istone in [int(stone) for stone in testinput.split()]:
    stones += transformMemo(istone, 6)
# of Stones:  22
print("Test # of Stones: ",  stones)

print(memo)

for istone in [int(stone) for stone in input.split()]:
    stones += transformMemo(istone, 25)
# of Stones:  190865
print("# of Stones: ",  stones)

stones = 0
for istone in [int(stone) for stone in input.split()]:
    stones += transformMemo(istone, 75)
print("Part 2 # of Stones: ",  stones)
