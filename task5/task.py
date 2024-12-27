import json
import numpy as np


def load_mat(json_str: str) -> list[list[int]]:
    data = json.loads(json_str)
    clusters = []
    n = 0
    for c in data:
        clusters.append(c if isinstance(c, list) else [c])
        n += len(clusters[-1])

    matrix = [[1] * n for _ in range(n)]
    less = []
    for c in clusters:
        for worse in less:
            for element in c:
                matrix[element - 1][worse - 1] = 0
        for element in c:
            less.append(element)

    return matrix


def main(a: str, b: str) -> str:
    A = np.array(load_mat(a))
    B = np.array(load_mat(b))

    AB = A * B
    AB_T = A.T * B.T
    M = np.maximum(AB, AB_T)

    core = set()
    for i in range(len(M)):
        for j in range(i + 1, len(M)):
            if M[i, j] == 0 and M[j, i] == 0:
                core.add((i + 1, j + 1))

    result = []
    for pair in sorted(core):
        result.append(pair[0] if len(pair) == 1 else pair)
    return json.dumps(result)


A = '[1,[2,3],4,[5,6,7],8,9,10]'
B = '[[1,2],[3,4,5],6,7,9,[8,10]]'

if __name__ == '__main__':
    print(main(A, B))