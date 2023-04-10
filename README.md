# Raspberry Pi Tools
![Build](https://github.com/francudina/Raspberry-Pi-Tools/actions/workflows/push_pullreq.yaml/badge.svg)

### About repository
Repository used as a playground for Raspberry Pi ideas

### Getting Started: `AutonomousDriving`

- executing (from `root` dir):
    ```
    # executing script:
    python3 -m Projects.AutonomousDriving.driving_script
  
    # enter path to configuration file, e.g.:
    Projects/AutonomousDriving/driving_input.json
    ```
  
- servo calibration (from `root` dir):
    ```
    # <servo_pin_number> <board_mode> are input params, e.g.: 4 GPIO.BCM
    python3 -m Projects.AutonomousDriving.servo_calibration <servo_pin_number> <servo_pin_number>
    ```
  
- running tests (from `root` dir):
  ```
  python3 -m unittest
  ```
