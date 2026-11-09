import os
import asyncio
import httpx
from typing import List, Dict, Any
from unittest.mock import patch, AsyncMock, MagicMock
import unittest

class FleetRobotManager:
    def __init__(self, max_concurrency: int = 4, bearer_token: str = None):
        self.max_concurrency = max_concurrency
        # Load bearer token from environment or parameter fallback
        self.bearer_token = bearer_token or os.getenv("API_BEARER_TOKEN", "secret-token")

    async def reboot(self, client: httpx.AsyncClient, server_id: str, url: str, semaphore: asyncio.Semaphore = None) -> dict:
        headers = {
            "Authorization": f"Bearer {self.bearer_token}",
            "Content-Type": "application/json"
        }
        payload = {"serial": server_id}

        async def _make_request():
            response = await client.post(url, json=payload, headers=headers, timeout=5.0)
            response.raise_for_status()
            data = response.json()
            if data.get("result") != "success":
                return {
                    "server_id": server_id, 
                    "status": "ERROR", 
                    "reason": data.get('reason', 'Unknown reason')
                }
            return data

        try:
            # Execute with semaphore rate-limiting if provided
            if semaphore:
                async with semaphore:
                    return await _make_request()
            else:
                return await _make_request()

        except httpx.TimeoutException:
            return {"server_id": server_id, "status": "ERROR", "reason": "Timeout error"}
        except httpx.ConnectError:
            return {"server_id": server_id, "status": "ERROR", "reason": "Connection error"}
        except httpx.HTTPStatusError as e:
            return {"server_id": server_id, "status": "ERROR", "reason": f"HTTP error: {e}"}
        except ValueError:
            return {"server_id": server_id, "status": "ERROR", "reason": "Invalid JSON response"}
        except Exception as e:
            return {"server_id": server_id, "status": "ERROR", "reason": f"Unexpected error: {e}"}
 
    async def reboot_multiple_servers(self, servers: List[str], url: str) -> List[Dict[str, Any]]:
        semaphore = asyncio.Semaphore(self.max_concurrency)
        async with httpx.AsyncClient() as client:
            tasks = [
                self.reboot(client, server_id, url, semaphore)
                for server_id in servers
            ]
            return await asyncio.gather(*tasks)

class TestFleetRobotManager(unittest.IsolatedAsyncioTestCase):

    @patch('httpx.AsyncClient.post', new_callable=AsyncMock)
    async def test_robot_success(self, mock_post):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"result": "success", "reason": "none"}
        mock_post.return_value = mock_response

        manager = FleetRobotManager()
        async with httpx.AsyncClient() as client:
            await manager.reboot(client, "server-01", "http://fake-url/reboot")
        
        # Verify call includes headers
        mock_post.assert_awaited_once_with(
            "http://fake-url/reboot", 
            json={"serial": "server-01"}, 
            headers={"Authorization": "Bearer secret-token", "Content-Type": "application/json"},
            timeout=5.0
        )

    @patch('httpx.AsyncClient.post', new_callable=AsyncMock)
    async def test_reboot_http_500_error(self, mock_post):
        from httpx import HTTPStatusError, Request, Response
        mock_response = MagicMock()
        mock_response.status_code = 500
        mock_response.raise_for_status.side_effect = HTTPStatusError(
            "500 Server Error", 
            request=Request("POST", "http://fake-url/reboot"), 
            response=mock_response
        )
        mock_post.return_value = mock_response

        manager = FleetRobotManager()
        async with httpx.AsyncClient() as client:
            result = await manager.reboot(client, "server-01", "http://fake-url/reboot")
        self.assertEqual(result["status"], "ERROR")

    @patch('httpx.AsyncClient.post', new_callable=AsyncMock)
    async def test_reboot_timeout(self, mock_post):
        from httpx import TimeoutException
        mock_post.side_effect = TimeoutException("Connection timed out")

        manager = FleetRobotManager()
        async with httpx.AsyncClient() as client:
            result = await manager.reboot(client, "server-01", "http://fake-url/reboot")
        self.assertEqual(result["status"], "ERROR")

    @patch('httpx.AsyncClient.post', new_callable=AsyncMock)
    async def test_reboot_success_returns_data(self, mock_post):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"result": "success", "reason": "reboot initiated"}
        mock_post.return_value = mock_response

        manager = FleetRobotManager()
        async with httpx.AsyncClient() as client:
            result = await manager.reboot(client, "server-01", "http://fake-url/reboot")
        
        self.assertEqual(result, {"result": "success", "reason": "reboot initiated"})
        mock_post.assert_awaited_once()

    @patch('httpx.AsyncClient.post', new_callable=AsyncMock)
    async def test_reboot_multiple_calls_all_servers(self, mock_post):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"result": "success"}
        mock_post.return_value = mock_response

        manager = FleetRobotManager(max_concurrency=2)
        servers = ["srv-A", "srv-B", "srv-C"]
        
        await manager.reboot_multiple_servers(servers, "http://fake-url/reboot")

        self.assertEqual(mock_post.await_count, 3)
        
        expected_headers = {"Authorization": "Bearer secret-token", "Content-Type": "application/json"}
        expected_calls = [
            (("http://fake-url/reboot",), {"json": {"serial": "srv-A"}, "headers": expected_headers, "timeout": 5.0}),
            (("http://fake-url/reboot",), {"json": {"serial": "srv-B"}, "headers": expected_headers, "timeout": 5.0}),
            (("http://fake-url/reboot",), {"json": {"serial": "srv-C"}, "headers": expected_headers, "timeout": 5.0}),
        ]
        
        for actual_call, expected_call in zip(mock_post.await_args_list, expected_calls):
            self.assertEqual(actual_call.args, expected_call[0])
            self.assertEqual(actual_call.kwargs, expected_call[1])

if __name__ == "__main__":
    manager = FleetRobotManager(max_concurrency=4)

    # Run unit tests
    unittest.main(argv=[''], exit=False)
    
    # Execution Demo
    async def main_demo():
        servers_to_reboot = ["server-01", "server-02", "server-03", "server-04", "server-05"]
        target_url = "http://your-fleet-controller-api.local/reboot"
        
        print(f"\nInitiating asynchronous concurrent reboot across {len(servers_to_reboot)} servers...")
        execution_results = await manager.reboot_multiple_servers(servers_to_reboot, target_url)
        print("Reboot Results Summary:", execution_results)

    asyncio.run(main_demo())
