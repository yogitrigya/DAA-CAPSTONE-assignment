import os
import random
import time
from typing import Dict, List
import matplotlib.pyplot as plt
import networkx as nx

from src.models import DeliveryGraph, Parcel
from src.sorting_knapsack import merge_sort_parcels, optimize_van_loading_dp
from src.graph_routing import dijkstra_shortest_paths, tsp_nearest_neighbor


def run_scalability_benchmarks(sizes: List[int] = [20, 50, 100, 250, 500]) -> List[Dict]:
    """Benchmarks runtime (ms) across major algorithmic modules for varying N."""
    results = []

    for n in sizes:
        # Generate synthetic parcels
        parcels = [
            Parcel(
                parcel_id=f"P{i:04d}",
                destination=f"Node_{random.randint(1, max(10, n // 3))}",
                weight=random.randint(1, 15),
                value=random.randint(20, 200),
                deadline=random.randint(1, 12),
            )
            for i in range(n)
        ]

        # Generate synthetic connected graph
        num_nodes = max(15, n // 2)
        graph = DeliveryGraph()
        for i in range(num_nodes - 1):
            graph.add_edge(f"Node_{i}", f"Node_{i+1}", round(random.uniform(1.5, 10.0), 1))
        for _ in range(num_nodes * 2):
            u = f"Node_{random.randint(0, num_nodes - 1)}"
            v = f"Node_{random.randint(0, num_nodes - 1)}"
            if u != v:
                graph.add_edge(u, v, round(random.uniform(1.5, 15.0), 1))

        # 1. Benchmark Merge Sort
        t0 = time.perf_counter()
        merge_sort_parcels(parcels)
        t_sort = (time.perf_counter() - t0) * 1000

        # 2. Benchmark 0/1 Knapsack DP (Fixed vehicle capacity = 100 kg)
        t0 = time.perf_counter()
        optimize_van_loading_dp(parcels, max_capacity=100)
        t_dp = (time.perf_counter() - t0) * 1000

        # 3. Benchmark Dijkstra
        t0 = time.perf_counter()
        dijkstra_shortest_paths(graph, "Node_0")
        t_dijkstra = (time.perf_counter() - t0) * 1000

        # 4. Benchmark TSP Nearest Neighbor (Cap target stops at 35 for realistic tour size)
        targets = [f"Node_{i}" for i in range(1, min(35, num_nodes))]
        t0 = time.perf_counter()
        tsp_nearest_neighbor(graph, "Node_0", targets)
        t_tsp = (time.perf_counter() - t0) * 1000

        results.append({
            "Input Size (N)": n,
            "Merge Sort (ms)": round(t_sort, 3),
            "Knapsack DP (ms)": round(t_dp, 3),
            "Dijkstra (ms)": round(t_dijkstra, 3),
            "TSP Route (ms)": round(t_tsp, 3),
        })

    return results


def save_visualizations(
    benchmark_results: List[Dict],
    graph: DeliveryGraph,
    detailed_route: List[str],
    depot: str,
    output_dir: str = "images",
) -> None:
    """Generates and saves runtime comparison charts and route network graphs."""
    os.makedirs(output_dir, exist_ok=True)

    # 1. Runtime Comparison Chart
    sizes = [r["Input Size (N)"] for r in benchmark_results]
    plt.figure(figsize=(10, 6))
    plt.plot(sizes, [r["Merge Sort (ms)"] for r in benchmark_results], marker="o", linewidth=2, label="Merge Sort O(N log N)")
    plt.plot(sizes, [r["Knapsack DP (ms)"] for r in benchmark_results], marker="s", linewidth=2, label="0/1 Knapsack DP O(N*W)")
    plt.plot(sizes, [r["Dijkstra (ms)"] for r in benchmark_results], marker="^", linewidth=2, label="Dijkstra O((V+E) log V)")
    plt.plot(sizes, [r["TSP Route (ms)"] for r in benchmark_results], marker="d", linewidth=2, label="TSP Nearest-Neighbor")
    plt.title("Mini-Courier Planner: Algorithmic Runtime Comparison", fontsize=13, fontweight="bold")
    plt.xlabel("Dataset Size (N)", fontsize=11)
    plt.ylabel("Execution Time (ms)", fontsize=11)
    plt.grid(True, linestyle="--", alpha=0.6)
    plt.legend()
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, "runtime_comparison.png"), dpi=300)
    plt.close()

    # 2. Delivery Route Network Graph
    G = nx.Graph()
    for u, neighbors in graph.adj_list.items():
        for v, w in neighbors:
            G.add_edge(u, v, weight=w)

    pos = nx.spring_layout(G, seed=42, k=0.9)
    plt.figure(figsize=(12, 8))

    # Draw base network
    nx.draw_networkx_edges(G, pos, edge_color="#cccccc", width=1.5)
    edge_labels = nx.get_edge_attributes(G, "weight")
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=8)

    # Highlight active TSP route edges
    route_edges = [(detailed_route[i], detailed_route[i + 1]) for i in range(len(detailed_route) - 1)]
    nx.draw_networkx_edges(G, pos, edgelist=route_edges, edge_color="#e63946", width=3.0)

    # Color nodes by role
    node_colors = []
    for node in G.nodes():
        if node == depot:
            node_colors.append("#2a9d8f")  # Depot in Teal
        elif node in detailed_route:
            node_colors.append("#f4a261")  # Visited stops in Orange
        else:
            node_colors.append("#e9ecef")  # Unvisited nodes in Light Gray

    nx.draw_networkx_nodes(G, pos, node_color=node_colors, node_size=900, edgecolors="#264653")
    nx.draw_networkx_labels(G, pos, font_size=9, font_weight="bold")

    plt.title("Optimized Courier Delivery Route (Dijkstra + Nearest-Neighbor TSP)", fontsize=13, fontweight="bold")
    plt.axis("off")
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, "route_visualization.png"), dpi=300)
    plt.close()
