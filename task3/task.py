import csv
import math
from io import StringIO


def calculate_entropy(matr: list[list[int]]) -> float:
    n = len(matr)
    if n <= 1:
        return 0.0
    k = len(matr[0])

    result = 0
    for j in range(n):
        for i in range(k):
            l_ij = matr[j][i]
            if l_ij > 0:
                prob = l_ij / (n - 1)
                result -= prob * math.log2(prob)

    return round(result, 1)


# вариант парсинга не в ноду
def parse_csv(csv_str: str) -> list[list[int]]:
    matr = []
    csv_reader = csv.reader(StringIO(csv_str), delimiter=',')

    for row in csv_reader:
        matr.append(list(map(int, row)))
    return matr


def main(csv_string: str) -> float:
    matrix = parse_csv(csv_string)
    entropy = calculate_entropy(matrix)
    return entropy


INPUT = '''
2,0,2,0,0
0,1,0,0,1
2,1,0,0,1
0,1,0,1,1
0,1,0,1,1
'''.strip()

if __name__ == '__main__':
    print(main(INPUT))
