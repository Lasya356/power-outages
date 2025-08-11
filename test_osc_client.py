#!/usr/bin/env python3
"""
Simple OSC Test Client

Sends test OSC messages to verify the server is working correctly.
"""

import time
import sys
import argparse

try:
    from pythonosc.udp_client import SimpleUDPClient
except ImportError:
    print("ERROR: python-osc library not installed.")
    print("Install with: pip install python-osc")
    sys.exit(1)

def main():
    parser = argparse.ArgumentParser(description="Send test OSC messages")
    parser.add_argument("--ip", default="127.0.0.1", help="OSC server IP (default: 127.0.0.1)")
    parser.add_argument("--port", type=int, default=12345, help="OSC server port (default: 12345)")
    parser.add_argument("--count", type=int, default=10, help="Number of test messages to send (default: 10)")
    parser.add_argument("--interval", type=float, default=1.0, help="Interval between messages in seconds (default: 1.0)")
    
    args = parser.parse_args()
    
    # Create OSC client
    client = SimpleUDPClient(args.ip, args.port)
    
    print(f"Sending {args.count} test OSC messages to {args.ip}:{args.port}")
    print("Press Ctrl+C to stop...")
    
    try:
        for i in range(args.count):
            # Send different types of test messages
            timestamp = int(time.time() * 1000)  # Current time in milliseconds
            
            # Test message 1: Simple timestamp
            client.send_message("/test/timestamp", timestamp)
            print(f"Sent: /test/timestamp -> {timestamp}")
            
            # Test message 2: EmotiBit-like format
            client.send_message("/emotibit/test", timestamp, i, "test_data", 123.45)
            print(f"Sent: /emotibit/test -> {timestamp}, {i}, test_data, 123.45")
            
            # Test message 3: Another format
            client.send_message("/EB/test", timestamp, "sensor_data", 67.89)
            print(f"Sent: /EB/test -> {timestamp}, sensor_data, 67.89")
            
            time.sleep(args.interval)
            
    except KeyboardInterrupt:
        print("\nTest interrupted by user")
    
    print("Test completed!")

if __name__ == "__main__":
    main()