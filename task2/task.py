import csv
from collections import defaultdict
from io import StringIO

from task1.task import Node, build_tree


def dfs(node: Node, extension_lengths: dict[Node, dict[str, int]], level_nodes: dict[int, list[Node]],
        depth: int = 0) -> None:
    extension_lengths[node]['r1'] = len(node.children)
    extension_lengths[node]['r2'] = 1 if depth > 0 else 0
    extension_lengths[node]['r4'] = max(0, depth - 1)
    level_nodes[depth].append(node)

    for child in node.children:
        dfs(child, extension_lengths, level_nodes, depth + 1)

        extension_lengths[node]['r3'] += extension_lengths[child]['r1']


def parse_csv(csv_string: str) -> Node:
    reader = csv.reader(csv_string.splitlines(), delimiter=',')
    edges = defaultdict[str, list](list)

    for parent, child in reader:
        edges[parent].append(child)

    return build_tree(dict(edges))


def get_extension_lengths(root: Node):
    extension_lengths = defaultdict[Node, dict[str, int]](lambda: {f'r{i}': 0 for i in range(1, 6)})
    level_nodes = defaultdict[int, list[Node]](list)

    dfs(root, extension_lengths, level_nodes)

    for depth, nodes in level_nodes.items():
        for node in nodes:
            extension_lengths[node]['r5'] = len(nodes) - 1
    return extension_lengths


def main(csv_string: str) -> str:
    root = parse_csv(csv_string)
    extension_lengths = get_extension_lengths(root)

    output = StringIO()
    writer = csv.writer(output)
    for node, lengths in extension_lengths.items():
        writer.writerow(lengths.values())
    return output.getvalue()


INPUT = '''
1,2
1,3
3,4
3,5
'''.strip()

if __name__ == '__main__':
    print(main(INPUT))
