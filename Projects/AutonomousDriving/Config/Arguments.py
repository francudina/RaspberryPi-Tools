import argparse
import logging

from Projects.Executables.Pipelines.Inputs.PipelineInputType import PipelineInputType


"""
Input argument for AutonomousDriving pipeline.
"""
class Arguments:

    pipeline_input: PipelineInputType
    gpio_warnings_enabled: bool
    logging_level: int

    def __init__(self, args):
        # expect pipeline input from source
        self.pipeline_input = PipelineInputType[str.upper(args.pipeline_input)]
        self.gpio_warnings_enabled = args.gpio_warnings_enabled
        self.logging_level = getattr(logging, str.upper(args.logging_level))


def _str2bool(v):
    if isinstance(v, bool):
        return v
    if v.lower() in ('yes', 'true', 't', 'y', '1'):
        return True
    elif v.lower() in ('no', 'false', 'f', 'n', '0'):
        return False
    else:
        raise argparse.ArgumentTypeError('Boolean value expected.')


def get_parser() -> Arguments:
    parser = argparse.ArgumentParser(prog='AutonomousDriving')
    # console is default input source
    parser.add_argument('--input', dest='pipeline_input', type=str, default=PipelineInputType.CONSOLE.name)
    # enable/disable GPIO warnings
    parser.add_argument("--gpio-warnings", dest='gpio_warnings_enabled',
                        type=_str2bool, nargs='?', const=True, default=False)
    # logging level
    parser.add_argument('--log', dest='logging_level', type=str, default='info')

    return Arguments(parser.parse_args())
