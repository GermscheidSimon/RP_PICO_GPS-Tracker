import os

class rpZ_LTEStart():
     def __init__(self):
        self.isconnected =  self.start()
     def start(self):
        try:
            os.system("ip link set wwan0 down ")
            os.system("echo 'Y' | sudo tee /sys/class/net/wwan0/qmi/raw_ip ")
            os.system("ip link set wwan0 up")
            os.system("qmicli -p -d /dev/cdc-wdm0 --device-open-net='net-raw-ip|net-no-qos-header' --wds-start-network=\"apn='h2g2',ip-type=4\" --client-no-release-cid")
            os.system("udhcpc -q -f -i wwan0")
            return True
        except:
            return False
        