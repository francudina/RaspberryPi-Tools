from Projects.Executables.Pipelines.Inputs.IPipelineInput import IPipelineInput
from Projects.Executables.Pipelines.Inputs.PipelineInputType import PipelineInputType


class WebInput(IPipelineInput):

    def __init__(self):
        super(WebInput, self).__init__(PipelineInputType.WEB)

    def next_input(self, **kwargs):
        pass
