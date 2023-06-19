"""
 Copyright (c) 2023 Anthony Mugendi
 
 This software is released under the MIT License.
 https://opensource.org/licenses/MIT
"""
import asyncio
from functools import wraps

from .timer import Timer
from .utils import DebugContext, log


class TimeIt:
    def __init__(self, verbose: bool = True, show_args: bool = False):
        self.verbose = verbose
        self.show_args = show_args

    def byline(self, func):
        """Function decorator to print duration taken to run decorated function
        line by line.
        Works for both sync and async functions.

        Example:

        ```python
        from wraptimer import TimeIt
        # init
        timeit = TimeIt(verbose=True, show_args=True)

        # decorate
        @timeit.byline
        def func_to_time():
            timer.sleep(1)
        ```
        """

        @wraps(func)
        async def wrapper(*args, **kwargs):
            debug_context = DebugContext(
                name=func.__name__, verbose=self.verbose, func=func
            )
            with debug_context:
                t = Timer()
                t.start()

                # run with await if async function
                if asyncio.iscoroutinefunction(func):
                    result = await func(*args, **kwargs)
                else:
                    result = func(*args, **kwargs)

                t.stop()

                # print(debug_context.traced)
                if self.verbose:
                    log(
                        what=func,
                        t=t,
                        args=args,
                        kwargs=kwargs,
                        show_args=self.show_args,
                        draw_sep=["bottom", "mid"],
                    )
                    return result
                else:
                    return (
                        result,
                        debug_context.traced,
                        log(
                            func,
                            t,
                            args,
                            kwargs,
                            self.show_args,
                            return_trace=True,
                        ),
                    )

        def run(*args, **kwargs):
            return asyncio.run(wrapper(*args, **kwargs))

        async def async_run(*args, **kwargs):
            return await wrapper(*args, **kwargs)

        return async_run if asyncio.iscoroutinefunction(func) else run

    def func(self, func: callable) -> None:
        """Function decorator to print duration taken to run decorated function.
        Works for both sync and async functions.

        Example:

        ```python
        from wraptimer import TimeIt
        # init
        timeit = TimeIt(verbose=True, show_args=True)

        # decorate
        @timeit.func
        def func_to_time():
            timer.sleep(1)
        ```
        """

        @wraps(func)
        async def wrapper(*args, **kwargs):
            t = Timer()
            t.start()

            # run with await if async function
            if asyncio.iscoroutinefunction(func):
                result = await func(*args, **kwargs)
            else:
                result = func(*args, **kwargs)

            t.stop()

            # if verbose, log
            if self.verbose:
                log(
                    what=func,
                    t=t,
                    args=args,
                    kwargs=kwargs,
                    show_args=self.show_args,
                    draw_sep=["top", "bottom"],
                )
                return result
            else:
                return (
                    result,
                    log(
                        wht=func,
                        t=t,
                        args=args,
                        kwargs=kwargs,
                        show_args=self.show_args,
                        return_trace=True,
                    ),
                )

        def run(*args, **kwargs):
            return asyncio.run(wrapper(*args, **kwargs))

        async def async_run(*args, **kwargs):
            return await wrapper(*args, **kwargs)

        return async_run if asyncio.iscoroutinefunction(func) else run
