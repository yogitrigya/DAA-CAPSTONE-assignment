import csv
import os
import sys
from tabulate import tabulate

# Ensure parent root is in path when running `python src/main.py`
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.models import DeliveryGraph, Parcel
from src.sorting_knapsack import merge_sort_parcels, optimize_van_loading_dp
from src.graph_routing import dijkstra_shortest_paths, tsp_nearest_neighbor
from src.benchmark import run_scalability_benchmarks, save_visualizations


def load_parcels(filepath: str) -> list[Parcel]:
    parcels = []
    with open(filepath, mode="r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            parcels.append(
                Parcel(
                    parcel_id=row["parcel_id"],
                    destination=row["destination"],
                    weight=int(row["weight_kg"]),
                    value=int(row["priority_value"]),
                    deadline=int(row["deadline_hrs"]),
                    customer_name=row["customer_name"],
                )
            )
    return parcels


def load_graph(filepath: str) -> DeliveryGraph:
    graph = DeliveryGraph()
    with open(filepath, mode="r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            graph.add_edge(row["source"], row["target"], float(row["distance_km"]))
    return graph


def main() -> None:
    VAN_CAPACITY_KG = 25
    DEPOT = "Central_Hub"

    print("=" * 72)
    print("        MINI-COURIER PLANNER - INTEGRATED CAPSTONE SYSTEM")
    print("=" * 72)

    parcels = load_parcels("datasets/parcels_sample.csv")
    graph = load_graph("datasets/delivery_graph.csv")

    # PHASE 2A: Merge Sort Prioritization
    print("\n[PHASE 2A] Sorting Parcels by Deadline & Priority Value (Merge Sort)...")
    sorted_parcels = merge_sort_parcels(parcels)
    sort_table = [
        [p.parcel_id, p.customer_name, p.destination, f"{p.weight} kg", p.value, f"{p.deadline} hrs", p.urgency_ratio]
        for p in sorted_parcels
    ]
    print(tabulate(sort_table, headers=["ID", "Customer", "Destination", "Weight", "Priority", "Deadline", "Urgency"], tablefmt="fancy_grid"))

    # PHASE 2B: 0/1 Knapsack Capacity Optimization
    print(f"\n[PHASE 2B] Optimizing Delivery Van Packing (Max Capacity = {VAN_CAPACITY_KG} kg)...")
    max_val, packed_parcels, _ = optimize_van_loading_dp(sorted_parcels, VAN_CAPACITY_KG)
    total_weight = sum(p.weight for p in packed_parcels)

    pack_table = [
        [p.parcel_id, p.destination, f"{p.weight} kg", p.value, f"{p.deadline} hrs"]
        for p in packed_parcels
    ]
    print(tabulate(pack_table, headers=["Selected ID", "Destination", "Weight", "Priority", "Deadline"], tablefmt="fancy_grid"))
    print(f"--> Total Packed Weight : {total_weight} / {VAN_CAPACITY_KG} kg")
    print(f"--> Total Priority Score: {max_val}")

    # PHASE 3A: Single-Source Shortest Paths from Depot
    print(f"\n[PHASE 3A] Computing Shortest Paths from {DEPOT} (Dijkstra's Algorithm)...")
    dists, paths = dijkstra_shortest_paths(graph, DEPOT)
    dijkstra_table = [
        [dest, f"{dists[dest]:.2f} km", " -> ".join(paths[dest])]
        for dest in sorted(graph.get_nodes()) if dest != DEPOT
    ]
    print(tabulate(dijkstra_table, headers=["Destination", "Shortest Distance", "Optimal Path from Depot"], tablefmt="fancy_grid"))

    # PHASE 3B: Nearest-Neighbor TSP Route Planning
    delivery_stops = list(dict.fromkeys(p.destination for p in packed_parcels))
    print(f"\n[PHASE 3B] Generating Delivery Tour for {len(delivery_stops)} Stops (Nearest-Neighbor TSP)...")
    visit_order, detailed_route, total_km = tsp_nearest_neighbor(graph, DEPOT, delivery_stops)
    print(f"--> Stop Sequence     : {' -> '.join(visit_order)}")
    print(f"--> Full Road Traverse: {' -> '.join(detailed_route)}")
    print(f"--> Total Route Length: {total_km:.2f} km")

    # PHASE 4: Scalability Benchmarking & Chart Generation
    print("\n[PHASE 4] Running Scalability Benchmarks & Generating Visuals...")
    bench_results = run_scalability_benchmarks([20, 50, 100, 250, 500])
    print(tabulate(bench_results, headers="keys", tablefmt="fancy_grid"))

    save_visualizations(bench_results, graph, detailed_route, DEPOT)
    print("\n[SUCCESS] Charts saved to 'images/runtime_comparison.png' and 'images/route_visualization.png'.")


if __name__ == "__main__":
    main()
