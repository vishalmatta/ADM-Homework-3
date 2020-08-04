import numpy as np

string = input()
l = len(string)

# creating a matrix(d,d) of 1
M = np.ones((l, l))

# main diagonal has already been filled with 1

for sublen in range(2, l+1):    # lenght of substring that i want to analyze
    for i in range(l-sublen+1): # number of substrings of that lenght and first element of the substring
        j = i + (sublen - 1)    # last element of the substring
        if string[i] == string[j]:
            M[i][j] = M[i+1][j-1] + 2
        else:
            M[i][j] = max(M[i][j-1], M[i+1][j])

result = np.amax(M)
print(result)