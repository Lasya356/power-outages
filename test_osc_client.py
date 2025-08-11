#!/usr/bin/env python3
"""
Simple OSC Client Test

This script sends test OSC messages to verify OSC communication is working.
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
    parser = argparse.ArgumentParser(description="Simple OSC Client Test")
    parser.add_argument("--ip", default="127.0.0.1", help="OSC server IP (default: 127.0.0.1)")
    parser.add_argument("--port", type=int, default=12345, help="OSC server port (default: 12345)")
    parser.add_argument("--count", type=int, default=5, help="Number of test messages to send (default: 5)")
    parser.add_argument("--interval", type=float, default=1.0, help="Interval between messages in seconds (default: 1.0)")
    
    args = parser.parse_args()
    
    # Create client
    client = SimpleUDPClient(args.ip, args.port)
    
    print(f"Sending {args.count} test messages to {args.ip}:{args.port}")
    print(f"Interval: {args.interval} seconds")
    print()
    
    try:
        for i in range(args.count):
            # Send test messages with different patterns
            timestamp = int(time.time() * 1000)  # Current timestamp in milliseconds
            
            # Test message 1: Simple timestamp
            client.send_message("/test/timestamp", [timestamp])
            print(f"Sent: /test/timestamp -> {timestamp}")
            
            # Test message 2: EmotiBit-like format
            client.send_message("/emotibit/test", [timestamp, i, "test_data", 1.23, 4.56])
            print(f"Sent: /emotibit/test -> {timestamp}, {i}, test_data, 1.23, 4.56")
            
            # Test message 3: Alternative format
            client.send_message("/EB/test", [timestamp, "sensor_data"])
            print(f"Sent: /EB/test -> {timestamp}, sensor_data")
            
            if i < args.count - 1:  # Don't sleep after last message
                time.sleep(args.interval)
        
        print(f"\nSent {args.count * 3} total test messages")
        
    except Exception as e:
        print(f"Error sending messages: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())