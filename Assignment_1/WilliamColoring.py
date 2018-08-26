import random
import copy
# from coloring_gui import draw


def return_second(elem):
    return elem[2]


def print_data(data):
    for k in data:
        print(k)


def check(data):
    for m in range(len(data)):
        for n in range(len(data) - 1):
            if data[m][n] == data[m][n + 1]:
                return (m, n)
            if data[n][m] == data[n + 1][m]:
                return (n, m)
    return 1


def count_collisions(array):
    return len(get_collissions(array))


def get_collissions(array):
    collissions = []

    for m in range(len(array) - 1):
        for n in range(len(array)):
            if (array[m][n] == array[m + 1][n]):
                if (m, n) not in collissions:
                    collissions.append((m, n))
                if (m + 1, n) not in collissions:
                    collissions.append((m + 1, n))
            if (array[n][m] == array[n][m + 1]):
                if (n, m) not in collissions:
                    collissions.append((n, m))
                if (n, m + 1) not in collissions:
                    collissions.append((n, m + 1))
    # print("Collisions: " + str(collissions))
    return collissions


def get_possibilities(value):
    val = [0, 1, 2, 3]
    val.remove(value)
    return val


def get_possibilities_2(input_array, pos):
    possibilities = []
    n = pos[0]
    m = pos[1]
    size = len(input_array[0]) - 1
    for i in [-1, 1]:
        if (m + i) >= 0 and m + i <= size:
            possibilities.append((m + i, n))
    for j in [-1, 1]:
        if (n + j) >= 0 and n + j <= size:
            possibilities.append((m, n + j))
    return possibilities


def generate_matrix(number_of_rows):
    data = []
    for i in range(number_of_rows):
        temp = []
        for j in range(number_of_rows):
            temp.append(random.randint(0, 3))
        data.append(temp)
    return data


def done(original, data):
    print("\n*Done*")
    print_data(data[0])
    print("Cost: " + str(data[1]))
    # draw(original, data[0])
    exit(0)


original_array = generate_matrix(int(input("\nEnter n: ")))

original_array = [[1, 1, 2], [1, 1, 2], [1, 2, 2]]

print_data(original_array)

count = 0
queue = []
extended_list = []
queue.append([original_array, 0, count_collisions(original_array)])

usr_input = int(input("\n1. BFS\n2. DFS\n3. Greedy Best First Search\n"))

if usr_input > 4 or usr_input < 0:
    print("Invalid Input!")
    exit(0)

while queue:
    popped_array = queue.pop(0)
    count = count + 1
    extended_list.append(popped_array[0])
    checked_pos = check(popped_array[0])
    if checked_pos == 1:
        done(original_array, popped_array)
    else:
        collisions = get_collissions(popped_array[0])

        for col in collisions:

            possibilities = get_possibilities_2(popped_array[0], col)

            m = col[0]
            n = col[1]

            for z in possibilities:
                print(queue)
                temp_data = copy.deepcopy(popped_array[0])
                swap_element = temp_data[m][n]
                temp_data[m][n] = temp_data[z[0]][z[1]]
                temp_data[z[0]][z[1]] = swap_element

                collissions = count_collisions(temp_data)
                insert_data = [temp_data, popped_array[1] + 1, collissions]

                if temp_data not in extended_list:
                    if usr_input == 1:
                        queue.append(insert_data)
                    elif usr_input == 2:
                        queue.insert(0, insert_data)
                    elif usr_input == 3:
                        queue.append(insert_data)
                        queue.sort(key=return_second)
                    # elif usr_input == 4:
                    #     queue.insert(0, [temp_data, popped_array[1] + 1, collissions])
                    #     queue.sort(key=return_second)
                print("Queue: " + str(len(queue)) + " Extended: " + str(len(extended_list)) + " Cost: " + str(
                    popped_array[1] + 1) + " Collissions: " + str(collissions))

                if check(temp_data) == 1:
                    done(original_array, [temp_data, popped_array[1] + 1])
print("\n*No possible Permutation found*")