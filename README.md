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
  
  - adding `[<arguments>]` to `driving_script` script
    ```
      # Info
      [-h]                  arguments help
    
      # Optional
      [--input]             input source for driving, possible options from 'PipelineInputType' class, default: console
      [--gpio-warnings]     enabling/disabling GPIO.setwarnings(...), default: false
      [--log]               logging level, default: info
      
      # Required
      # todo
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
