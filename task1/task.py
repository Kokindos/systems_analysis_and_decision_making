import json
import sys


class Node:
    def __init__(self, name: str):
        self.name = name
        self.children = []


def build_tree(data: dict[str, list[str]]) -> Node | None:
    nodes = {}
    all_nodes = set(data.keys())
    child_nodes = set()

    for name in data:
        if name not in nodes:
            nodes[name] = Node(name)

    for name, children in data.items():
        node = nodes[name]
        for child_name in children:
            if child_name not in nodes:
                nodes[child_name] = Node(child_name)
            child_node = nodes[child_name]
            child_nodes.add(child_name)
            node.children.append(child_node)

    root_candidates = all_nodes - child_nodes
    if root_candidates:
        root_name = root_candidates.pop()
        return nodes[root_name]
    return None


def print_tree(node: Node, level=0) -> None:
    print('  ' * level, node.name)
    for child in node.children:
        print_tree(child, level + 1)


def main(file_path: str) -> Node:
    with open(file_path) as file:
        data = json.load(file)

    root = build_tree(data['nodes'])

    print_tree(root)
    return root


if __name__ == '__main__':
    main(sys.argv[1])
