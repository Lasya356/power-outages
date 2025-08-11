# EmotiBit OSC Troubleshooting Guide

## Problem: No OSC Data Received

If you're getting "No OSC data received yet" errors, follow these steps:

### 1. Install Dependencies
```bash
pip install python-osc
```

### 2. Test OSC Server with Test Client

First, run the validator in one terminal:
```bash
python emotibit_osc_validator.py --no-wait --duration 30
```

Then, in another terminal, run the test client:
```bash
python test_osc_client.py
```

If the test client works but EmotiBit doesn't, the issue is with EmotiBit configuration.

### 3. EmotiBit Oscilloscope Configuration

#### Check OSC Output Settings:
1. Open EmotiBit Oscilloscope
2. Go to **Settings** → **OSC Output**
3. Make sure **OSC Output** is **enabled**
4. Set **IP Address** to match your computer's IP (or use `127.0.0.1` for localhost)
5. Set **Port** to `12345`
6. Click **Apply**

#### Alternative IP Addresses to Try:
- `127.0.0.1` (localhost)
- `0.0.0.0` (all interfaces)
- Your computer's actual IP address (e.g., `192.168.1.100`)

### 4. Network and Firewall Issues

#### Check if port is blocked:
```bash
# On Linux/Mac
netstat -an | grep 12345

# On Windows
netstat -an | findstr 12345
```

#### Test with different port:
```bash
python emotibit_osc_validator.py --port 8000
```
Then configure EmotiBit to use port 8000.

### 5. EmotiBit Streaming

Make sure EmotiBit is actually streaming data:
1. Check that EmotiBit device is connected
2. Verify data is being received in EmotiBit Oscilloscope
3. Start streaming in EmotiBit Oscilloscope
4. Look for data activity in the oscilloscope interface

### 6. Debug Mode

Run the validator with verbose logging:
```bash
python emotibit_osc_validator.py --verbose --no-wait
```

### 7. Common OSC Address Patterns

EmotiBit might use different OSC address patterns. The script now catches all messages, but common patterns include:
- `/emotibit/*`
- `/EB/*`
- `/EmotiBit/*`
- `/sensor/*`
- `/data/*`

### 8. Alternative Validation Script

If the main script doesn't work, try this minimal version:

```python
#!/usr/bin/env python3
import time
from pythonosc import dispatcher, osc_server

def handle_message(address, *args):
    print(f"Received: {address} -> {args}")

# Setup server
disp = dispatcher.Dispatcher()
disp.set_default_handler(handle_message)

server = osc_server.ThreadingOSCUDPServer(("0.0.0.0", 12345), disp)
print("Listening on 0.0.0.0:12345...")
server.serve_forever()
```

### 9. Check EmotiBit Documentation

Refer to the official EmotiBit documentation for:
- Correct OSC message format
- Required OSC addresses
- Network configuration requirements

### 10. System-Specific Issues

#### Linux:
- Check if port is in use: `sudo lsof -i :12345`
- Check firewall: `sudo ufw status`

#### Windows:
- Check Windows Firewall settings
- Try running as Administrator

#### macOS:
- Check macOS Firewall settings
- Try different network interfaces

## Quick Test Commands

```bash
# Test 1: Basic validation
python emotibit_osc_validator.py --no-wait --duration 30

# Test 2: Different IP
python emotibit_osc_validator.py --ip 0.0.0.0 --no-wait

# Test 3: Different port
python emotibit_osc_validator.py --port 8000 --no-wait

# Test 4: Test client
python test_osc_client.py

# Test 5: Verbose mode
python emotibit_osc_validator.py --verbose --no-wait
```

## Expected Output

When working correctly, you should see:
```
2025-08-11 12:30:00,000 - INFO - 📨 OSC Message #1: /emotibit/data -> (1234567890, 1, 'PPG', 0.123)
2025-08-11 12:30:00,100 - INFO - 📨 OSC Message #2: /emotibit/data -> (1234567990, 2, 'PPG', 0.124)
```

If you see this, the connection is working and you can proceed with timestamp validation.