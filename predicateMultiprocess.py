from abc import ABC
import concurrent.futures
#from concurrent.futures import ProcessPoolExecutor
from typing import List, Dict, Any

class Predicate(ABC):
    def __init__(self):
        pass
    
    def evaluate(self, row:dict):
        raise NotImplementedError

class GreaterThan(Predicate):

    def __init__(self, field: str, threshold: float | int):
        self.field = field
        self.threshold = threshold

    def evaluate(self, row:dict):
        val = row.get(self.field)
        if val is None:
            return False
        try:
            return val > self.threshold
        except TypeError:
            # Defensive handling for type mismatches (e.g. comparing str > int)
            return False

class LesserThan(Predicate):

    def __init__(self, field: str, threshold: float | int):
        self.field = field
        self.threshold = threshold

    def evaluate(self, row:dict):
        val = row.get(self.field)
        if val is None:
            return False
        try:
            return val < self.threshold
        except TypeError:
            # Defensive handling for type mismatches (e.g. comparing str > int)
            return False

class And(Predicate):

    def __init__(self, conditionList: list[Predicate]):
        self.conditionList = conditionList
    
    def evaluate(self, row:dict):
        for condition in self.conditionList:
            if not condition.evaluate(row):
                return False
        return True

class Or(Predicate):

    def __init__(self, conditionList: list[Predicate]):
        self.conditionList = conditionList
    
    def evaluate(self, row:dict):
        for condition in self.conditionList:
            if condition.evaluate(row):
                return True
        return False

def filter_chunk(chunk: list[dict[str, Any]], query_tree: Predicate) -> list[dict[str,Any]]:
    result = []
    for row in chunk:
        if query_tree.evaluate(row):
            result.append(row)
    return result

def parallel_filter_dataset(dataset: list[dict[str, Any]], query_tree: Predicate, num_workers: int = 4) -> List[Dict[str, Any]]:

    if not dataset:
        return []
    
    chunk_size = max(1, len(dataset) // num_workers)
    chunks = []

    for i in range(0, len(dataset), chunk_size):
        chunks.append(dataset[i:i+chunk_size])
    
    filtered_results = []
    futures = []

    with concurrent.futures.ProcessPoolExecutor(max_workers = num_workers) as executor:
        for chunk in chunks:
            future = executor.submit(filter_chunk, chunk, query_tree)
            futures.append(future)

        for future in concurrent.futures.as_completed(futures):
            filtered_results.extend(future.result())
    
    return filtered_results


if __name__ == "__main__":
    # Construct a query: (accuracy > 0.90) AND (loss < 0.05)
    query = And([
        GreaterThan("accuracy", 0.90),
        LesserThan("loss", 0.05)
    ])

    dataset = [
        {"run_id": "exp_1", "accuracy": 0.95, "loss": 0.03},  # Match
        {"run_id": "exp_2", "accuracy": 0.85, "loss": 0.02},  # Fails accuracy
        {"run_id": "exp_3", "accuracy": 0.92, "loss": 0.08},  # Fails loss
        {"run_id": "exp_4", "accuracy": 0.98, "loss": 0.01},  # Match
    ]

    results = parallel_filter_dataset(dataset, query, num_workers=2)
    print("Filtered Matching Runs:", results)
