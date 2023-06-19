"""
 Copyright (c) 2023 Anthony Mugendi
 
 This software is released under the MIT License.
 https://opensource.org/licenses/MIT
"""
import asyncio
import os
import sys
from functools import wraps

from termcolor import colored

from .timer import Timer

try:
    term_size = os.get_terminal_size()
    term_size = term_size.columns
except Exception:
    term_size = 80


class DebugContext:
    """Debug context to trace any function calls inside the context"""

    tracers = {}

    def __init__(self, name, func, verbose=True):
        self.verbose = verbose
        self.name = name
        self.func = func
        self.tracers[self.name] = sys.settrace
        self.t = Timer()
        self.traced = []
        self.line_count = 0

    def __enter__(self):
        # print(f"Entering Debug Decorated func {self.name}")
        # Set the trace function to the trace_calls function
        # So all events are now traced
        self.tracers[self.name](self.trace_calls)

    def __exit__(self, *args, **kwargs):
        # Stop tracing all events
        self.tracers[self.name] = None

    def trace_calls(self, frame, event, arg):
        # We want to only trace our call to the decorated function
        if event != "call":
            return
        elif frame.f_code.co_name != self.name:
            return
        # return the trace function to use when you go into that

        self.t.start()
        # function call
        return self.trace_lines

    def trace_lines(self, frame, event, arg):
        # If you want to print local variables each line
        # keep the check for the event 'line'
        # If you want to print local variables only on return
        # check only for the 'return' event

        if event not in ["line"] or frame.f_lasti == 0:
            return

        took = 0

        if not self.t._is_started:
            self.t.start()
        else:
            self.t.stop()
            took = self.t.time_string
            self.t.start()

        # self.t.stop()
        # pprint(dir(frame))
        # if frame.f_lasti==0:
        co = frame.f_code
        func_name = co.co_name
        line_no = frame.f_lineno - 1
        # filename = co.co_filename
        # local_vars = frame.f_lo

        func_type = "ASYNC" if asyncio.iscoroutinefunction(self.func) else "SYNC"

        self.traced.append(
            {
                f"{func_type} FUNC": func_name,
                "LINE": line_no,
                "TOOK": took,
            }
        )

        self.line_count += 1

        # if verbose, log
        if self.verbose:
            draw_sep = None
            line_str = f"LINE: {line_no}, "

            if self.line_count == 1:
                draw_sep = "top"

            log(
                what=line_str,
                t=took,
                draw_sep=draw_sep,
                title=f"{func_type} FUNC: {func_name}",
            )


class TimeIt:
    def __init__(self, verbose: bool = True, show_args: bool = False):
        self.verbose = verbose
        self.show_args = show_args

    def byline(self, func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            """Debug decorator to call the function within the debug context"""
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

    def func(self, func):
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


def log(
    what,
    t,
    title=None,
    args=None,
    kwargs=None,
    show_args=False,
    return_trace=False,
    draw_sep=False,
):
    # print(what, return_trace)
    what_str = ""
    if callable(what):
        func_type = "ASYNC" if asyncio.iscoroutinefunction(what) else "SYNC"
        what_str = ""
        title = f"{func_type} FUNC: {what.__name__}"
    else:
        what_str = what

    t_str = t.time_string if isinstance(t, Timer) else t

    log_arr = []

    if show_args:
        args = (
            [f" ARGS: {args}", f" KWARGS: {kwargs}"]
            if return_trace
            else [
                colored(f" ARGS: {args}", "cyan"),
                colored(f" KWARGS: {kwargs}", "cyan"),
            ]
        )

        log_arr = log_arr + args

    if return_trace:
        log_arr.append(f" {what_str}TOOK: {t_str}")
        return log_arr
    else:
        color = "white" if "LINE" in what_str else "blue"
        attrs = ["bold"] if color != "white" else []
        log_arr.append(colored(f" {what_str}TOOK: {t_str}", color, attrs=attrs))

        # print(log_arr)
        draw_sep = [draw_sep] if not isinstance(draw_sep, list) else draw_sep
        sep_color = "dark_grey"

        if "all" in draw_sep or "top" in draw_sep:
            if title:
                center_len = int((term_size - (len(title) + 6)) / 2)
                sep_str = colored("━" * center_len, sep_color)
                sep_str = (
                    sep_str + colored(f" [ {title} ] ", "blue", attrs=["bold"]) + sep_str
                )
            else:
                sep_str = "━" * term_size

            print()
            print(sep_str)

        if "all" in draw_sep or "mid" in draw_sep:
            print(" " + colored("-" * (term_size - 2), sep_color) + " ")

        print("\n".join(log_arr))

        if "all" in draw_sep or "bottom" in draw_sep:
            print(colored("━" * term_size, sep_color))
            print()
