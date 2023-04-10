import time
from threading import Event


"""
Sleeps in a thread blocking way.

:returns Always False because it cannot be interrupted by Event!
"""
def blocking_sleep(total_seconds: float) -> bool:
    time.sleep(total_seconds)
    return False


"""
Sleeps in a thread nonblocking way until Event is set to True.

:returns waiting was interrupted with Event set!
"""
def nonblocking_sleep(total_seconds: float, event: Event) -> bool:
    return event.wait(timeout=total_seconds)
