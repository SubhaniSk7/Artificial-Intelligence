import random

n = int(input('enter n:'));

a = [[0] * n for i in range(n)];

for i in range(0, n):
    for j in range(0,n):
        a[i][j]=random.randint(1, 4);


for i in range(0,n):
    print(a[i]);
