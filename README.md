# DAA-CAPSTONE-assignment
# Mini-Courier Planner — DAA Capstone Project

An intelligent courier dispatch and route optimization prototype implemented in Python. This system integrates **Merge Sort**, **0/1 Knapsack Dynamic Programming**, **Dijkstra's Shortest Path Algorithm**, and the **Nearest-Neighbor TSP Approximation** to prioritize parcels, maximize delivery van utility, and compute minimal-distance delivery routes.

---

## 1. System Architecture & Algorithmic Pipeline

1. **Phase 1 — Data Modeling (`src/models.py`)**: Represents customer parcels (`Parcel` dataclass with weight, priority score, deadline, and urgency ratio) and the road network (`DeliveryGraph` adjacency list).
2. **Phase 2 — Prioritization & Packing (`src/sorting_knapsack.py`)**:
   - **Merge Sort**: Orders incoming parcels deterministically by earliest delivery deadline and descending priority score in $\mathcal{O}(N \log N)$ time.
   - **0/1 Knapsack (Dynamic Programming)**: Selects the priority-maximizing subset of parcels that fits within the courier van's weight capacity $W$ in $\mathcal{O}(N \cdot W)$ time.
3. **Phase 3 — Shortest Path & Route Planning (`src/graph_routing.py`)**:
   - **Dijkstra's Algorithm**: Uses a binary min-heap (`heapq`) to compute single-source shortest paths between the central hub and delivery nodes in $\mathcal{O}((V + E) \log V)$ time.
   - **Nearest-Neighbor TSP Heuristic**: Constructs a closed delivery tour across all selected parcel destinations in polynomial time.
4. **Phase 4 — Empirical Benchmarking (`src/benchmark.py`)**: Evaluates execution times across dataset sizes $N \in \{20, 50, 100, 250, 500\}$ and exports high-resolution charts.

---

## 2. Computational Complexity Analysis

| Module | Algorithm | Time Complexity | Space Complexity | Justification |
| :--- | :--- | :--- | :--- | :--- |
| Parcel Sorting | Merge Sort | $\mathcal{O}(N \log N)$ | $\mathcal{O}(N)$ | Stable, guaranteed worst-case $\mathcal{O}(N \log N)$ without QuickSort's $\mathcal{O}(N^2)$ pivot degradation. |
| Van Packing | 0/1 Knapsack (DP) | $\mathcal{O}(N \cdot W)$ | $\mathcal{O}(N \cdot W)$ | Guarantees global optimality for indivisible parcels, unlike Greedy Fractional Knapsack. |
| Shortest Path | Dijkstra (Min-Heap) | $\mathcal{O}((V + E) \log V)$ | $\mathcal{O}(V + E)$ | Optimal for non-negative road distances; outperforms Bellman-Ford $\mathcal{O}(V \cdot E)$. |
| Multi-Stop Tour | Nearest-Neighbor TSP | $\mathcal{O}(K(V + E)\log V + K^2)$ | $\mathcal{O}(V + K^2)$ | Avoids intractable $\mathcal{O}(K!)$ exact TSP complexity while yielding practical routes for $K$ stops. |

---

## 3. Repository Structure

```text
DAA-Capstone-Mini-Courier-Planner/
├── README.md                      # Project documentation & technical report
├── requirements.txt               # Python dependencies
├── .gitignore                     # Git ignore rules
├── mini_courier_planner.ipynb     # Interactive Jupyter Notebook implementation
├── datasets/
│   ├── parcels_sample.csv         # Sample parcel manifest
│   └── delivery_graph.csv         # Weighted city road network
└── src/
    ├── models.py                  # Parcel and DeliveryGraph classes
    ├── sorting_knapsack.py        # Merge Sort & 0/1 Knapsack DP
    ├── graph_routing.py           # Dijkstra & Nearest-Neighbor TSP
    ├── benchmark.py               # Runtime profiler & Matplotlib/NetworkX plots
    └── main.py                    # CLI pipeline entry point
