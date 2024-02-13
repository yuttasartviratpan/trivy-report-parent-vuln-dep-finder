from typing import List, Dict
from collections import deque


# Breath First Search
def bfs(dependency_graph: Dict, root_dependency: List, dependency_key: str) -> List:
    ans_lst = []
    visited = set()  # Set to keep track of visited nodes
    queue = deque([dependency_key])  # Initialize the queue with the starting node

    while queue:
        node = queue.popleft()  # Dequeue a node from the queue

        # Check if the node has already been visited
        if node in visited:
            continue

        # Mark the node as visited
        visited.add(node)

        # Check if the current node is in the search list
        if node in root_dependency:
            ans_lst.append(node)

        # Add the neighbors of the current node to the queue
        if node in dependency_graph:
            for neighbor in dependency_graph[node]:
                queue.append(neighbor)

    return ans_lst