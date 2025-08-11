#!/usr/bin/env python3
"""
Simple OSC Server Test

This script creates a basic OSC server to test if OSC communication is working.
"""

import time
import sys
import argparse
import logging
from datetime import datetime

try:
    from pythonosc import dispatcher, osc_server
    from pythonosc.udp_client import SimpleUDPClient
except ImportError:
    print("ERROR: python-osc library not installed.")
    print("Install with: pip install python-osc")
    sys.exit(1)

def handle_any_message(address, *args):
    """Handle any OSC message"""
    timestamp = datetime.now().strftime("%H:%M:%S.%f")[:-3]
    print(f"[{timestamp}] OSC: {address} -> {args}")

def main():
    parser = argparse.ArgumentParser(description="Simple OSC Server Test")
    parser.add_argument("--ip", default="127.0.0.1", help="OSC server IP (default: 127.0.0.1)")
    parser.add_argument("--port", type=int, default=12345, help="OSC server port (default: 12345)")
    parser.add_argument("--verbose", "-v", action="store_true", help="Enable verbose logging")
    
    args = parser.parse_args()
    
    if args.verbose:
        logging.basicConfig(level=logging.DEBUG)
    
    # Setup dispatcher
    disp = dispatcher.Dispatcher()
    disp.map("/*", handle_any_message)  # Catch all messages
    
    print(f"Starting OSC server on {args.ip}:{args.port}")
    print("Send any OSC message to test...")
    print("Press Ctrl+C to stop\n")
    
    try:
        # Create server
        server = osc_server.ThreadingOSCUDPServer((args.ip, args.port), disp)
        
        # Start server
        server.serve_forever()
        
    except KeyboardInterrupt:
        print("\nServer stopped by user")
    except Exception as e:
        print(f"Error: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())