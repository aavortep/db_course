import os
import sys


os_type = sys.platform.lower()
if "win" in os_type:
    command = "wmic bios get serialnumber"
else:
    command = "hal-get-property --udi /org/freedesktop/Hal/devices/computer " \
              "--key system.hardware.uuid"
binded_serial = os.popen(command).read().replace("\n", "")

with open("serial.key", "w") as f:
    f.write(str(binded_serial))
