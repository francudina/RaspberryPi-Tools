import logging
from abc import abstractmethod

import RPi.GPIO as GPIO
from typing import Any, Callable

from Projects.Executables.External.IExternalService import IExternalService
from Projects.Executables.External.Sensors.SensorConfig import SensorConfig


class ISensor(IExternalService):

    def __init__(self,
                 pin_number: int,
                 pin_direction: GPIO.OUT or GPIO.IN,
                 board_mode: GPIO.BCM or GPIO.BOARD,
                 with_callback: bool,
                 bouncetime: int,
                 pull_up_down: GPIO.PUD_UP or GPIO.PUD_DOWN,
                 callback_edge: GPIO.RISING or GPIO.FALLING or None,
                 callback_func: Callable):
        super(ISensor, self).__init__(pin_number, pin_direction, board_mode)
        # input values
        # - callback
        self.with_callback: bool = with_callback
        self.callback_func: Callable = None if not with_callback else callback_func
        self.callback_edge = None if not with_callback else callback_edge
        self.bouncetime = None if not with_callback else bouncetime
        self.pull_up_down = None if not with_callback else pull_up_down

# methods
    # public
    def new_result(self, **kwargs) -> Any:
        if self.with_callback:
            raise Exception(f"Cannot use ISensor.new_result() for events! "
                            f"Instead use custom method with fixed expected arguments!")
        else:
            return self.__new_result_without_callback(**kwargs)

    def start(self, **kwargs) -> bool:
        return self.__configure()

    def stop(self, **kwargs) -> bool:
        if self.with_callback:
            GPIO.remove_event_detect(self.pin_number)
        else:
            GPIO.cleanup(self.pin_number)
        return True

    # private
    def __configure(self) -> bool:
        try:
            GPIO.setmode(self.board_mode)
            GPIO.setwarnings(False)

            if self.with_callback:
                GPIO.setup(self.pin_number, self.pin_direction, self.pull_up_down)
                GPIO.add_event_detect(
                    self.pin_number,
                    self.callback_edge,
                    callback=self.callback_func,
                    bouncetime=self.bouncetime)
            else:
                GPIO.setup(self.pin_number, self.pin_direction)

            return True
        except Exception as e:
            logging.error(f'Error in ISensor.__configure() method: {e}')
            return False

    def __new_result_without_callback(self, **kwargs):
        if self.pin_direction == GPIO.IN:
            return GPIO.input(self.pin_number)
        elif self.pin_direction == GPIO.OUT:
            if SensorConfig.SENSOR_OUTPUT_VOLTAGE_LEVEL_KEY.value not in kwargs.keys():
                raise ValueError(f'ISensor.new_result(**kwargs) must have '
                                 f'{SensorConfig.SENSOR_OUTPUT_VOLTAGE_LEVEL_KEY.value} key specified!')
            # set GPIO.LOW ili GPIO.HIGH as pin output value!
            output_value = kwargs[SensorConfig.SENSOR_OUTPUT_VOLTAGE_LEVEL_KEY.value]
            GPIO.output(self.pin_number, output_value)
            # returns sent value
            return output_value
        else:
            raise ValueError(f'Wrong pin_direction set! Expected: GPIO.OUT or GPIO.IN value!')

    @abstractmethod
    def _new_result_with_callback(self, **kwargs):
        pass
