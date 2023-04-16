import logging

from Projects.AutonomousDriving.Config.Arguments import Arguments, get_parser
from Projects.Executables.Activities.IActivity import IActivity
from Projects.Executables.Pipelines.IPipeline import IPipeline
from Projects.Executables.Pipelines.Inputs.IPipelineInput import IPipelineInput
from RPi import GPIO


if __name__ == "__main__":

    arguments: Arguments = get_parser()

    GPIO.setwarnings(arguments.gpio_warnings_enabled)
    logging.basicConfig(level=arguments.logging_level)

    pipeline_input: IPipelineInput = IPipelineInput.get_pipeline_input(arguments)
    pipeline = IPipeline(arguments.pipeline_input)

    try:
        # iteration start
        while True:
            activity: IActivity = pipeline_input.next_input()
            if activity is None:
                break

            added: bool = pipeline.add(activity)
            if not added:
                continue

            started: bool = pipeline.start()
            # if not started:
            #     compensated: bool = pipeline.compensate()
    except KeyboardInterrupt as e:
        GPIO.cleanup()
