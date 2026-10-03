import heapq
import sys
from collections import defaultdict
from typing import List, Dict, Set, Tuple, Optional

def resolve_module_dependencies(modules: List[str], dependencies: List[Tuple[str, str]]) -> str:
    adj: Dict[str, Set[str]] = defaultdict(set)
    in_degree: Dict[str, int] = {mod: 0 for mod in modules}

    for mod_a, mod_b in dependencies:
        if mod_b not in adj[mod_a]:
            if mod_a in in_degree and mod_b in in_degree:
                if mod_a not in adj[mod_b]:
                    adj[mod_b].add(mod_a)
                    in_degree[mod_a] += 1

    heap: List[str] = [mod for mod in modules if in_degree[mod] == 0]
    heapq.heapify(heap)

    loading_order: List[str] = []

    while heap:
        curr = heapq.heappop(heap)
        loading_order.append(curr)

        for neighbor in sorted(adj[curr]):
            in_degree[neighbor] -= 1
            if in_degree[neighbor] == 0:
                heapq.heappush(heap, neighbor)

    if len(loading_order) == len(modules):
        return " ".join(loading_order)

    unresolved = [m for m in modules if in_degree[m] > 0]
    cycle_path = find_cycle(unresolved, adj)
    return f"CYCLE {' '.join(cycle_path)}"

def find_cycle(unresolved: List[str], adj: Dict[str, Set[str]]) -> List[str]:
    state: Dict[str, int] = {}
    parent: Dict[str, str] = {}
    cycle_nodes: List[str] = []

    def dfs(node: str) -> bool:
        state[node] = 1
        for neighbor in sorted(adj[node]):
            if state.get(neighbor, 0) == 1:
                curr = node
                path = [neighbor, curr]
                while curr != neighbor and curr in parent:
                    curr = parent[curr]
                    path.append(curr)
                path.reverse()
                cycle_nodes.extend(path)
                return True
            elif state.get(neighbor, 0) == 0:
                parent[neighbor] = node
                if dfs(neighbor):
                    return True
        state[node] = 2
        return False

    for node in unresolved:
        if state.get(node, 0) == 0:
            if dfs(node):
                break

    return cycle_nodes if cycle_nodes else unresolved

if __name__ == "__main__":
    lines = [line.strip() for line in sys.stdin if line.strip()]
    if lines:
        first = lines[0].split()
        n, e = int(first[0]), int(first[1])
        modules = [lines[i] for i in range(1, 1 + n)]
        dependencies = []
        for i in range(1 + n, 1 + n + e):
            parts = lines[i].split()
            if len(parts) >= 2:
                dependencies.append((parts[0], parts[1]))
        output = resolve_module_dependencies(modules, dependencies)
        print(output)
