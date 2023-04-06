import json
import logging
from typing import Dict

from Projects.AutonomousDriving.Services.Driving.DrivingActivity import DrivingActivity
from Projects.Executables.Activities.ActivityType import ActivityType
from Projects.Executables.Activities.IActivity import IActivity
from Projects.Executables.Pipelines.Inputs.IPipelineInput import IPipelineInput
from Projects.Executables.Pipelines.Inputs.InputConfig import InputConfig
from Projects.Executables.Pipelines.Inputs.PipelineInputType import PipelineInputType


class ConsoleInput(IPipelineInput):

    def __init__(self):
        super(ConsoleInput, self).__init__(PipelineInputType.CONSOLE)

    def _get_input(self, **kwargs) -> IActivity:
        iter_num: int = 3

        activity: IActivity = None
        while iter_num > 1:
            iter_num -= 1

            input_data: str = input(f'\n## Insert ACTIVITY Config file path (attempts remaining: {iter_num}): ')
            file_data: Dict = self.__read_file(input_data)
            if file_data is None:
                continue

            activity = self.__get_activity(**file_data)
            if activity is None:
                continue
            break

        return activity

# private
    def __get_activity(self, **file_data) -> IActivity:
        try:
            activity_type: str = file_data[InputConfig.ACTIVITY_TYPE_FIELD.value]

            # todo dodaj i druge tipove aktivnosti ovdje da se kreiraju!
            if activity_type == ActivityType.DRIVING.value:
                return DrivingActivity(
                    pipeline_input_type=self.input_type,
                    **file_data
                )
            else:
                return None
        except Exception as e:
            logging.error(f"Error during activity creation: {e}")
            return None

    def __read_file(self, file_path: str):
        try:
            with open(file_path, 'r', encoding="utf-8") as fh:
                return json.loads(fh.read())
        except Exception as e:
            print(f"(e) Exception: {e}")
            return None
