# Raspberry-Pi-Tools
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
    python3 -m Projects.AutonomousDriving.servo_calibration <servo_pin_number_param> <board_mode_param>
    ```
