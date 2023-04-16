import time
from datetime import datetime
from threading import Event


def blocking_sleep(total_seconds: float) -> bool:
    """
    Sleeps in a thread blocking way.

    :return Always False because it cannot be interrupted by Event!
    """
    time.sleep(total_seconds)
    return False


def nonblocking_sleep(total_seconds: float, event: Event) -> bool:
    """
    Sleeps in a thread nonblocking way until Event is set to True.

    :return waiting was interrupted with Event set!
    """
    return event.wait(timeout=total_seconds)


def current_time(with_format: str = "%H:%M:%S.%f") -> str:
    return datetime.now().strftime(with_format)
