"""
Functions to get maximum number of concurrent tasks of a directed acyclic graph.
"""
import uuid


def max_dag_para(graph):
    """
    Get the maximum number of concurrent tasks.
    """
    return max(dag_para(graph).values())


def dag_para(graph):
    """
    Get number of concurrent tasks and corresponding node.

    """

    graph = graph.copy()
    # get start and end node
    n_predecessors_dict = dict()
    n_successors_dict = dict()
    for node in graph.nodes:
        n_predecessors_dict[node] = len(list(graph.predecessors(node)))
        n_successors_dict[node] = len(list(graph.successors(node)))
    # Connect nodes with no predecessors to origin node and with successors to end node
    # Give node of origin and end need an unique name
    origins = [key for key, value in n_predecessors_dict.items() if value == 0]
    origin = "origin_" + uuid.uuid4().hex[:8]
    for node in origins:
        graph.add_edge(origin, node)
    ends = [key for key, value in n_successors_dict.items() if value == 0]
    end = "end_" + uuid.uuid4().hex[:8]
    for node in ends:
        graph.add_edge(node, end)
    # get blocking nodes and difference of in- and output edges
    edge_sum = dict()
    blocking = dict()
    for node in graph.nodes:
        edge_sum[node] = len(list(graph.successors(node))) - len(
            list(graph.predecessors(node))
        )
        blocking[node] = list(graph.predecessors(node))
    visited = {origin}
    next_node = origin
    concurrency = edge_sum[next_node]
    concurrency_list = [concurrency]
    # Calculate sorted list of nodes.
    sorted_nodes = sorted(edge_sum, key=edge_sum.get, reverse=True)
    # Iterate over nodes until reaching the end node
    while next_node != end:
        # Remove visited nodes from blocking nodes
        for node, blocking_nodes in blocking.items():
            blocking[node] = [
                blocking_node
                for blocking_node in blocking_nodes
                if blocking_node not in visited
            ]
        # Remove nodes which don't have any blocking nodes
        blocking = {
            node: blocked_nodes
            for node, blocked_nodes in blocking.items()
            if len(blocked_nodes) != 0
        }
        # Select the first item of sorted_nodes
        # (highest number of successors - predecessors)
        # which was not yet visited and is not blocked
        next_node = [
            node
            for node in sorted_nodes
            if (node not in blocking.keys()) and (node not in visited)
        ][0]
        # Update concurrency and add next_node to visited nodes
        concurrency += edge_sum[next_node]
        concurrency_list.append(concurrency)
        visited.add(next_node)
    return dict(zip(visited, concurrency_list))
