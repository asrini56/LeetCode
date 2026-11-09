import os
import asyncio
import concurrent.futures
import requests
from typing import List, Dict, Any
from unittest.mock import patch, MagicMock
import unittest

class FleetRobotManager:
    def __init__(self, max_concurrency: int = 4, bearer_token: str = None):
        self.max_concurrency = max_concurrency
        # Load bearer token from environment or parameter fallback
        self.bearer_token = bearer_token or os.getenv("API_BEARER_TOKEN", "secret-token")

    def _reboot_sync(self, server_id: str, url: str) -> dict:
        """Synchronous helper method that executes the blocking requests call."""
        headers = {
            "Authorization": f"Bearer {self.bearer_token}",
            "Content-Type": "application/json"
        }
        try:
            payload = {"serial": server_id}
            response = requests.post(url, json=payload, headers=headers, timeout=5.0)
            response.raise_for_status()
            data = response.json()
            if data.get("result") != "success":
                return {
                    "server_id": server_id, 
                    "status": "ERROR", 
                    "reason": data.get('reason', 'Unknown reason')
                }
            return data

        except requests.exceptions.Timeout:
            return {"server_id": server_id, "status": "ERROR", "reason": "Timeout error"}
        except requests.exceptions.ConnectionError:
            return {"server_id": server_id, "status": "ERROR", "reason": "Connection error"}
        except requests.exceptions.HTTPError as e:
            return {"server_id": server_id, "status": "ERROR", "reason": f"HTTP error: {e}"}
        except ValueError:
            return {"server_id": server_id, "status": "ERROR", "reason": "Invalid JSON response"}
        except Exception as e:
            return {"server_id": server_id, "status": "ERROR", "reason": f"Unexpected error: {e}"}

    async def reboot(self, server_id: str, url: str, semaphore: asyncio.Semaphore = None) -> dict:
        """Asynchronous wrapper that offloads the blocking request to a worker thread pool, 
        controlled by a semaphore for concurrency limits."""
        async def _run_with_semaphore():
            if semaphore:
                async with semaphore:
                    # Offload the blocking requests call to a separate thread
                    return await asyncio.to_thread(self._reboot_sync, server_id, url)
            else:
                return await asyncio.to_thread(self._reboot_sync, server_id, url)

        return await _run_with_semaphore()
     
    async def reboot_multiple_servers(self, servers: List[str], url: str) -> List[Dict[str, Any]]:
        semaphore = asyncio.Semaphore(self.max_concurrency)
        tasks = [
            self.reboot(server_id, url, semaphore)
            for server_id in servers
        ]
        return await asyncio.gather(*tasks)

class TestFleetRobotManager(unittest.IsolatedAsyncioTestCase):

    @patch('requests.post')
    async def test_robot_success(self, mock_post):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"result": "success", "reason": "none"}
        mock_post.return_value = mock_response

        manager = FleetRobotManager()
        await manager.reboot("server-01", "http://fake-url/reboot")
        
        # Verify call includes headers
        mock_post.assert_called_once_with(
            "http://fake-url/reboot", 
            json={"serial": "server-01"}, 
            headers={"Authorization": "Bearer secret-token", "Content-Type": "application/json"},
            timeout=5.0
        )

    @patch('requests.post')
    async def test_reboot_http_500_error(self, mock_post):
        from requests.exceptions import HTTPError
        mock_response = MagicMock()
        mock_response.raise_for_status.side_effect = HTTPError("500 Server Error")
        mock_post.return_value = mock_response

        manager = FleetRobotManager()
        result = await manager.reboot("server-01", "http://fake-url/reboot")
        self.assertEqual(result["status"], "ERROR")

    @patch('requests.post')
    async def test_reboot_timeout(self, mock_post):
        from requests.exceptions import Timeout
        mock_post.side_effect = Timeout("Connection timed out")

        manager = FleetRobotManager()
        result = await manager.reboot("server-01", "http://fake-url/reboot")
        self.assertEqual(result["status"], "ERROR")

    @patch('requests.post')
    async def test_reboot_success_returns_data(self, mock_post):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"result": "success", "reason": "reboot initiated"}
        mock_post.return_value = mock_response

        manager = FleetRobotManager()
        result = await manager.reboot("server-01", "http://fake-url/reboot")
        
        self.assertEqual(result, {"result": "success", "reason": "reboot initiated"})
        mock_post.assert_called_once()

    @patch('requests.post')
    async def test_reboot_multiple_calls_all_servers(self, mock_post):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"result": "success"}
        mock_post.return_value = mock_response

        manager = FleetRobotManager(max_concurrency=2)
        servers = ["srv-A", "srv-B", "srv-C"]
        
        await manager.reboot_multiple_servers(servers, "http://fake-url/reboot")

        self.assertEqual(mock_post.call_count, 3)
        
        expected_headers = {"Authorization": "Bearer secret-token", "Content-Type": "application/json"}
        expected_calls = [
            (("http://fake-url/reboot",), {"json": {"serial": "srv-A"}, "headers": expected_headers, "timeout": 5.0}),
            (("http://fake-url/reboot",), {"json": {"serial": "srv-B"}, "headers": expected_headers, "timeout": 5.0}),
            (("http://fake-url/reboot",), {"json": {"serial": "srv-C"}, "headers": expected_headers, "timeout": 5.0}),
        ]
        
        for actual_call, expected_call in zip(mock_post.call_args_list, expected_calls):
            self.assertEqual(actual_call[0], expected_call[0])
            self.assertEqual(actual_call[1], expected_call[1])

if __name__ == "__main__":
    manager = FleetRobotManager(max_concurrency=4)

    # Run unit tests via unittest
    unittest.main(argv=[''], exit=False)
    
    # Execution Demo
    async def main_demo():
        servers_to_reboot = ["server-01", "server-02", "server-03", "server-04", "server-05"]
        target_url = "http://your-fleet-controller-api.local/reboot"
        
        print(f"\nInitiating asynchronous concurrent reboot with requests across {len(servers_to_reboot)} servers...")
        execution_results = await manager.reboot_multiple_servers(servers_to_reboot, target_url)
        print("Reboot Results Summary:", execution_results)

    asyncio.run(main_demo())
