from Projects.Executables.Pipelines.Inputs.IPipelineInput import IPipelineInput
from Projects.Executables.Pipelines.Inputs.PipelineInputType import PipelineInputType


class AlgorithmInput(IPipelineInput):

    def __init__(self):
        super(AlgorithmInput, self).__init__(PipelineInputType.ALGORITHM)

    def next_input(self, **kwargs):
        pass
