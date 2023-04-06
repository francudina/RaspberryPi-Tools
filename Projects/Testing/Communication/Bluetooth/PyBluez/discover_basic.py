# simple inquiry example

import bluetooth


while True:
    nearby_devices = bluetooth.discover_devices(lookup_names=True)
    print("\n# Found {} devices.".format(len(nearby_devices)))

    if len(nearby_devices) == 0:
        continue

    for addr, name in nearby_devices:
        print("\t> name: {}, address: {}".format(name, addr))
