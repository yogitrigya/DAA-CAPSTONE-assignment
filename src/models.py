from dataclasses import dataclass
from typing import Dict, List, Tuple


@dataclass
class Parcel:
    parcel_id: str
    destination: str
    weight: int          # Weight in kg (integer for 0/1 Knapsack DP table)
    value: int           # Priority score / delivery profit
    deadline: int        # Delivery deadline in hours
    customer_name: str = "Customer"

    @property
    def urgency_ratio(self) -> float:
        """Higher value and shorter deadline yields higher urgency."""
        return round(self.value / max(1, self.deadline), 2)


class DeliveryGraph:
    """Weighted undirected graph representing the city road network."""

    def __init__(self) -> None:
        self.adj_list: Dict[str, List[Tuple[str, float]]] = {}

    def add_edge(self, u: str, v: str, weight: float) -> None:
        if u not in self.adj_list:
            self.adj_list[u] = []
        if v not in self.adj_list:
            self.adj_list[v] = []
        self.adj_list[u].append((v, weight))
        self.adj_list[v].append((u, weight))

    def get_nodes(self) -> List[str]:
        return list(self.adj_list.keys())
