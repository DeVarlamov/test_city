import heapq
import math
import random

from matplotlib import pyplot as plt


class CityGrid:
    def __init__(self, n, m, coverage=0.3):
        self.n = n
        self.m = m
        self.grid = [[0] * m for _ in range(n)]
        self.place_obstructed_blocks(coverage)

    def place_obstructed_blocks(self, coverage):
        """Генерация случайных заблокированных блоков."""
        total_blocks = self.n * self.m
        obstructed_blocks = int(total_blocks * coverage)

        while obstructed_blocks > 0:
            row = random.randint(0, self.n - 1)
            col = random.randint(0, self.m - 1)

            if self.grid[row][col] == 0:
                self.grid[row][col] = 1
                obstructed_blocks -= 1

    def place_tower(self, row, col, radius):
        """
        Каждая вышка имеет фиксированный диапазон R
        (в блоках), в пределах которого она
        обеспечивает покрытие. Это покрытие представляет собой
        квадрат с башней в центре.
        Реализуйте метод в классе CityGrid для размещения башни
        и визуализации ее покрытия.
        """
        for i in range(max(0, row - radius), min(self.n, row + radius + 1)):
            for j in range(max(0, col - radius),
                           min(self.m, col + radius + 1)):
                self.grid[i][j] = 2

    def optimize_towers(self, radius):
        """
        Задача 3: Задача оптимизации
        Разработайте алгоритм размещения минимального количества
        вышек таким образом, чтобы все незащищенные блоки находились в зоне
        действия по крайней мере одной вышки. Алгоритм не может размещать
        башни на блокированных участках.
        Реализуйте метод в классе CityGrid для отображения размещения башен.
        """
        unprotected_blocks = []  # Список незащищенных блоков

        for i in range(self.n):
            for j in range(self.m):
                if self.grid[i][j] == 0:
                    unprotected_blocks.append((i, j))

        while unprotected_blocks:
            block = unprotected_blocks.pop(0)
            row, col = block
            nearest_tower = None
            min_distance = math.inf

            for i in range(self.n):
                for j in range(self.m):
                    if self.grid[i][j] == 2:
                        distance = math.sqrt((i - row) ** 2 + (j - col) ** 2)
                        if distance <= radius and distance < min_distance:
                            nearest_tower = (i, j)
                            min_distance = distance

            if nearest_tower is None:
                self.place_tower(row, col, radius)
            else:
                self.grid[nearest_tower[0]][nearest_tower[1]] = 2

    def find_most_reliable_path(self, start_row, start_col, end_row, end_col):
        """Task 4: Path Reliability
        Imagine that data is transmitted between towers. For simplicity,
        assume that each tower can
        directly communicate with any other tower within its range.
        Design an algorithm to find the most reliable path between two towers.
        The reliability of a path decreases with the number of hops
        (tower-to-tower links). So, a path with fewer hops is more reliable.
        """
        distances = [[float('inf')] * self.m for _ in range(self.n)]
        distances[start_row][start_col] = 0
        queue = [(0, start_row, start_col)]
        while queue:
            current_dist, row, col = heapq.heappop(queue)
            if row == end_row and col == end_col:
                return current_dist

            for i, j in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
                new_row, new_col = row + i, col + j

                if 0 <= new_row < self.n and 0 <= new_col < self.m:
                    weight = 1 / (
                        self.grid[row][col] + self.grid[new_row][new_col])
                    if current_dist + weight < distances[new_row][new_col]:
                        distances[new_row][new_col] = current_dist + weight
                        heapq.heappush(queue, (
                            current_dist + weight, new_row, new_col))

        return None

    def plot_grid(self):
        """Метод визуализации матрицы."""
        fig, ax = plt.subplots()
        for i in range(self.n):
            for j in range(self.m):
                if self.grid[i][j] == 0:
                    ax.add_patch(plt.Rectangle((j, i), 1, 1, color='white'))
                elif self.grid[i][j] == 1:
                    ax.add_patch(plt.Rectangle((j, i), 1, 1, color='black'))
                elif self.grid[i][j] == 2:
                    ax.add_patch(plt.Rectangle((j, i), 1, 1, color='green'))
        ax.set_xlim([0, self.m])
        ax.set_ylim([0, self.n])
        ax.set_aspect('equal')
        plt.show()

    def plot_coverage(self):
        """Метод визуализации зоны покрытия."""
        fig, ax = plt.subplots()
        for i in range(self.n):
            for j in range(self.m):
                if self.grid[i][j] == 2:
                    ax.add_patch(plt.Rectangle(
                        (j - 2, i - 2), 5, 5, color='green', alpha=0.2))
        ax.set_xlim([0, self.m])
        ax.set_ylim([0, self.n])
        ax.set_aspect('equal')
        plt.show()

    def plot_path(self, start_row, start_col, end_row, end_col):
        """Метод визуализации пути."""
        fig, ax = plt.subplots()
        for i in range(self.n):
            for j in range(self.m):
                if self.grid[i][j] == 0:
                    ax.add_patch(plt.Rectangle((j, i), 1, 1, color='white'))
                elif self.grid[i][j] == 1:
                    ax.add_patch(plt.Rectangle((j, i), 1, 1, color='black'))
                elif self.grid[i][j] == 2:
                    ax.add_patch(plt.Rectangle((j, i), 1, 1, color='green'))
        ax.plot(
            [start_col + 0.5, end_col + 0.5],
            [start_row + 0.5, end_row + 0.5], color='red')
        ax.set_xlim([0, self.m])
        ax.set_ylim([0, self.n])
        ax.set_aspect('equal')
        plt.show()

    def print_grid(self):
        """Метод вывода матрицы."""
        for row in self.grid:
            print(row)


if __name__ == "__main__":
    grid = CityGrid(10, 10)
    grid.optimize_towers(2)
    grid.plot_grid()
    grid.plot_coverage()
    grid.plot_path(1, 1, 8, 8)
