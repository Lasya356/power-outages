#!/usr/bin/env python3
"""
EmotiBit OSC Timestamp Validation Script

Receives OSC stream from EmotiBit Oscilloscope and validates timestamps
to detect PTP synchronization failures (timestamps starting from 0).
"""

import time
import sys
import argparse
import logging
import threading
from datetime import datetime

try:
    from pythonosc import dispatcher, osc_server
    from pythonosc.udp_client import SimpleUDPClient
except ImportError:
    print("ERROR: python-osc library not installed.")
    print("Install with: pip install python-osc")
    sys.exit(1)

class EmotiBitOSCValidator:
    def __init__(self, osc_ip="127.0.0.1", osc_port=12345, settle_time=20):
        """
        Initialize the EmotiBit OSC validator
        
        Args:
            osc_ip (str): IP address to listen for OSC messages
            osc_port (int): Port to listen for OSC messages  
            settle_time (int): Time to wait before checking (seconds)
        """
        self.osc_ip = osc_ip
        self.osc_port = osc_port
        self.settle_time = settle_time
        
        # Validation state
        self.is_running = False
        self.settle_complete = False
        self.sync_failure_detected = False
        self.data_received = False
        
        # Statistics
        self.total_messages = 0
        self.valid_timestamps = 0
        self.invalid_timestamps = 0
        self.first_invalid = None
        
        # Debug info
        self.message_samples = []
        self.max_samples = 10
        
        # Setup logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger(__name__)
        
        # Setup OSC dispatcher
        self.dispatcher = dispatcher.Dispatcher()
        self.setup_osc_handlers()
    
    def setup_osc_handlers(self):
        """Setup OSC message handlers for EmotiBit data"""
        # Add handlers for different EmotiBit data types
        # EmotiBit typically uses these OSC address patterns:
        self.dispatcher.map("/emotibit/*", self.handle_emotibit_message)
        self.dispatcher.map("/EB/*", self.handle_emotibit_message)
        self.dispatcher.map("/EmotiBit/*", self.handle_emotibit_message)
        self.dispatcher.map("/emotibit", self.handle_emotibit_message)
        self.dispatcher.map("/EB", self.handle_emotibit_message)
        self.dispatcher.map("/EmotiBit", self.handle_emotibit_message)
        
        # Catch-all handler for debugging - this will catch ANY OSC message
        self.dispatcher.set_default_handler(self.handle_any_message)
    
    def handle_emotibit_message(self, address, *args):
        """Handle EmotiBit OSC messages"""
        if not self.settle_complete:
            return
        
        self.data_received = True
        self.total_messages += 1
        
        # Store sample messages for debugging
        if len(self.message_samples) < self.max_samples:
            self.message_samples.append({
                'address': address,
                'args': args,
                'time': datetime.now()
            })
        
        # Log first few messages to understand format
        if self.total_messages <= 5:
            self.logger.info(f"📨 OSC Message #{self.total_messages}: {address} -> {args}")
        
        # Look for timestamp in the message
        # EmotiBit typically sends: timestamp, packet_number, data_type, values...
        if len(args) >= 1:
            try:
                timestamp = args[0]
                if isinstance(timestamp, (int, float)):
                    timestamp_int = int(timestamp)
                    self.validate_timestamp(timestamp_int, address, args)
            except (ValueError, TypeError):
                # Skip non-numeric timestamps
                pass
    
    def handle_any_message(self, address, *args):
        """Handle any OSC message for debugging"""
        if not self.settle_complete:
            return
            
        self.data_received = True
        self.total_messages += 1
        
        # Store sample messages for debugging
        if len(self.message_samples) < self.max_samples:
            self.message_samples.append({
                'address': address,
                'args': args,
                'time': datetime.now()
            })
        
        # Log first few messages to help identify the correct format
        if self.total_messages <= 5:
            self.logger.info(f"📨 OSC Message #{self.total_messages}: {address} -> {args}")
        
        # Try to extract timestamp from any position in the message
        for i, arg in enumerate(args):
            try:
                if isinstance(arg, (int, float)):
                    timestamp_int = int(arg)
                    # Check if this looks like a timestamp (reasonable range)
                    if timestamp_int > 1000000000:  # Unix timestamp
                        self.validate_timestamp(timestamp_int, address, args)
                        break
                    elif timestamp_int > 1000:  # Could be milliseconds or other format
                        self.validate_timestamp(timestamp_int, address, args)
                        break
            except (ValueError, TypeError):
                continue
    
    def validate_timestamp(self, timestamp_int, address, full_message):
        """Validate a single timestamp"""
        # Check if timestamp starts from 0 (sync failure)
        if timestamp_int == 0 or timestamp_int < 100:
            self.invalid_timestamps += 1
            self.sync_failure_detected = True
            
            if self.first_invalid is None:
                self.first_invalid = {
                    'timestamp': timestamp_int,
                    'address': address,
                    'message': full_message,
                    'time': datetime.now()
                }
            
            self.logger.error(f"❌ SYNC FAILURE: Timestamp {timestamp_int} at {address}")
            self.logger.error(f"Full message: {full_message}")
            
            # Stop validation on first failure
            self.stop_validation()
            
        else:
            self.valid_timestamps += 1
            
            # Log progress every 100 valid timestamps
            if self.valid_timestamps % 100 == 0:
                self.logger.info(f"✓ Validated {self.valid_timestamps} timestamps")
    
    def wait_for_settle(self):
        """Wait for settle time in separate thread"""
        def settle_thread():
            if self.settle_time > 0:
                self.logger.info(f"Waiting {self.settle_time} seconds for EmotiBit to settle and sync...")
                for i in range(self.settle_time):
                    if not self.is_running:
                        return
                    remaining = self.settle_time - i
                    print(f"\rSettling... {remaining} seconds remaining", end="", flush=True)
                    time.sleep(1)
                print()  # New line after countdown
            
            self.settle_complete = True
            self.logger.info("Settle time complete. Starting timestamp validation...")
            self.logger.info(f"Listening for OSC messages on {self.osc_ip}:{self.osc_port}")
            self.logger.info("Enable OSC output in EmotiBit Oscilloscope and start streaming...")
        
        threading.Thread(target=settle_thread, daemon=True).start()
    
    def run_validation(self, duration=60):
        """
        Run OSC validation for specified duration
        
        Args:
            duration (int): How long to run validation in seconds (0 = indefinite)
        """
        self.logger.info("=== EmotiBit OSC Timestamp Validation Started ===")
        self.is_running = True
        
        # Start settle timer
        self.wait_for_settle()
        
        try:
            # Setup OSC server
            server = osc_server.ThreadingOSCUDPServer(
                (self.osc_ip, self.osc_port), self.dispatcher
            )
            
            self.logger.info(f"OSC server listening on {self.osc_ip}:{self.osc_port}")
            
            # Start server in background
            server_thread = threading.Thread(target=server.serve_forever, daemon=True)
            server_thread.start()
            
            # Run for specified duration or until failure
            start_time = time.time()
            while self.is_running:
                current_time = time.time()
                elapsed = current_time - start_time
                
                # Check if we should stop
                if duration > 0 and elapsed >= duration:
                    self.logger.info(f"Validation completed after {duration} seconds")
                    break
                
                if self.sync_failure_detected:
                    break
                
                # Show periodic status
                if self.settle_complete and elapsed > 0 and int(elapsed) % 10 == 0:
                    if self.data_received:
                        self.logger.info(f"Status: {self.valid_timestamps} valid timestamps after {int(elapsed)}s")
                    else:
                        self.logger.warning("No OSC data received yet - check EmotiBit Oscilloscope OSC output")
                
                time.sleep(1)
            
            server.shutdown()
            
        except KeyboardInterrupt:
            self.logger.info("Validation interrupted by user")
        except Exception as e:
            self.logger.error(f"Error during validation: {e}")
            return False
        
        return self.print_results()
    
    def stop_validation(self):
        """Stop the validation process"""
        self.is_running = False
    
    def print_results(self):
        """Print validation results and return success status"""
        self.logger.info("\n" + "="*60)
        self.logger.info("VALIDATION RESULTS")
        self.logger.info("="*60)
        
        self.logger.info(f"Total OSC messages processed: {self.total_messages}")
        self.logger.info(f"Valid timestamps: {self.valid_timestamps}")
        self.logger.info(f"Invalid timestamps: {self.invalid_timestamps}")
        
        if not self.data_received:
            self.logger.error("❌ NO DATA RECEIVED")
            self.logger.error("Make sure EmotiBit Oscilloscope OSC output is enabled and configured correctly")
            self.logger.error("\nTROUBLESHOOTING:")
            self.logger.error("1. Check that EmotiBit Oscilloscope is running")
            self.logger.error("2. Verify OSC output is enabled in EmotiBit Oscilloscope")
            self.logger.error("3. Confirm OSC is configured to send to: " + self.osc_ip + ":" + str(self.osc_port))
            self.logger.error("4. Check firewall settings")
            self.logger.error("5. Try using '0.0.0.0' instead of '127.0.0.1' for the IP")
            return False
        
        # Print sample messages for debugging
        if self.message_samples:
            self.logger.info("\n📋 SAMPLE OSC MESSAGES RECEIVED:")
            for i, sample in enumerate(self.message_samples[:5]):
                self.logger.info(f"  {i+1}. {sample['address']} -> {sample['args']}")
        
        if self.sync_failure_detected:
            self.logger.error("\n❌ SYNC FAILURE DETECTED")
            if self.first_invalid:
                self.logger.error(f"First invalid timestamp: {self.first_invalid['timestamp']}")
                self.logger.error(f"OSC Address: {self.first_invalid['address']}")
                self.logger.error(f"Time detected: {self.first_invalid['time']}")
            self.logger.error("EmotiBit is not synchronized to PTP time - check sync status")
            return False
        
        if self.valid_timestamps > 0:
            self.logger.info("\n🎉 VALIDATION PASSED")
            self.logger.info("EmotiBit timestamps are synchronized correctly!")
            return True
        else:
            self.logger.warning("\nNo timestamp data received for validation")
            return False


