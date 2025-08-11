# EmotiBit OSC Validation Troubleshooting Guide

## Problem: No OSC Data Received

If you're getting "No OSC data received" errors, follow these steps to diagnose and fix the issue.

## Step 1: Test Basic OSC Communication

First, let's verify that OSC communication is working on your system:

### Terminal 1: Start the test server
```bash
python3 test_osc_server.py
```

### Terminal 2: Send test messages
```bash
python3 test_osc_client.py
```

You should see messages being received in Terminal 1. If this works, OSC communication is functional.

## Step 2: Check EmotiBit Oscilloscope Configuration

1. **Verify OSC Output is Enabled:**
   - Open EmotiBit Oscilloscope
   - Go to Settings/Preferences
   - Look for "OSC Output" or "Network Output" settings
   - Make sure it's enabled

2. **Check OSC Configuration:**
   - Verify the IP address is set to `127.0.0.1` (or your computer's IP)
   - Verify the port is set to `12345`
   - Make sure the patchboard configuration is correct

3. **Check the Patchboard XML:**
   Your patchboard should look like this:
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

## Step 3: Test with EmotiBit Data

1. **Start the validation script with verbose logging:**
   ```bash
   python3 emotibit_osc_validator.py --verbose --no-wait
   ```

2. **In EmotiBit Oscilloscope:**
   - Make sure EmotiBit is connected and streaming
   - Start the data stream
   - Check that OSC output is active

3. **Look for debug output:**
   - The script will show any OSC messages it receives
   - This helps identify the correct message format

## Step 4: Common Issues and Solutions

### Issue: "Address already in use"
**Solution:** Change the port number
```bash
python3 emotibit_osc_validator.py --port 12346
```

### Issue: Firewall blocking UDP
**Solution:** Check firewall settings and allow UDP traffic on port 12345

### Issue: Wrong IP address
**Solution:** Use your computer's actual IP address instead of localhost
```bash
python3 emotibit_osc_validator.py --ip 192.168.1.100
```

### Issue: EmotiBit not sending OSC
**Solution:** 
- Restart EmotiBit Oscilloscope
- Reconnect the EmotiBit device
- Check that the patchboard is properly configured

## Step 5: Advanced Debugging

### Run with maximum debugging:
```bash
python3 emotibit_osc_validator.py --verbose --no-wait --duration 0
```

### Check network connectivity:
```bash
# Test if port is open
netstat -an | grep 12345

# Test UDP connectivity
nc -u -l 12345
```

### Monitor network traffic:
```bash
# Install tcpdump if needed
sudo tcpdump -i lo udp port 12345
```

## Step 6: Verify EmotiBit OSC Format

The script expects EmotiBit to send OSC messages in this format:
- Address: `/emotibit/*` or `/EB/*`
- First argument: timestamp (integer/float)
- Additional arguments: data values

If EmotiBit uses a different format, you may need to modify the script.

## Step 7: Alternative Testing

If the main script still doesn't work, try the simple test server:

1. **Start simple server:**
   ```bash
   python3 test_osc_server.py
   ```

2. **Configure EmotiBit to send to this server**

3. **Check what messages are actually being sent**

This will help identify the exact OSC message format that EmotiBit is using.

## Still Having Issues?

If you're still not receiving data:

1. **Check EmotiBit documentation** for the correct OSC output format
2. **Verify EmotiBit firmware** is up to date
3. **Try a different port** (some ports may be blocked)
4. **Check system logs** for any network errors
5. **Test on a different computer** to isolate the issue

## Contact Information

If you continue to have issues, please provide:
- EmotiBit Oscilloscope version
- Operating system
- Output from the test scripts
- Any error messages from EmotiBit Oscilloscope