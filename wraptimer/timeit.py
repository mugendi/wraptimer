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

    """# Timeit Class
    This class exposes two decorators `@byline` and `@func`
    which work perfectly with both synchronous and asynchronous
    functions.

    ## Args:
    - `verbose` bool : Defaults to `True`.
    If True, then decorators will print execution time
    to console. If false then the execution time data is added to
    the function response so that it return a tuple.

        **Example:**
        ```python
        # init
        import pprint
        timeit_non_verbose = TimeIt(verbose=False)

        # decorate
        @timeit_non_verbose.byline
        def test_non_verbose(v=1):
            time.sleep(1.5)
            x = v * 50
            return x

        resp = test_non_verbose(22)
        pprint.pprint(resp)
        ```
        This will output:
        ```txt
        (1100,
            [{'LINE': 75, 'SYNC FUNC': 'test_non_verbose', 'TOOK': '1.501589155 s'},
            {'LINE': 76, 'SYNC FUNC': 'test_non_verbose', 'TOOK': '29.476 μs'}],
            [' TOOK: 1.501719173 s'])
        ```
        Where:

        1. The first value **1100** is the si the `test_non_verbose()`
        return value i.e **22*50**
        2. The second tuple value is a list of all execution times
        in this case *by line* execution times and *total execution time*

        !!! note
            Setting `verbose` to `False` is useful in cases where you want
            to measure execution time and instead of printing, use the values
            in other ways, such as saving the data to a timeseries database
            for future reporting on code execution.

    - `show_args` bool : Defaults to `False`. When set to `True`, arguments
    passed to the decorated function are printed.

        **Example:**
        ```python
        # init
        timeit_non_verbose = TimeIt(show_args=True)

        # decorate
        @timeit_non_verbose.byline
        def test_non_verbose(v=1):
            time.sleep(1.5)
            x = v * 50
            return x

        test_non_verbose(22)

        ```
        Logs:
        ![](images/)
        ```txt
        ━━━━━━━━━━━━━━━━━━━━━━━ [ SYNC FUNC: test_non_verbose ] ━━━━━━━━━━━━━━━━━━━━━━━
        LINE: 89, TOOK: 1.500271156 s
        LINE: 90, TOOK: 320.156 μs
        ------------------------------------------------------------------------------
        ARGS: (22,)
        KWARGS: {}
        TOOK: 1.50086468 s
        ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
        ```
        !!! note
            Values of `ARGS: (22,)` and `KWARGS: {}` are printed.

            This setting is important foe when you are measuring execution
            times of the same functions but passing varying arguments.
            That way you c`an see how each argument affects execution time.


    """

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
