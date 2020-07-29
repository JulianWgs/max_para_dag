"""
Functions to get maximum number of concurrent tasks of a directed acyclic graph.
"""


def max_dag_para(graph):
    """
    Get the maximum number of concurrent tasks.
    """
    return max(dag_para(graph).values())


def dag_para(graph):
    """
    Get number of concurrent tasks and corresponding node.

    Implementation currently does not support multiple origin or end nodes.
    """

    # get start and end node
    n_predecessors_dict = dict()
    n_successors_dict = dict()
    for node in graph.nodes:
        n_predecessors_dict[node] = len(list(graph.predecessors(node)))
        n_successors_dict[node] = len(list(graph.successors(node)))
    origin = [key for key, value in n_predecessors_dict.items() if value == 0][0]
    end = [key for key, value in n_successors_dict.items() if value == 0][0]

    nodes = dict()
    visited = [origin]
    next_node = origin
    current_concurrency = 0
    concurrency = list()
    while next_node != end:
        for node in graph.successors(next_node):
            n_successors = len(list(graph.successors(node)))
            n_predecessors = len(
                [node for node in graph.predecessors(node)]
            )
            n_blocking = len(
                [node for node in graph.predecessors(node) if node not in visited]
            )
            nodes[node] = {
                "n_successors": n_successors,
                "n_predecessors": n_predecessors,
                "n_blocking": n_blocking,
            }
        nodes_filtered = {
            key: value for key, value in nodes.items() if value["n_blocking"] == 0
        }
        current_concurrency += len(list(graph.successors(next_node))) - len(
            list(graph.predecessors(next_node))
        )
        concurrency.append(current_concurrency)
        next_node = max(
            nodes_filtered.items(), key=lambda item: item[1]["n_successors"] - item[1]["n_predecessors"]
        )
        next_node = next_node[0]
        nodes.pop(next_node)
        visited.append(next_node)
    current_concurrency += len(list(graph.successors(next_node))) - len(
        list(graph.predecessors(next_node))
    )
    concurrency.append(current_concurrency)
    return dict(zip(visited, concurrency))
