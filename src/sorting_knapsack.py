from typing import List, Tuple
from src.models import Parcel


def merge_sort_parcels(parcels: List[Parcel], key_fn=None) -> List[Parcel]:
    """
    Sorts parcels in O(N log N) time using Merge Sort.
    Default order: Earliest deadline first, then highest priority value.
    """
    if key_fn is None:
        key_fn = lambda p: (p.deadline, -p.value)

    if len(parcels) <= 1:
        return parcels

    mid = len(parcels) // 2
    left = merge_sort_parcels(parcels[:mid], key_fn)
    right = merge_sort_parcels(parcels[mid:], key_fn)

    return _merge(left, right, key_fn)


def _merge(left: List[Parcel], right: List[Parcel], key_fn) -> List[Parcel]:
    sorted_list = []
    i = j = 0
    while i < len(left) and j < len(right):
        if key_fn(left[i]) <= key_fn(right[j]):
            sorted_list.append(left[i])
            i += 1
        else:
            sorted_list.append(right[j])
            j += 1
    sorted_list.extend(left[i:])
    sorted_list.extend(right[j:])
    return sorted_list


def optimize_van_loading_dp(
    parcels: List[Parcel], max_capacity: int
) -> Tuple[int, List[Parcel], List[List[int]]]:
    """
    Solves the 0/1 Knapsack problem using Bottom-Up Dynamic Programming.
    Time Complexity: O(N * W) | Space Complexity: O(N * W)
    Returns: (max_priority_value, selected_parcels, dp_table)
    """
    n = len(parcels)
    dp = [[0 for _ in range(max_capacity + 1)] for _ in range(n + 1)]

    for i in range(1, n + 1):
        p = parcels[i - 1]
        for w in range(max_capacity + 1):
            if p.weight <= w:
                dp[i][w] = max(dp[i - 1][w], dp[i - 1][w - p.weight] + p.value)
            else:
                dp[i][w] = dp[i - 1][w]

    # Backtrack to find selected parcels
    selected_parcels: List[Parcel] = []
    w = max_capacity
    for i in range(n, 0, -1):
        if dp[i][w] != dp[i - 1][w]:
            selected_parcel = parcels[i - 1]
            selected_parcels.append(selected_parcel)
            w -= selected_parcel.weight

    selected_parcels.reverse()
    return dp[n][max_capacity], selected_parcels, dp
