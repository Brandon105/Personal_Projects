arr = [1, 1, 2]

freq = [0] * (max(arr) + 1)

for i in arr:
    freq[i] = i

print(freq)