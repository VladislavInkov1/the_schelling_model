import numpy as np
import random
import matplotlib.pyplot as plt
import os

n = int(input('Введите размерность матрицы: '))
iter_k = int(input('Введите число итераций: '))
number_of_friends = int(input('Сколько друзей нужно клетке для счастья? '))
iteration_frequency = int(input('Через сколько итераций сохранять матрицу? '))



def delete_previous_experiment():
    for f in os.listdir('img_iteration/'):
        os.remove(os.path.join('img_iteration/', f))


# generating an n*n matrix with a random distribution of cells
def matrix_creation(n):
    selection = ['красный', 'синий', 'пустой']
    matrix = np.random.choice(selection, (n, n), p = [0.45, 0.45, 0.1])
    return matrix


# checks if the cell is unhappy
def is_unhappy_cell(i, j, matrix):
    offsets = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
    friends_counter = 0
    for di, dj in offsets:
        ni, nj = i + di, j + dj
        if ni in range(len(matrix)) and nj in range(len(matrix)) and matrix[ni][nj] == matrix[i][j]:
            friends_counter += 1
    if friends_counter >= number_of_friends:
        return False
    else:
        return True


# selection of unhappy and empty cells
def cell_separation(matrix):
    unhappy_cells = []
    empty_cells = []
    for i, row in enumerate(matrix):
        for j, column in enumerate(row):
            if matrix[i][j] == (255, 255, 255):
                empty_cells.append((i, j))
            else:
                if is_unhappy_cell(i, j, matrix):
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
    new_a_i, new_a_j = empty_cells[new_adress][0], empty_cells[new_adress][1]
    old_a_i, old_a_j = unhappy_cells[old_address][0], unhappy_cells[old_address][1]
    matrix[new_a_i][new_a_j], matrix[old_a_i][old_a_j] = matrix[old_a_i][old_a_j], matrix[new_a_i][new_a_j]
    empty_cells.pop(new_adress)
    empty_cells.append(unhappy_cells[old_address])
    unhappy_cells.pop(old_address)
    if is_unhappy_cell(new_a_i, new_a_j, matrix):
        unhappy_cells.append((new_a_i, new_a_j))
    offsets = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
    for di, dj in offsets:
        ni, nj = new_a_i + di, new_a_j + dj
        if ni in range(len(matrix)) and nj in range(len(matrix)):
            if is_unhappy_cell(ni, nj, matrix) and matrix[ni][nj] != (255, 255, 255) and not((ni, nj) in unhappy_cells):
                unhappy_cells.append((ni, nj))
            elif not(is_unhappy_cell(ni, nj, matrix)) and (ni, nj) in  unhappy_cells:
                unhappy_cells.remove((ni, nj))
        oi, oj = old_a_i + di, old_a_j + dj
        if oi in range(len(matrix)) and oj in range(len(matrix)):
            if is_unhappy_cell(oi, oj, matrix) and matrix[oi][oj] != (255, 255, 255) and not((oi, oj) in unhappy_cells):
                unhappy_cells.append((oi, oj))
            elif not(is_unhappy_cell(oi, oj, matrix)) and (oi, oj) in  unhappy_cells:
                unhappy_cells.remove((oi, oj))
    return matrix, unhappy_cells, empty_cells


# moving a given number of unlucky cells
def relocation(matrix, iter_k):
    plt.imshow(matrix)
    plt.savefig('img_iteration/matrix_' + str(0) + '.png')
    unhappy_cells, empty_cells = cell_separation(matrix)
    for k in range(iter_k):
        matrix, unhappy_cells, empty_cells = choosing_migrant(matrix, unhappy_cells, empty_cells)
        if (k + 1) % iteration_frequency == 0:
            plt.imshow(matrix)
            plt.savefig('img_iteration/matrix_' + str(k + 1) + '.png')
        if len(unhappy_cells) == 0:
            plt.imshow(matrix)
            plt.savefig('img_iteration/matrix_' + str(k + 1) + '.png')
            return print('Все клетки счастливы! \n Остановка на ', k + 1, ' итерации')

delete_previous_experiment()
matrix = matrix_creation(n)
matrix = matrix.tolist()
matrix = matrix_conversion(matrix)
matrix = relocation(matrix, iter_k)
