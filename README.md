# Raspberry Pi Tools
[![Tests](https://github.com/francudina/Raspberry-Pi-Tools/actions/workflows/tests.yaml/badge.svg)](https://github.com/francudina/Raspberry-Pi-Tools/actions/workflows/tests.yaml)


### About repository
Repository used as a playground for Raspberry Pi ideas

### Getting Started: `AutonomousDriving`

- executing (from `root` dir):
    ```
    # executing script, see below for list of arguments:
    python3 -m Projects.AutonomousDriving.driving_script [<arguments>]
  
    # enter path to configuration file, e.g.:
    Projects/AutonomousDriving/driving_input.json
    ```
  
  - see `[<arguments>]` options with `-h` or `--help` param on `driving_script`
  

- servo calibration (from `root` dir):
    ```
    # <servo_pin_number> <board_mode> are input params, e.g.: 4 GPIO.BCM
    python3 -m Projects.AutonomousDriving.servo_calibration <servo_pin_number> <servo_pin_number>
    ```
  
- running tests (from `root` dir):
  ```
  python3 -m unittest
  ```
