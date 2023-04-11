import logging
from unittest.mock import patch
from unittest import TestCase

from Projects.Executables.Activities.IActivity import IActivity
from Projects.Executables.ExecutablesStatus import ExecutablesStatus
from Projects.Executables.Pipelines.IPipeline import IPipeline
from Projects.Executables.Pipelines.Inputs.IPipelineInput import IPipelineInput
from Projects.Executables.Pipelines.Inputs.PipelineInputType import PipelineInputType

test_case_1 = "test/driving_test_input_basic_obstacles.json"
logging.basicConfig(level=logging.INFO)


class Test(TestCase):

    @patch(
        target='Projects.Executables.Pipelines.Inputs.Types.ConsoleInput.ConsoleInput._read_input',
        return_value=test_case_1
    )
    def test_driving(self, input):
        pipeline_input_type: PipelineInputType = PipelineInputType.CONSOLE
        pipeline_input: IPipelineInput = IPipelineInput.get_pipeline_input(pipeline_input_type)
        pipeline = IPipeline(pipeline_input_type)

        run_n_times: int = 3
        for _ in range(run_n_times):
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

            self.assertEqual(started, True)
            self.assertNotEqual(pipeline_status, ExecutablesStatus.FAILED)
            self.assertEqual(activity_passed, pipeline_passed)
