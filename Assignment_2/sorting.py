a = [1, 2, 3]

for i in range(0, len(a)):
    for j in range(i, len(a)):
        if (a[j] > a[i]):
            # print('i:', i, ' j:', j, ' a[i]:', a[i], ' a[j]:', a[j])
            t1, t2 = a[j], a[i]
            a[i] = t1
            a[j] = t2
            print(a)

print(a)

a = [0 for i in range(3)];
print(a)
