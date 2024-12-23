import os
from collections import Counter
from collections import defaultdict

def loadInitialSecrets(filename = 'test.txt'):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    data_file_path = os.path.join(script_dir, filename)

    with open(data_file_path) as f:
        lines = f.readlines()
    return [ int(i.strip()) for i in lines]


# - To mix a value into the secret number, calculate the bitwise XOR of
#   the given value and the secret number. Then, the secret number becomes
#   the result of that operation.
def mixSecrets(seed, value):
    return seed ^ value

#   To prune the secret number, calculate the value of the secret number
#   modulo 16777216. Then, the secret number becomes the result of that
#   operation.
def pruneSecret(secret):
    return secret % 16777216

def evolveSecret(seed, times):
    lastDigit = secretNumber = seed
    seqPrice = {}
    lastFourDiffs = []
    for i in range(times):
        # - Calculate the result of multiplying the secret number by 64.
        #   Then, mix this result into the secret number.
        #   Finally, prune the secret number.
        secretNumber = pruneSecret(mixSecrets(secretNumber, secretNumber * 64))

        # - Calculate the result of dividing the secret number by 32. Round the
        #   result down to the nearest integer.
        #   Then, mix this result into the secret number. Finally, prune the secret number.
        secretNumber = pruneSecret(mixSecrets(secretNumber, secretNumber // 32))

        # - Calculate the result of multiplying the secret number by 2048. Then,
        #   mix this result into the secret number. Finally, prune the secret
        #   number.
        secretNumber = pruneSecret(mixSecrets(secretNumber, secretNumber * 2048))

        #   Save the juicy bits
        secretDigit = secretNumber % 10
        lastFourDiffs.append(secretDigit - lastDigit)
        if len(lastFourDiffs) > 4:
            lastFourDiffs.pop(0)
            l4 = tuple(lastFourDiffs)
            if l4 not in seqPrice:  # only save the first time we see this sequence
                seqPrice[l4] = secretNumber%10
        lastDigit = secretDigit
    return secretNumber, seqPrice

secretseeds = loadInitialSecrets('input.txt')

#evolveSecret(123, 10)
total  = 0
highBananas = defaultdict(int)
for seed in secretseeds:
    secretNumber, seqPrice = evolveSecret(seed, 2000)
    total += secretNumber
    for k, v in seqPrice.items():
        highBananas[k] += v

print(f"Part 1: {total}")

maxBananas = max(highBananas.values())
print(f"Part 2: max bananas {maxBananas}")

# Part 1: 14392541715
# Part 2: max bananas 1628