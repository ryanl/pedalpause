# pedalpause
Pauses playback (e.g. of Netflix, YouTube) when you aren't pedaling your
exercise bike. Resumes when you start pedaling.

## Requirements

*  **Wahoo BLE Cadence sensor**. https://www.amazon.com/dp/B00L9XNFPY. May work with other sensors.

* **Bluetooth USB adapter that supports BLE**, e.g. I used
  https://www.amazon.com/gp/product/B07V1SZCY6

* **USB extension cable** (optional) so you can position the receiver close to the bike. I found the signal was unreliable without it.

* **Windows 10**. The script is written for Windows 10, but it should be easy enough to adapt to other OSs.

* **Python 3.8** with the following pip packages installed (`py -m pip install `):  win32api, bleak.

## Usage

1. Attach the sensor to your bike, per the manufacturer's instructions.

1. Pedal your bike for 30 secs. This will ensure the sensor starts up its Bluetooth radio.

1. Ensure your Bluetooth is turned on in Windows system settings.
   If you click add device, you should be able to see your sensors in the list of devices. No need to add it here though.

1. Run `pedalpause.py`. Keep pedaling. First time the script runs, it will try to detect your sensor.
