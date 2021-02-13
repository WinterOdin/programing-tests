#given two strings A and B print 1 if A is a subsqc of B and 0 otherwise


string = input()
name   = string.split()
x = len(name[0])
y = len(name[1])

str1 = name[0]
str2 = name[1]

index_x = 0
index_y = 0
while index_x <x and index_y< y:
    if str1[index_x] == str2[index_y]:
        index_x = index_x + 1
    index_y = index_y + 1

if index_x == x:
    print("1")
else:
    print("0")