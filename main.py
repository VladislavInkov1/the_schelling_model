import numpy as np
import random
import matplotlib.pyplot as plt

n = int(input('Введите размерность матрицы: '))
iter_k = int(input('Введите число итераций: '))


# generating an n*n matrix with a random distribution of cells
def matrix_creation(n):
    selection = ['красный', 'синий', 'пустой']
    matrix = np.random.choice(selection, (n, n), p = [0.45, 0.45, 0.1])
    return matrix


# selection of unhappy and empty cells
def cell_separation(matrix):
    unhappy_cells = []
    empty_cells = []
    offsets = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
    for i, row in enumerate(matrix):
        for j, column in enumerate(row):
            friends_counter = 0
            if matrix[i][j] == (255, 255, 255):
                empty_cells.append((i, j))
            else:
                for di, dj in offsets:
                    ni, nj = i + di, j + dj
                    if ni in range(len(matrix)) and nj in range(len(matrix)) and matrix[ni][nj] == matrix[i][j]:
                        friends_counter += 1
                if friends_counter < 3:
                    unhappy_cells.append((i, j))
    return unhappy_cells, empty_cells


# assigning colors to each cell
def matrix_conversion(matrix):
    for i, row in enumerate(matrix):
        for j, column in enumerate(row):
            if column == 'пустой':
                matrix[i][j] = (255, 255, 255)
            elif column == 'красный':
                matrix[i][j] = (255, 0, 0)
            else:
                matrix[i][j] = (0, 0, 255)
    return matrix


# sampling and moving a random unfortunate cell
def choosing_migrant(matrix, unhappy_cells, empty_cells):
    old_address = random.randint(0, len(unhappy_cells) - 1)
    new_adress = random.randint(0, len(empty_cells) - 1)
    try:
        new_a_i, new_a_j = unhappy_cells[new_adress][1], unhappy_cells[new_adress][1]
        old_a_i, old_a_j = empty_cells[new_adress][1], empty_cells[new_adress][1]
        matrix[new_a_i][new_a_j], matrix[old_a_i][old_a_j] = matrix[old_a_i][old_a_j], matrix[new_a_i][new_a_j]
    except:
        print('Все клетки счастливы!')
    return matrix

# moving a given number of unlucky cells
def relocation(matrix, iter_k):
    for k in range(iter_k):
        unhappy_cells, empty_cells = cell_separation(matrix)
        matrix = choosing_migrant(matrix, unhappy_cells, empty_cells)
        if k%1000 == 0:
            plt.imshow(matrix)
            plt.savefig('img_iteration/matrix_' + str(k) + '.png')
    return matrix


matrix = matrix_creation(n)
matrix = matrix.tolist()
matrix = matrix_conversion(matrix)
plt.imshow(matrix)
plt.savefig('img_iteration/matrix_start.png')
matrix = relocation(matrix, iter_k)
plt.imshow(matrix)
plt.savefig('img_iteration/matrix_end.png')
