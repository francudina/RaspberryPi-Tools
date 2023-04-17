import logging
from types import SimpleNamespace
from unittest import TestCase

from Projects.AutonomousDriving.Config import Arguments
from Projects.AutonomousDriving.Config.Arguments import Arguments
from Projects.Executables.Activities.IActivity import IActivity
from Projects.Executables.ExecutablesStatus import ExecutablesStatus
from Projects.Executables.Pipelines.IPipeline import IPipeline
from Projects.Executables.Pipelines.Inputs.IPipelineInput import IPipelineInput
from Projects.Executables.Pipelines.Inputs.PipelineInputType import PipelineInputType
from RPi import GPIO

# inputs & inputs
device_config = "test/devices.json"
commands = "test/commands.json"
# device_config = "devices.json"
# commands = "commands.json"
logging.basicConfig(level=logging.INFO)


class Test(TestCase):

    def _execute_test(self, run_n_times: int):

        data: {} = {
            'pipeline_input': PipelineInputType.CONSOLE.name,
            'devices_config_file': device_config,
            'commands': commands,
            'gpio_warnings_enabled': False,
            'logging_level': 'info'
        }
        args: SimpleNamespace = SimpleNamespace(**data)
        arguments: Arguments = Arguments(args)

        for _ in range(run_n_times):
            logging.info(f"\n\n*** TEST EXECUTION ***")

            pipeline_input_type: PipelineInputType = PipelineInputType.CONSOLE
            pipeline_input: IPipelineInput = IPipelineInput.get_pipeline_input(arguments)
            pipeline = IPipeline(pipeline_input_type)

            activity: IActivity = pipeline_input.next_input()
            self.assertNotEqual(activity, None)

            added: bool = pipeline.add(activity)
            self.assertNotEqual(added, False)

            started: bool = pipeline.start()

            activity_status: ExecutablesStatus = activity.status
            pipeline_status: ExecutablesStatus = pipeline.status

            activity_passed: bool = activity_status in [
                ExecutablesStatus.FINISHED,
                ExecutablesStatus.DONE_WITH_COMPENSATION,
            ]
            pipeline_passed: bool = pipeline_status in [
                ExecutablesStatus.FINISHED,
                ExecutablesStatus.DONE_WITH_COMPENSATION,
            ]

            logging.info(30 * '- ')
            logging.info(f"> pipeline status: {pipeline_status}")
            logging.info(f"> activity status: {activity_status}")
            logging.info(30 * '- ')

            if not started:
                pipeline_soft_fail: bool = pipeline_status in [
                    ExecutablesStatus.STOP_FAILED,
                    ExecutablesStatus.COMPENSATION_FAILED
                ]
                self.assertEqual(pipeline_soft_fail, True)

            self.assertNotEqual(pipeline_status, ExecutablesStatus.FAILED)
            self.assertEqual(activity_passed, pipeline_passed)

    def test_driving_happy_path(self):
        # setting lower probability to avoid obstacle detection
        GPIO.CURRENT_THRESHOLD = 0.12
        GPIO.CURRENT_SLEEP = 1
        self._execute_test(run_n_times=2)

    def test_driving_unhappy_path_1(self):
        # setting higher probability to force obstacle detection
        GPIO.CURRENT_THRESHOLD = 0.30
        GPIO.CURRENT_SLEEP = 0.5
        self._execute_test(run_n_times=2)

    def test_driving_unhappy_path_2(self):
        # setting even higher probability to force obstacle detection
        GPIO.CURRENT_THRESHOLD = 0.8
        GPIO.CURRENT_SLEEP = 0.1
        self._execute_test(run_n_times=3)
