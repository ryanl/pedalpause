import asyncio
from bleak import BleakScanner, BleakClient
import win32api
import win32con
import time


def punish():
    """Pauses media if not already paused"""
    global stopped
    if not stopped:
        print("Pausing media")
        win32api.PostMessage(0xffff, 0x319, 0, 65536 * 47)
        stopped = True

stopped = False
punish()

def unpunish():
    """Resumes media if not already playing"""
    global stopped
    if stopped:
        print("Resuming media")
        win32api.PostMessage(0xffff, 0x319, 0, 65536 * 46)
        stopped = False

previous_value = None

def notification_handler(sender, data):
    """Handles messages received from the cadence sensor"""
    global previous_value
    print("{}: {}".format(sender, data.hex()))
    if previous_value is not None and data != previous_value:
        unpunish()
    previous_value = data

def write_bluetooth_address(address):
    with open("bluetooth_address", "w") as f:
        f.write(address)

async def run():
    global previous_value

    try:
        with open("bluetooth_address", "r") as f:
            bluetooth_address = f.read().strip()
    except:
        print("Discovering nearby devices")
        devices_seen = {}
        bluetooth_address = None
        for _ in range(5):
            devices = await BleakScanner.discover(address_type="random")

            for d in devices:
                devices_seen[d.address] = d
                if "cadence" in d.name.lower():
                    bluetooth_address = d.address
            if bluetooth_address:
                break

        if bluetooth_address:
            print("Detected cadence sensor {}".format(bluetooth_address))
        else:
            numbered_devices = enumerate(devices_seen.values())
            for (n, d) in numbered_devices:
                print("{}: {}".format(n, str(d)[:60]))

            print("Are any of the devices above your cadence sensor? Enter its row number here.")
            print("If your device is not showing up, make sure you are pedaling")
            n = int(input())
            if n >= 0 and n < len(numbered_devices):
                bluetooth_address = numbered_devices[n][1]

        if bluetooth_address:
            write_bluetooth_address(bluetooth_address)
        else:
            print("Bluetooth address not found")


    characteristic = "00002a5b-0000-1000-8000-00805f9b34fb"
    while True:
        try:
            print("Attempting to connect")
            previous_value = None
            async with BleakClient(bluetooth_address) as client:
                print("Connected")
                await client.start_notify(
                    characteristic, notification_handler)
                print("Registered")
                punish_count = 0
                while punish_count < 10:
                    store = previous_value
                    print("Storing current value of {}".format(store))
                    await asyncio.sleep(6)
                    print("Comparing {} to {}".format(store, previous_value))
                    if store == previous_value:
                        punish()
                        punish_count += 1
                    else:
                        punish_count = 0

                print("Unregistering")
                await client.stop_notify(characteristic)
            # Not sure if this is necessary, but I've added some down time to
            # allow the sensor to sleep so we don't waste the battery.
            if punish_count == 10:
                print("Letting the device go to sleep")
                await asyncio.sleep(60)
        except Exception as e:
            print(e)

loop = asyncio.get_event_loop()
loop.run_until_complete(run())
