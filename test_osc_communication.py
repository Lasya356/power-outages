#!/usr/bin/env python3
"""
Test OSC Communication

This script tests OSC communication by running a server and client in sequence.
"""

import time
import sys
import threading
import subprocess

try:
    from pythonosc import dispatcher, osc_server
    from pythonosc.udp_client import SimpleUDPClient
except ImportError:
    print("ERROR: python-osc library not installed.")
    print("Install with: pip install python-osc")
    sys.exit(1)

def handle_message(address, *args):
    """Handle OSC messages"""
    timestamp = time.strftime("%H:%M:%S")
    print(f"[{timestamp}] Received: {address} -> {args}")

def run_server():
    """Run OSC server"""
    disp = dispatcher.Dispatcher()
    disp.map("/*", handle_message)
    
    server = osc_server.ThreadingOSCUDPServer(("127.0.0.1", 12345), disp)
    print("OSC Server started on 127.0.0.1:12345")
    server.serve_forever()

def run_client():
    """Run OSC client"""
    time.sleep(1)  # Wait for server to start
    
    client = SimpleUDPClient("127.0.0.1", 12345)
    
    print("Sending test messages...")
    
    # Send test messages
    timestamp = int(time.time() * 1000)
    
    client.send_message("/test/1", [timestamp])
    time.sleep(0.1)
    
    client.send_message("/emotibit/test", [timestamp, 1, "test_data", 1.23])
    time.sleep(0.1)
    
    client.send_message("/EB/test", [timestamp, "sensor_data"])
    time.sleep(0.1)
    
    print("Test messages sent!")

def main():
    print("Testing OSC Communication...")
    print("=" * 40)
    
    # Start server in background thread
    server_thread = threading.Thread(target=run_server, daemon=True)
    server_thread.start()
    
    # Run client
    run_client()
    
    # Wait a bit for messages to be processed
    time.sleep(1)
    
    print("=" * 40)
    print("OSC Communication test completed!")

if __name__ == "__main__":
    main()