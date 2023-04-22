import argparse
import logging

from Projects.AutonomousDriving.Services.Algorithm.DrivingAlgorithmType import DrivingAlgorithmType
from Projects.Executables.Pipelines.Inputs.PipelineInputType import PipelineInputType


class Arguments:
    """
    Input argument for AutonomousDriving pipeline.
    """

    pipeline_input: PipelineInputType
    devices_config_file: str
    commands: str

    gpio_warnings_enabled: bool
    logging_level: int

    algorithm: DrivingAlgorithmType
    max_execution_seconds: int

    tabu_queue_size: int

    option_success_reward: float
    option_failure_penalty: float

    option_success_time_reward: float
    option_failure_time_penalty: float

    def __init__(self, args):
        self.pipeline_input = PipelineInputType[str.upper(args.pipeline_input)]
        self.devices_config_file = args.devices_config_file
        self.commands = args.commands

        self.gpio_warnings_enabled = args.gpio_warnings_enabled
        self.logging_level = getattr(logging, str.upper(args.logging_level))

        if args.algorithm:
            self.algorithm = DrivingAlgorithmType[str.upper(args.algorithm)]
        self.max_execution_seconds = args.max_execution_seconds

        self.tabu_queue_size = args.tabu_queue_size

        self.option_success_reward = args.option_success_reward
        self.option_failure_penalty = args.option_failure_penalty

        self.option_success_time_reward = args.option_success_time_reward
        self.option_failure_time_penalty = args.option_failure_time_penalty


def _str2bool(v):
    if isinstance(v, bool):
        return v
    if v.lower() in ('yes', 'true', 't', 'y', '1'):
        return True
    elif v.lower() in ('no', 'false', 'f', 'n', '0'):
        return False
    else:
        raise argparse.ArgumentTypeError('Boolean value expected.')


def parser_config() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog='AutonomousDriving')
    parser.add_argument('--input',
                        dest='pipeline_input',
                        type=str,
                        default=PipelineInputType.CONSOLE.name,
                        help='input source for driving; options from PipelineInputType class; '
                             'default: console')
    parser.add_argument('--config',
                        dest='devices_config_file',
                        type=str,
                        required=True,
                        help='used devices input file path; '
                             'default: true')
    parser.add_argument('--commands',
                        dest='commands',
                        type=str,
                        default=None,
                        help='commands to execute input file path; '
                             'default: None')
    parser.add_argument("--gpio-warnings",
                        dest='gpio_warnings_enabled',
                        type=_str2bool,
                        nargs='?',
                        const=True,
                        default=False,
                        help='enabling/disabling GPIO.setwarnings(...), '
                             'default: false')
    parser.add_argument('--log',
                        dest='logging_level',
                        type=str,
                        default='info',
                        help='logging level, default: info')
    parser.add_argument('--algorithm',
                        dest='algorithm',
                        type=str,
                        default=DrivingAlgorithmType.RANDOM.name,
                        help='used algorithm in execution; only used with Algorithm input; '
                             'default: random')
    parser.add_argument('--max-seconds',
                        dest='max_execution_seconds',
                        type=int,
                        default=30,
                        help='maximum number of seconds allowed for execution; '
                             'default: 30')
    parser.add_argument('--tabu-size',
                        dest='tabu_queue_size',
                        type=int,
                        default=2,
                        help='(Tabu algorithm only!) direction tabu search queue (FIFO) size; '
                             'default: 2')
    parser.add_argument('--likelihood-reward',
                        dest='option_success_reward',
                        type=float,
                        default=0.1,
                        help='(Tabu algorithm only!) reward direction likelihood for which was successful; '
                             'default: 0.1')
    parser.add_argument('--likelihood-penalty',
                        dest='option_failure_penalty',
                        type=float,
                        default=0.05,
                        help='(Tabu algorithm only!) likelihood penalty for direction which was unsuccessful; '
                             'default: 0.05')
    parser.add_argument('--success-time-reward',
                        dest='option_success_time_reward',
                        type=float,
                        default=2,
                        help='(Tabu algorithm only!) reward direction time factor for which was successful; '
                             'default: 2')
    parser.add_argument('--success-time-penalty',
                        dest='option_failure_time_penalty',
                        type=float,
                        default=0.5,
                        help='(Tabu algorithm only!) time penalty factor for direction which was unsuccessful; '
                             'default: 0.5')
    return parser


def get_parser() -> Arguments:
    parser = parser_config()
    return Arguments(parser.parse_args())
