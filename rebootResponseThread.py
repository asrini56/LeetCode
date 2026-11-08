import os
import sys
import json
import time
import argparse
import logging
from dataclasses import dataclass
from typing import List, Optional
import requests
from concurrent.futures import ThreadPoolExecutor, as_completed
from flask import Flask, request, jsonify
import threading

# Configure structured logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

# ==========================================
# 1. FLASK BACKEND SERVER (Your App)
# ==========================================
app = Flask(__name__)

# Load bearer token from environment or use test default
API_BEARER_TOKEN = os.getenv("API_BEARER_TOKEN", "secret-token-42")


@app.route("/api/health", methods=["GET"])
def health():
    return {"status": "ok"}


@app.route("/api/reboot", methods=["POST"])
def reboot_server():
    # 1. Validate Authorization header
    auth_header = request.headers.get("Authorization", "")
    if not auth_header.startswith("Bearer ") or auth_header.split(" ")[1] != API_BEARER_TOKEN:
        return jsonify({"status": "UNAUTHORIZED", "message": "Invalid or missing bearer token"}), 401

    # 2. Validate Content-Type and JSON payload
    if not request.is_json:
        return jsonify({"status": "BAD_REQUEST", "message": "Content-Type must be application/json"}), 400

    data = request.get_json()
    serial = data.get("serial")

    if not serial:
        return jsonify({"status": "BAD_REQUEST", "message": "Missing 'serial' field in payload"}), 400

    # 3. Simulate failure injection based on serial naming for testing client resilience
    if "timeout" in serial:
        time.sleep(3.0)  # Forces a client timeout
    if "server-error" in serial:
        return jsonify({"status": "ERROR", "message": "Hardware controller fault"}), 500
    if "malformed" in serial:
        # Returns invalid content type/string to test client JSON decoding safety
        return "<html>502 Bad Gateway</html>", 200, {'Content-Type': 'text/html'}

    # 4. Successful execution path
    return jsonify({
        "serial": serial,
        "status": "SUCCESS",
        "message": f"Server {serial} reboot signal dispatched successfully."
    }), 200


# ==========================================
# 2. CLIENT & DATA STRUCTURE COMPONENTS
# ==========================================
@dataclass
class RebootResponse:
    serial: str
    status: str       # SUCCESS, TIMEOUT, CONNECTION_ERROR, HTTP_ERROR, MALFORMED_JSON
    message: Optional[str] = None


class FleetClient:
    def __init__(self, endpoint: str, token: str, timeout: float = 2.0):
        self.endpoint = endpoint
        self.headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }
        self.timeout = timeout

    def reboot_server(self, serial: str) -> RebootResponse:
        payload = {"serial": serial}
        try:
            response = requests.post(
                self.endpoint,
                json=payload,
                headers=self.headers,
                timeout=self.timeout
            )
            
            # Isolate server-side error statuses without crashing
            if response.status_code >= 500:
                return RebootResponse(
                    serial=serial, 
                    status="HTTP_ERROR", 
                    message=f"Server returned HTTP {response.status_code}"
                )
            
            response.raise_for_status()
            
            # Guard against non-JSON payloads or broken responses
            data = response.json()
            return RebootResponse(
                serial=serial,
                status=data.get("status", "SUCCESS"),
                message=data.get("message")
            )

        except requests.exceptions.Timeout:
            return RebootResponse(
                serial=serial, 
                status="TIMEOUT", 
                message=f"Request exceeded timeout limit of {self.timeout}s"
            )
        except requests.exceptions.ConnectionError:
            return RebootResponse(
                serial=serial, 
                status="CONNECTION_ERROR", 
                message="Failed to establish connection to backend"
            )
        except requests.exceptions.HTTPError as e:
            return RebootResponse(
                serial=serial, 
                status="HTTP_ERROR", 
                message=str(e)
            )
        except json.JSONDecodeError:
            return RebootResponse(
                serial=serial, 
                status="MALFORMED_JSON", 
                message="Response body contained invalid or non-JSON data"
            )
        except Exception as e:
            return RebootResponse(
                serial=serial, 
                status="UNKNOWN_ERROR", 
                message=str(e)
            )


# ==========================================
# 3. CLI ARGUMENT & STDIN PARSING
# ==========================================
def parse_serials() -> List[str]:
    """Reads serial numbers from command-line arguments or piped stdin."""
    serials = []
    if not sys.stdin.isatty():
        for line in sys.stdin:
            cleaned = line.strip()
            if cleaned:
                serials.append(cleaned)
    else:
        parser = argparse.ArgumentParser(description="Fleet Reboot Tool")
        parser.add_argument("serials", nargs="*", help="Server serial numbers")
        args = parser.parse_args()
        serials = args.serials
    return serials


# ==========================================
# 4. EXECUTION HARNESS
# ==========================================
def main():
    serials = parse_serials()
    if not serials:
        # Default test payload covering success, timeout, server error, and malformed JSON
        serials = ["node-01", "node-02", "timeout-node-03", "server-error-node-04", "malformed-node-05"]
        logging.info("No inputs supplied via arguments or stdin. Running default test batch...")

    endpoint = "http://127.0.0.1:5000/api/reboot"
    token = API_BEARER_TOKEN
    client = FleetClient(endpoint=endpoint, token=token, timeout=1.5)

    logging.info(f"Initiating concurrent fleet reboot across {len(serials)} servers using ThreadPoolExecutor...")

    has_failures = False

    # Bounded parallel execution avoiding the asyncio+requests event loop block
    with ThreadPoolExecutor(max_workers=4) as executor:
        future_to_serial = {
            executor.submit(client.reboot_server, serial): serial 
            for serial in serials
        }

        for future in as_completed(future_to_serial):
            result = future.result()
            if result.status == "SUCCESS":
                logging.info(f"[SUCCESS] Server {result.serial}: {result.message}")
            else:
                logging.error(f"[{result.status}] Server {result.serial}: {result.message}")
                has_failures = True

    # Return proper Unix exit codes for automation/CI
    if has_failures:
        sys.exit(1)
    sys.exit(0)


if __name__ == "__main__":
    # Spin up the Flask server in a background daemon thread for self-contained testing
    server_thread = threading.Thread(
        target=lambda: app.run(host="0.0.0.0", port=5000, debug=False, use_reloader=False), 
        daemon=True
    )
    server_thread.start()
    time.sleep(0.5)  # Allow socket to bind cleanly

    main()
