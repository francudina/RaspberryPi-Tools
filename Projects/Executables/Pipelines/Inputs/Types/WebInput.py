from Projects.AutonomousDriving.Config.Arguments import Arguments
from Projects.Executables.Activities.IActivity import IActivity
from Projects.Executables.Pipelines.Inputs.IPipelineInput import IPipelineInput
from Projects.Executables.Pipelines.Inputs.PipelineInputType import PipelineInputType


class WebInput(IPipelineInput):

    def __init__(self, arguments: Arguments):
        super(WebInput, self).__init__()

    def _get_input(self, **kwargs) -> IActivity:
        pass
