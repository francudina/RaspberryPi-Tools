import logging

from Projects.AutonomousDriving.Services.Algorithm.DrivingAlgorithmType import DrivingAlgorithmType
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

    def _execute(
            self,
            run_n_times: int,
            algorithm: DrivingAlgorithmType,
            use_init_commands: bool,
            max_execution_seconds: int,
            tabu_queue_size: int = None,
    ):
        data: {} = {
            'pipeline_input': PipelineInputType.ALGORITHM.name,
            'devices_config_file': device_config,
            'commands': commands if use_init_commands else None,
            'gpio_warnings_enabled': False,
            'logging_level': 'info',
            'algorithm': algorithm.name,
            'max_execution_seconds': max_execution_seconds,
            'tabu_queue_size': tabu_queue_size,
            'option_success_reward': 0.1,
            'option_failure_penalty': 0.05,
            'option_success_time_reward': 2,
            'option_failure_time_penalty': 0.5
        }
        args: SimpleNamespace = SimpleNamespace(**data)

        for _ in range(run_n_times):
            execute_test(self, args)

    def test_random_driving_happy_path(self):
        # setting lower probability to avoid obstacle detection
        GPIO.CURRENT_THRESHOLD = 0.12
        GPIO.CURRENT_SLEEP = 1
        self._execute(
            run_n_times=1,
            algorithm=DrivingAlgorithmType.RANDOM,
            use_init_commands=True,
            max_execution_seconds=5
        )

    def test_tabu_driving_happy_path(self):
        # setting higher to force failures of commands
        GPIO.CURRENT_THRESHOLD = 0.12
        GPIO.CURRENT_SLEEP = 1.5
        self._execute(
            run_n_times=1,
            algorithm=DrivingAlgorithmType.TABU_SEARCH,
            use_init_commands=False,
            max_execution_seconds=10,
            tabu_queue_size=2
        )
