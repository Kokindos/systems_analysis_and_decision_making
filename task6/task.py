import json
from bisect import bisect_right
from collections import defaultdict
from typing import NamedTuple


class FuzzySetError(Exception):
    pass


class Term(NamedTuple):
    name: str
    points: list[tuple[int, float]]


class LingVar(NamedTuple):
    name: str
    terms: list[Term]


def load_ling_var(json_str: str) -> LingVar:
    data = json.loads(json_str)
    name = list(data.keys())[0]
    terms = []
    for item in data[name]:
        points = sorted([tuple(point) for point in item['points']])
        terms.append(Term(item['id'], points))
    return LingVar(name, terms)

def fuzzify(ling_var: LingVar, value: float) -> dict[str, float]:
    d = {}
    for term in ling_var.terms:
        idx = bisect_right(term.points, (value, 0))

        left = term.points[idx - 1]
        right = term.points[idx]

        d[term.name] = left[1] + (right[1] - left[1]) * (value - left[0]) / (right[0] - left[0])

    return d


def main(temperature_json: str, regulator_json: str, mapping_json: str, cur_temp: float) -> float:
    temp = load_ling_var(temperature_json)
    reg = load_ling_var(regulator_json)
    mapping = dict(json.loads(mapping_json))

    fuzzy_temperature = fuzzify(temp, cur_temp)
    fuzzy_regulator = {mapping[item]: fuzzy_temperature[item] for item in fuzzy_temperature}

    maximums = defaultdict(list)
    for term in reg.terms:
        fuzzy_value = fuzzy_regulator[term.name]
        updated_points = [(point[0], min(point[1], fuzzy_value)) for point in term.points]

        if fuzzy_value > 0:
            max_value, max_truth = max(updated_points, key=lambda x: x[1])
            maximums[max_truth].append(max_value)

    max_truth = max(maximums)
    return min(maximums[max_truth])



if __name__ == '__main__':
    args = []
    with open('temp.json') as t_fd, open('reg.json') as r_fd, open('mapping.json') as m_fd:
        print(main(
            temperature_json=t_fd.read(),
            regulator_json=r_fd.read(),
            mapping_json=m_fd.read(),
            cur_temp=19,
        ))
