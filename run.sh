#!/bin/bash

ANDROID_SDK="$HOME/Library/Android/sdk"
ADB="$ANDROID_SDK/platform-tools/adb"
EMULATOR="$ANDROID_SDK/emulator/emulator"

export PATH="$ANDROID_SDK/platform-tools:$ANDROID_SDK/emulator:$PATH"

# Start ADB server
echo "[1/5] Starting ADB server..."
$ADB start-server 2>&1 | grep -v "daemon started successfully" || true
sleep 1

# Check for running devices
echo "[2/5] Checking for devices..."
DEVICE_COUNT=$($ADB devices | grep -v "List of devices" | grep -E "device$|emulator" | wc -l | xargs)

if [ "$DEVICE_COUNT" -eq 0 ]; then
    echo "No running devices found."
    echo ""
    echo "Available emulators:"
    AVDS=$($EMULATOR -list-avds)
    
    if [ -z "$AVDS" ]; then
        echo "Error: No emulators available. Please create one in Android Studio."
        exit 1
    fi
    
    echo "$AVDS"
    echo ""
    
    # Get first available AVD
    FIRST_AVD=$(echo "$AVDS" | head -n 1)
    echo "Starting emulator: $FIRST_AVD"
    
    # Start emulator in background
    $EMULATOR -avd "$FIRST_AVD" -no-snapshot-load > /dev/null 2>&1 &
    EMULATOR_PID=$!
    
    echo "Waiting for emulator to boot (30-60 seconds)..."
    
    # Wait for device to appear
    MAX_WAIT=120
    WAITED=0
    while [ $WAITED -lt $MAX_WAIT ]; do
        DEVICE_COUNT=$($ADB devices | grep -v "List of devices" | grep -E "device$|emulator" | wc -l | xargs)
        if [ "$DEVICE_COUNT" -gt 0 ]; then
            break
        fi
        sleep 3
        WAITED=$((WAITED + 3))
        echo -n "."
    done
    echo ""
    
    if [ "$DEVICE_COUNT" -eq 0 ]; then
        echo "Error: Timeout waiting for emulator"
        exit 1
    fi
fi

# Get device serial
DEVICE_SERIAL=$($ADB devices | grep -v "List of devices" | grep -E "device$|emulator" | head -n 1 | awk '{print $1}')
echo "Device found: $DEVICE_SERIAL"

# Extract port number
DEVICE_PORT=$(echo "$DEVICE_SERIAL" | sed 's/emulator-//')

echo "[3/5] Waiting for device to be ready..."
$ADB -s "$DEVICE_SERIAL" wait-for-device

# Wait for boot to complete
MAX_BOOT_WAIT=60
BOOT_WAITED=0
while [ $BOOT_WAITED -lt $MAX_BOOT_WAIT ]; do
    BOOT_STATUS=$($ADB -s "$DEVICE_SERIAL" shell getprop sys.boot_completed 2>/dev/null | tr -d '\r')
    if [ "$BOOT_STATUS" = "1" ]; then
        break
    fi
    sleep 2
    BOOT_WAITED=$((BOOT_WAITED + 2))
done

if [ "$BOOT_STATUS" != "1" ]; then
    echo "Warning: Device may not be fully booted"
fi

echo "Device is ready (port: $DEVICE_PORT)"

# Wait for package manager
sleep 2
$ADB -s "$DEVICE_SERIAL" shell pm list packages > /dev/null 2>&1

echo "[4/5] Activating Python environment..."
cd "$(dirname "$0")/Automation"
source ../env/bin/activate

echo "[5/6] Installing  APK..."
$ADB -s "$DEVICE_SERIAL" install -t -r APKs/50.apk
echo ""


python3 reproduction.py "$DEVICE_PORT" BRs/50.txt
echo "  Execution Complete"

