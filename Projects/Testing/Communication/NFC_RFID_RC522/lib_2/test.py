import time
from pirc522 import RFID

rdr = RFID()

print("# Starting with reading ...")

while True:

    print("\n> Waiting for tag  ...")
    rdr.wait_for_tag()

    (error, tag_type) = rdr.request()
    print(f"< Got from request! \n\t(i) tag_type: {tag_type} \n\t(e) error: {error}\n")

    if error:
        print(f"(e) Error occurred during request!\n")
        continue

    print("# Tag detected!")

    (error, uid) = rdr.anticoll()
    print(f"< Got from anticoll! \n\t(i) uid: {uid} \n\t(e) error: {error}\n")

    if error:
        print(f"(e) Error occurred during anticoll!\n")
        continue

    # Select Tag is required before Auth
    if rdr.select_tag(uid):
        print(f"(e) Select tag - failed\n")
        continue

    # Auth for block 10 (block 2 of sector 2) using default shipping key A
    if not rdr.card_auth(rdr.auth_a, 10, [0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF], uid):
        # This will print something like (False, [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
        print("(i) Reading block 10: " + str(rdr.read(10)))
        # Always stop crypto1 when done working
        rdr.stop_crypto()

    time.sleep(2)

# Calls GPIO cleanup
rdr.cleanup()
