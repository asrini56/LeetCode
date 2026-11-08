import asyncio
import time

async def check_node_health(node_id: str, endpoint: str, semaphore: asyncio.Semaphore, timeout: float = 2.0) -> dict:
    async with semaphore:
        try:
            async def _mock_network_call():
                # Simulate variable network latency / processing delay
                await asyncio.sleep(0.5)
                if "fail" in node_id:
                    raise ConnectionError("Node unreachable")
                if "hang" in node_id:
                    await asyncio.sleep(3.0)  # Will trigger timeout
                return {"cpu_load": 42.5, "gpu_temp": 71.0}
            
            # Must call the coroutine () and await it inside wait_for
            data = await asyncio.wait_for(_mock_network_call(), timeout=timeout)

            return {
                "node_id": node_id,
                "status": "SUCCESS",
                "metrics": data
            }
        except asyncio.TimeoutError:
            return {
                "node_id": node_id,
                "status": "ERROR",
                "error": "Request timed out"
            }
        except Exception as e:
            return {
                "node_id": node_id,
                "status": "ERROR",
                "error": str(e)
            }

async def poll_fleet_cluster(nodes: list[dict], max_concurrency: int) -> list[dict]:
    semaphore = asyncio.Semaphore(max_concurrency)
    timeout = 1.5
    endpoint = "fakeendpoint"
    
    # Create coroutine objects for each node
    tasks = [
        check_node_health(node["node_id"], endpoint, semaphore, timeout) 
        for node in nodes
    ]
    
    # Execute all tasks concurrently and gather their results
    results = await asyncio.gather(*tasks)
    return results

if __name__ == "__main__":
    cluster_nodes = [
        {"node_id": "gpu-node-01"},
        {"node_id": "gpu-node-02-fail"},
        {"node_id": "gpu-node-03-hang"},
        {"node_id": "gpu-node-04"}
    ]

    start_time = time.time()
    loop_results = asyncio.run(poll_fleet_cluster(cluster_nodes, max_concurrency=2))
    duration = time.time() - start_time

    print(f"\nCompleted cluster health check in {duration:.2f} seconds.")
    for res in loop_results:
        print(res)
