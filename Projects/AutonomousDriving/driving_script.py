import json
from typing import Dict

from Projects.Executables.Activities.IActivity import IActivity
from Projects.Executables.Pipelines.IPipeline import IPipeline
from Projects.Executables.Pipelines.Inputs.IPipelineInput import IPipelineInput
from Projects.Executables.Pipelines.Inputs.PipelineInputType import PipelineInputType


if __name__ == "__main__":

    # config_path = 'driving_input.json'

    # pipeline config
    # - type
    pipeline_input_type: PipelineInputType = PipelineInputType.CONSOLE
    # - input
    pipeline_input: IPipelineInput = IPipelineInput.get_pipeline_input(pipeline_input_type)
    # - pipeline
    pipeline = IPipeline(pipeline_input_type)

    # iteration start!
    while True:
        activity: IActivity = pipeline_input.next_input()
        if activity is None:
            break

        added: bool = pipeline.add(activity)
        if not added:
            continue

        started: bool = pipeline.start()
        if not started:
            compensated: bool = pipeline.compensate()