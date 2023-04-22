import logging
from RPi import GPIO
from types import SimpleNamespace
from unittest import TestCase

from Projects.Executables.Pipelines.Inputs.PipelineInputType import PipelineInputType
from test.Utils.algorithm_execution import execute_test

# inputs & inputs
device_config = "test/devices.json"
commands = "test/commands.json"
# device_config = "devices.json"
# commands = "commands.json"
logging.basicConfig(level=logging.INFO)


class Test(TestCase):

    def _execute(self, run_n_times: int = 1):
        data: {} = {
            'pipeline_input': PipelineInputType.CONSOLE.name,
            'devices_config_file': device_config,
            'commands': commands,
            'gpio_warnings_enabled': False,
            'logging_level': 'info',
            'algorithm': None,
            'max_execution_seconds': None,
            'tabu_queue_size': None,
            'option_success_reward': None,
            'option_failure_penalty': None,
            'option_success_time_reward': None,
            'option_failure_time_penalty': None
        }
        args: SimpleNamespace = SimpleNamespace(**data)

        for _ in range(run_n_times):
            execute_test(self, args)

    def test_driving_happy_path(self):
        # setting lower probability to avoid obstacle detection
        GPIO.CURRENT_THRESHOLD = 0.12
        GPIO.CURRENT_SLEEP = 1
        self._execute(run_n_times=1)

    def test_driving_unhappy_path_1(self):
        # setting higher probability to force obstacle detection
        GPIO.CURRENT_THRESHOLD = 0.30
        GPIO.CURRENT_SLEEP = 0.5
        self._execute(run_n_times=2)

    def test_driving_unhappy_path_2(self):
        # setting even higher probability to force obstacle detection
        GPIO.CURRENT_THRESHOLD = 0.8
        GPIO.CURRENT_SLEEP = 0.1
        self._execute(run_n_times=1)
