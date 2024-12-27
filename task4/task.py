import csv
import math
from collections.abc import Iterable

def compute_log_probability(p: float) -> float:
    return -p * math.log2(p)

def calculate_probabilities(data: list[list[int]]) -> list[list[float]]:
    total_sum = sum(map(sum, data))
    return [[value / total_sum for value in row] for row in data]

def calculate_entropy(probabilities: list[list[float]]) -> float:
    return sum(compute_log_probability(p) for row in probabilities for p in row)

def calculate_joint_entropy(probabilities: Iterable[Iterable[float]]) -> list[float]:
    return [compute_log_probability(sum(row)) for row in probabilities]

def calculate_conditional_entropy(probabilities: list[list[float]]) -> list[float]:
    conditional_entropy = []
    for row in probabilities:
        row_sum = sum(row)
        conditioned_row = [p / row_sum for p in row if row_sum > 0]
        conditional_entropy.append(sum(compute_log_probability(p) for p in conditioned_row))
    return conditional_entropy

def calc_result(data: list[list[int]]) -> list[float]:
    probabilities = calculate_probabilities(data)
    H_AB = calculate_entropy(probabilities)

    H_A = sum(calculate_joint_entropy(probabilities))
    H_B = sum(calculate_joint_entropy(zip(*probabilities)))  # Transpose matrix for B

    conditional_entropy_A = calculate_conditional_entropy(probabilities)
    H_a_B = sum(row_conditional * row_prob_sum
               for row_conditional, row_prob_sum in zip(conditional_entropy_A, map(sum, probabilities)))

    I_A_B = H_A - H_a_B

    return [round(value, 2) for value in (H_AB, H_A, H_B, H_a_B, I_A_B)]


def main() -> list[float]:
    with open('input.csv') as fd:
        reader = csv.reader(fd)
        next(reader)  # Skip header
        data = [list(map(int, row[1:])) for row in reader]
    return calc_result(data)

INPUT = '''
20,15,10,5
30,20,15,10
25,25,20,15
20,20,25,20
15,15,30,25
'''.strip()

if __name__ == '__main__':
    print(main())
