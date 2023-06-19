"""
 Copyright (c) 2023 Anthony Mugendi
 
 This software is released under the MIT License.
 https://opensource.org/licenses/MIT
"""

import gc
import time
from typing import Literal, NoReturn, Optional


class Timer:

    """
    # Timer Class.

    Timer type can only take the following string values:

    - `performance`:
        the most precise clock in the system.
    - `process`:
        measures the CPU time, meaning sleep time is not measured.
    - `long_running`:
        it is an increasing clock that do not change when
        the date and or time of the machine is changed.

    # Example

    ```python

    import time
    from wraptimer import Timer

    # initialize
    t = Timer(timer_type="performance")
    # start timer
    t.start()
    # some long running code
    time.sleep(1)
    # stop timer
    t.stop()
    # get duration taken to run
    print('took', t.time_string)

    ```



    """

    _counter_start: Optional[int] = None
    _counter_stop: Optional[int] = None
    _is_started = False

    def __init__(
        self,
        timer_type: Literal["performance", "process", "long_running"] = "performance",
        disable_garbage_collect: bool = True,
    ) -> None:
        self.timer_type = timer_type
        self.disable_garbage_collect = disable_garbage_collect

    def start(self) -> None:
        """Starts the timer ."""
        if self._is_started:
            return

        if self.disable_garbage_collect:
            gc.disable()
        self._counter_start = self.__get_counter()

        self._is_started = True

    def stop(self) -> None:
        """Stop the timer ."""
        self._counter_stop = self.__get_counter()
        if self.disable_garbage_collect:
            gc.enable()

        self._is_started = False

    @property
    def time_nanosec(self) -> float:
        """Return the number of nanoseconds taken from start() to stop().
        Returns:
            float: nanoseconds as a float
        """
        self.__valid_start_stop()
        return self._counter_stop - self._counter_start  # type: ignore

    @property
    def time_sec(self) -> float:
        """Return the number of seconds taken from start() to stop().
        Returns:
            float: seconds as a float
        """
        return self.time_nanosec / 1e9

    @property
    def time_millisec(self) -> float:
        """Return the number of milliseconds taken from start() to stop().
        Returns:
            float: milliseconds as a float
        """
        return self.time_nanosec / 1e6

    @property
    def time_microsec(self) -> float:
        """Return the number of microseconds taken from start() to stop().
        Returns:
            float: microseconds as a float
        """
        return self.time_nanosec / 1e3

    @property
    def time_units(self) -> dict:
        """Return a dictionary of time taken from start() to stop().
        Returns:
            float: nanoseconds as a float
        """
        timers = [
            {"units": "s", "value": self.time_sec},
            {"units": "ms", "value": self.time_millisec},
            {"units": "μs", "value": self.time_microsec},
            {"units": "ns", "value": self.time_nanosec},
        ]

        # print(timers)

        filtered = list(filter(lambda t: t["value"] > 1, timers))

        return filtered[0]

    @property
    def time_string(self) -> str:
        """Return human readable duration taken from start() to stop().
        Returns:
            str: human readable duration
        """
        took = self.time_units
        return "{} {}".format(took["value"], took["units"])

    def __get_counter(self) -> int:
        counter: int
        if self.timer_type == "performance":
            counter = time.perf_counter_ns()
        elif self.timer_type == "process":
            counter = time.process_time_ns()
        elif self.timer_type == "long_running":
            counter = time.monotonic_ns()

        return counter

    def __valid_start_stop(self) -> Optional[NoReturn]:
        if self._counter_start is None:
            raise ValueError("Timer has not been started.")
        if self._counter_stop is None:
            raise ValueError("Timer has not been stopped.")
        return None
