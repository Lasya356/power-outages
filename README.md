# EmotiBit OSC Timestamp Validation Tool

This tool validates EmotiBit timestamps via OSC stream to detect PTP synchronization failures.

## Features

- Receives OSC stream from EmotiBit Oscilloscope
- Validates timestamps to detect sync failures (timestamps starting from 0)
- Comprehensive debugging and troubleshooting capabilities
- Configurable settle time and validation duration
- Detailed logging and status reporting

## Installation

### Prerequisites

- Python 3.6+
- EmotiBit Oscilloscope software
- EmotiBit device

### Install Dependencies

```bash
# Install python-osc library
pip install python-osc --break-system-packages
```

## Usage

### Basic Usage

```bash
python3 emotibit_osc_validator.py
```

### Advanced Options

```bash
# Skip settle time and run for 30 seconds
python3 emotibit_osc_validator.py --no-wait --duration 30

# Use different IP and port
python3 emotibit_osc_validator.py --ip 192.168.1.100 --port 12346

# Enable verbose logging
python3 emotibit_osc_validator.py --verbose

# Run indefinitely until interrupted
python3 emotibit_osc_validator.py --duration 0
```

### Command Line Options

- `--ip`: OSC server IP address (default: 127.0.0.1)
- `--port`: OSC server port (default: 12345)
- `--settle-time, -s`: Time to wait before validation in seconds (default: 20)
- `--duration, -d`: Validation duration in seconds (default: 60, 0=indefinite)
- `--no-wait`: Skip settle time
- `--verbose, -v`: Enable verbose logging

## EmotiBit Oscilloscope Configuration

### 1. Enable OSC Output

1. Open EmotiBit Oscilloscope
2. Go to Settings/Preferences
3. Enable "OSC Output" or "Network Output"

### 2. Configure OSC Settings

Set the following in EmotiBit Oscilloscope:
- **IP Address**: `127.0.0.1` (or your computer's IP)
- **Port**: `12345`
- **Protocol**: OSC

### 3. Patchboard Configuration

Your patchboard XML should include:

```xml
<patchboard>
    <settings>
        <input>
            <type>EmotiBit</type>
        </input>
        <output>
            <type>OSC</type>
            <ipAddress>localhost</ipAddress>
            <port>12345</port>
        </output>
    </settings>
    <patchcords>
        <!-- Your patchcords here -->
    </patchcords>
</patchboard>
```

## Testing

### Test OSC Communication

Before using with EmotiBit, test that OSC communication works:

```bash
# Terminal 1: Start test server
python3 test_osc_server.py

# Terminal 2: Send test messages
python3 test_osc_client.py
```

### Test Complete System

```bash
# Run the complete test
python3 test_osc_communication.py
```

## Troubleshooting

### No Data Received

If you get "No OSC data received" errors:

1. **Verify OSC is working:**
   ```bash
   python3 test_osc_communication.py
   ```

2. **Check EmotiBit Oscilloscope:**
   - Ensure OSC output is enabled
   - Verify IP/port configuration
   - Check that EmotiBit is streaming data

3. **Check network:**
   - Verify firewall settings
   - Try different port numbers
   - Use actual IP instead of localhost

4. **Run with debugging:**
   ```bash
   python3 emotibit_osc_validator.py --verbose --no-wait
   ```

### Common Issues

- **"Address already in use"**: Change port number
- **Firewall blocking**: Allow UDP traffic on port 12345
- **Wrong IP**: Use computer's actual IP address
- **EmotiBit not sending**: Restart EmotiBit Oscilloscope

## Expected Output

### Successful Validation

```
🎉 VALIDATION PASSED
EmotiBit timestamps are synchronized correctly!
```

### Sync Failure Detected

```
❌ SYNC FAILURE DETECTED
First invalid timestamp: 0
OSC Address: /emotibit/data
Time detected: 2025-08-11 19:40:16
EmotiBit is not synchronized to PTP time - check sync status
```

### No Data Received

```
❌ NO DATA RECEIVED
Make sure EmotiBit Oscilloscope OSC output is enabled and configured correctly
```

## Files

- `emotibit_osc_validator.py` - Main validation script
- `test_osc_server.py` - Simple OSC server for testing
- `test_osc_client.py` - Simple OSC client for testing
- `test_osc_communication.py` - Complete OSC communication test
- `TROUBLESHOOTING.md` - Detailed troubleshooting guide

## Support

If you continue to have issues:

1. Check the troubleshooting guide
2. Verify EmotiBit documentation for correct OSC format
3. Test with the provided test scripts
4. Check system logs for network errors

## License

This tool is provided as-is for EmotiBit timestamp validation.
