from heapq import heappush, heappop

def maximizeShipmentOrder(shipmentOrder, windowSize):
    a, k = shipmentOrder, windowSize
    stack, heap = [], []
    best_changed, best_start = -1, 0

    for right, value in enumerate(a):
        while stack and a[stack[-1]] > value:
            heappush(heap, stack.pop())
        stack.append(right)

        left = right - k + 1
        if left < 0:
            continue
        while heap and heap[0] < left:
            heappop(heap)
        if not heap:
            return list(a)

        if heap[0] > best_changed:
            best_changed = heap[0]
            best_start = left

    return (list(a[:best_start])
            + sorted(a[best_start:best_start + k])
            + list(a[best_start + k:]))
