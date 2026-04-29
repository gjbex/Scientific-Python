# 2. Checking a matrix product by hand

## Example solution

Pick two small matrices with known entries.

```python
A = [[1, 2],
     [3, 4]]

B = [[5, 6],
     [7, 8]]

C = [[0, 0],
     [0, 0]]

for i in range(2):
    for j in range(2):
        for k in range(2):
            C[i][j] += A[i][k] * B[k][j]

print(C)
```

The hand calculation gives

```text
C[0,0] = 1*5 + 2*7 = 19
C[0,1] = 1*6 + 2*8 = 22
C[1,0] = 3*5 + 4*7 = 43
C[1,1] = 3*6 + 4*8 = 50
```

so the expected result is `[[19, 22], [43, 50]]`.
