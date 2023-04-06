# bluetooth low energy scan

from bluetooth.ble import DiscoveryService


service = DiscoveryService()

while True:
    devices = service.discover(2)
    print("\n# Found {} devices.".format(len(devices)))

    if len(devices) == 0:
        continue

    for address, name in devices.items():
        print("\t> name: {}, address: {}".format(name, address))
