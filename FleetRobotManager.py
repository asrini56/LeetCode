import requests
import concurrent.futures
from unittest.mock import patch, MagicMock
import unittest

class FleetRobotManager:
    def __init__(self, max_threads: int = 4):
        self.max_threads = max_threads

    def reboot(self,server_id, url):
        try:
            payload = {"serial": server_id}
            response = requests.post(url, json=payload, timeout=5.0)
            response.raise_for_status()
            data = response.json()
            if data.get("result") != "success":
                print(f"Reboot failed for {server_id}: {data.get('reason', 'Unknown reason')}")
                return None
            else:
                print(f"Successfully rebooted {server_id}")
                return data

        except requests.exceptions.Timeout:
            print(f"Timeout error while trying to reboot {server_id}")
        except requests.exceptions.ConnectionError:
            print(f"Connection error: Could not reach server {server_id}")
        except requests.exceptions.HTTPError as e:
            print(f"HTTP error for {server_id}: {e}")
        except ValueError:
            print(f"Invalid JSON response received from {server_id}")
        except Exception as e:
            print(f"Unexpected error for {server_id}: {e}")
    
    def reboot_multiple_servers(self, servers, url):
        with concurrent.futures.ThreadPoolExecutor(max_workers=self.max_threads) as executor:
            for server_id in servers:
                executor.submit(self.reboot, server_id, url)

class TestFleetRobotManager(unittest.TestCase):

    @patch('requests.post')
    def test_robot_success(self, mock_post):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"result": "success", "reason": "none"}
        mock_post.return_value = mock_response

        manager = FleetRobotManager()
        # Act & Assert (should not raise an exception)
        manager.reboot("server-01", "http://fake-url/reboot")
        mock_post.assert_called_once_with("http://fake-url/reboot", json={"serial": "server-01"}, timeout=5.0)

    @patch('requests.post')
    def test_reboot_http_500_error(self, mock_post):
        # Arrange
        from requests.exceptions import HTTPError
        mock_response = MagicMock()
        mock_response.raise_for_status.side_effect = HTTPError("500 Server Error")
        mock_post.return_value = mock_response

        manager = FleetRobotManager()
        
        # Act (should catch the exception gracefully and print/log the error)
        manager.reboot("server-01", "http://fake-url/reboot")
    
    @patch('requests.post')
    def test_reboot_timeout(self, mock_post):
        # Arrange
        from requests.exceptions import Timeout
        mock_post.side_effect = Timeout("Connection timed out")

        manager = FleetRobotManager()
        
        # Act (should catch the timeout cleanly)
        manager.reboot("server-01", "http://fake-url/reboot")

    @patch('requests.post')
    def test_reboot_success_returns_data(self, mock_post):
        # Arrange
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"result": "success", "reason": "reboot initiated"}
        mock_post.return_value = mock_response

        manager = FleetRobotManager()
        
        # Act
        result = manager.reboot("server-01", "http://fake-url/reboot")
        
        # Assert
        self.assertEqual(result, {"result": "success", "reason": "reboot initiated"})
        mock_post.assert_called_once()

    @patch('requests.post')
    def test_reboot_multiple_calls_all_servers(self, mock_post):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"result": "success"}
        mock_post.return_value = mock_response

        manager = FleetRobotManager(max_threads=2)
        servers = ["srv-A", "srv-B", "srv-C"]
        
        manager.reboot_multiple_servers(servers, "http://fake-url/reboot")

        # Verify requests.post was called exactly once for each server
        self.assertEqual(mock_post.call_count, 3)
        
        # Verify the correct payloads were passed across the threads
        expected_calls = [
            (("http://fake-url/reboot",), {"json": {"serial": "srv-A"}, "timeout": 5.0}),
            (("http://fake-url/reboot",), {"json": {"serial": "srv-B"}, "timeout": 5.0}),
            (("http://fake-url/reboot",), {"json": {"serial": "srv-C"}, "timeout": 5.0}),
        ]
        # mock_post.call_args_list holds every call made across the threads
        for actual_call, expected_call in zip(mock_post.call_args_list, expected_calls):
            self.assertEqual(actual_call[0], expected_call[0])
            self.assertEqual(actual_call[1], expected_call[1])

if __name__ == "__main__":
    # Initialize the manager with a max worker thread limit
    manager = FleetRobotManager(max_threads=4)

    unittest.main(argv=[''], exit=False)
    
    # Define your target servers and API endpoint
    servers_to_reboot = ["server-01", "server-02", "server-03", "server-04", "server-05"]
    target_url = "http://your-fleet-controller-api.local/reboot"
    
    print(f"Initiating concurrent reboot across {len(servers_to_reboot)} servers...")
    manager.reboot_multiple_servers(servers_to_reboot, target_url)

