import logging
from types import SimpleNamespace
from unittest import TestCase

from Projects.AutonomousDriving.Config import Arguments
from Projects.AutonomousDriving.Config.Arguments import Arguments
from Projects.Executables.Activities.IActivity import IActivity
from Projects.Executables.ExecutablesStatus import ExecutablesStatus
from Projects.Executables.Pipelines.IPipeline import IPipeline
from Projects.Executables.Pipelines.Inputs.IPipelineInput import IPipelineInput
from RPi import GPIO


def execute_test(test_case: TestCase, args: SimpleNamespace):

    logging.info(f"\n\n\t*** TEST EXECUTION ***")
    logging.info(f"(i) Test params:")
    logging.info(f"\t > current threshold: {GPIO.CURRENT_THRESHOLD}")
    logging.info(f"\t > current sleep: {GPIO.CURRENT_SLEEP}")
    logging.info(f"\t > arguments: {args}")

    arguments: Arguments = Arguments(args)

    logging.basicConfig(level=arguments.logging_level)

    pipeline_input: IPipelineInput = IPipelineInput.get_pipeline_input(arguments)
    pipeline = IPipeline(arguments.pipeline_input)

    activity: IActivity = pipeline_input.next_input()
    test_case.assertNotEqual(activity, None)

    added: bool = pipeline.add(activity)
    test_case.assertNotEqual(added, False)

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
        test_case.assertEqual(pipeline_soft_fail, True)

    test_case.assertNotEqual(pipeline_status, ExecutablesStatus.FAILED)
    test_case.assertEqual(activity_passed, pipeline_passed)
