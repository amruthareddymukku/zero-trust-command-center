# blast_radius.py

from collections import deque


def calculate_blast_radius(graph, compromised_agent):

    visited = set()
    queue = deque([compromised_agent])

    reachable_resources = []

    while queue:

        current = queue.popleft()

        if current in visited:
            continue

        visited.add(current)

        for neighbour in graph.get(current, []):

            if neighbour not in visited:

                queue.append(neighbour)

                if neighbour.startswith("RESOURCE:"):

                    resource_name = neighbour.replace(
                        "RESOURCE:",
                        ""
                    )

                    reachable_resources.append(
                        resource_name
                    )

    return reachable_resources