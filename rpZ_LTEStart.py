import os
import sys
import dotenv
import asyncio

class rpZ_LTEStart():
    async def __init__(self):
        await self.start()
    async def start(self):

        await os.system("sudo ip link set wwan0 down ")
        await os.system("echo 'Y' | sudo tee /sys/class/net/wwan0/qmi/raw_ip ")
        await os.system("sudo ip link set wwan0 up")
        await os.system("sudo qmicli -p -d /dev/cdc-wdm0 --device-open-net='net-raw-ip|net-no-qos-header' --wds-start-network=\"apn='h2g2',ip-type=4\" --client-no-release-cid")
        await os.system("sudo udhcpc -q -f -i wwan0")
        