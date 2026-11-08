import collections
from typing import BinaryIO
import threading
import concurrent.futures
import io


class ChunkStreamProcessor:
    """
    A concurrent, thread-safe chunk stream processor with out-of-order 
    reordering, telemetry, and context manager support.
    """
    def __init__(self, stream: BinaryIO, chunk_size: int = 4 * 1024 * 1024, max_workers: int = 4):
        self.stream = stream
        self.chunk_size = chunk_size
        self.max_workers = max_workers
        self.lock = threading.Lock()
        self.completed_chunks = 0
        self.bytes_processed = 0
        self.total_chunks = 0
        self.chunks = {}  # Fixed from defaultdict()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.stream and hasattr(self.stream, "close"):
            self.stream.close()
    
    def read_chunks(self) -> None:
        chunk_index = 0
        while True:
            data = self.stream.read(self.chunk_size)
            if not data:
                break
            self.chunks[chunk_index] = data
            chunk_index += 1
            self.total_chunks += 1
    
    def process_single_chunk(self, chunk_index: int, data: bytes) -> tuple:
        processed_data = data  # Placeholder for transform/processing logic
        with self.lock:
            self.bytes_processed += len(data)
            self.completed_chunks += 1
        return (chunk_index, processed_data)
    
    def process_stream(self):
        self.read_chunks()
        if self.total_chunks == 0:
            return

        results_buffer = {}
        next_to_yield = 0
        future_to_index = {}

        with concurrent.futures.ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            for idx in self.chunks:
                data = self.chunks[idx]
                future = executor.submit(self.process_single_chunk, idx, data)
                future_to_index[future] = idx
            
            for future in concurrent.futures.as_completed(future_to_index):
                idx, processed_data = future.result()
                results_buffer[idx] = processed_data
            
                while next_to_yield in results_buffer:
                    yield next_to_yield, results_buffer.pop(next_to_yield)
                    next_to_yield += 1


# --- Test Harness Using Context Manager ---
mock_data = b"Hello CoreWeave! " * (1 * 1024 * 1024)  # ~17MB of data
stream = io.BytesIO(mock_data)

# Using 'with' ensures self.stream is cleaned up properly via __exit__
with ChunkStreamProcessor(stream, chunk_size=2 * 1024 * 1024, max_workers=4) as processor:
    print("Starting stream processing...")
    total_bytes_received = 0

    for chunk_idx, chunk_data in processor.process_stream():
        total_bytes_received += len(chunk_data)

    print(f"\nProcessing complete! Total bytes received: {total_bytes_received}")
    print(f"Final Telemetry: {processor.completed_chunks} chunks completed.")
