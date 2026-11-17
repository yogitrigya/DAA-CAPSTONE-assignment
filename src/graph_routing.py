import heapq
from typing import Dict, List, Tuple
from src.models import DeliveryGraph


def dijkstra_shortest_paths(
    graph: DeliveryGraph, start_node: str
) -> Tuple[Dict[str, float], Dict[str, List[str]]]:
    """
    Computes single-source shortest paths using Dijkstra's Algorithm with a Min-Heap.
    Time Complexity: O((V + E) log V)
    Returns: (distances_dict, paths_dict)
    """
    distances: Dict[str, float] = {node: float("inf") for node in graph.get_nodes()}
    predecessors: Dict[str, str | None] = {node: None for node in graph.get_nodes()}
    distances[start_node] = 0.0

    pq: List[Tuple[float, str]] = [(0.0, start_node)]

    while pq:
        curr_dist, u = heapq.heappop(pq)
        if curr_dist > distances[u]:
            continue

        for neighbor, weight in graph.adj_list.get(u, []):
            new_dist = curr_dist + weight
            if new_dist < distances[neighbor]:
                distances[neighbor] = new_dist
                predecessors[neighbor] = u
                heapq.heappush(pq, (new_dist, neighbor))

    # Reconstruct full node-by-node paths
    paths: Dict[str, List[str]] = {}
    for node in graph.get_nodes():
        if distances[node] == float("inf"):
            paths[node] = []
            continue
        path = []
        curr = node
        while curr is not None:
            path.append(curr)
            curr = predecessors[curr]
        paths[node] = path[::-1]

    return distances, paths


def tsp_nearest_neighbor(
    graph: DeliveryGraph, depot: str, targets: List[str]
) -> Tuple[List[str], List[str], float]:
    """
    Approximates the Travelling Salesperson Problem (TSP) using the Greedy
    Nearest-Neighbor heuristic over precomputed Dijkstra shortest paths.
    Time Complexity: O(K * (V + E) log V + K^2), where K = number of targets.
    Returns: (visit_order, detailed_road_route, total_distance_km)
    """
    unvisited = set(targets)
    if depot in unvisited:
        unvisited.remove(depot)

    key_nodes = [depot] + list(unvisited)
    all_dists: Dict[str, Dict[str, float]] = {}
    all_paths: Dict[str, Dict[str, List[str]]] = {}

    for node in key_nodes:
        dists, paths = dijkstra_shortest_paths(graph, node)
        all_dists[node] = dists
        all_paths[node] = paths

    visit_order = [depot]
    detailed_route = [depot]
    total_distance = 0.0
    curr_node = depot

    while unvisited:
        next_node = min(unvisited, key=lambda target: all_dists[curr_node][target])
        step_dist = all_dists[curr_node][next_node]
        step_path = all_paths[curr_node][next_node]

        total_distance += step_dist
        visit_order.append(next_node)
        detailed_route.extend(step_path[1:])
        unvisited.remove(next_node)
        curr_node = next_node

    # Return trip to the central depot
    return_dist = all_dists[curr_node][depot]
    return_path = all_paths[curr_node][depot]
    total_distance += return_dist
    visit_order.append(depot)
    detailed_route.extend(return_path[1:])

    return visit_order, detailed_route, round(total_distance, 2)
