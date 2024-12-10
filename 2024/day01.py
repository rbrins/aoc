#!/bin/python3

# Step 1 - get puzzle input read
puzzleFile = "day01.txt"
with open(puzzleFile, "r") as input:
    puzzleInput = input.readlines()

#puzzleInput_sanitized = puzzleInput.strip('\n')
#print(puzzleInput)

# Step 2 - parse / format puzzle input
left = []
right = []

for row in puzzleInput:
    item = row.strip('\n').split("  ")
    left.append(int(item[0]))
    right.append(int(item[1]))

left.sort()
right.sort()


# Step 3 - do the math
values = []
for i in range(len(left)):
   value = abs(left[i] - right[i])
   values.append(value)

result1 = sum(values)
print(result1)

# Part 2
# Step 4 - similar items in lists
similarity_score = 0
for i in range(len(left)):
    similarity_score+=(left[i] * right.count(left[i]))

print(similarity_score)