def main():
    parser = argparse.ArgumentParser(description="Validate EmotiBit timestamps via OSC stream")
    parser.add_argument("--ip", default="0.0.0.0", help="OSC server IP (default: 0.0.0.0)")
    parser.add_argument("--port", type=int, default=12345, help="OSC server port (default: 12345)")
    parser.add_argument("--settle-time", "-s", type=int, default=20, 
                       help="Time to wait before validation (seconds, default: 20)")
    parser.add_argument("--duration", "-d", type=int, default=60,
                       help="Validation duration in seconds (default: 60, 0=indefinite)")
    parser.add_argument("--no-wait", action="store_true", help="Skip settle time")
    parser.add_argument("--verbose", "-v", action="store_true", help="Enable verbose logging")
    
    args = parser.parse_args()
    
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
    
    settle_time = 0 if args.no_wait else args.settle_time
    
    # Create validator
    validator = EmotiBitOSCValidator(
        osc_ip=args.ip,
        osc_port=args.port,
        settle_time=settle_time
    )
    
    print("\nIMPORTANT: Make sure to enable OSC output in EmotiBit Oscilloscope!")
    print(f"Configure OSC to send to: {args.ip}:{args.port}")
    print("Then start EmotiBit streaming...\n")
    
    try:
        success = validator.run_validation(args.duration)
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\nValidation interrupted by user")
        sys.exit(1)


if __name__ == "__main__":
    main()