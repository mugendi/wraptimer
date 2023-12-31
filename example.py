import asyncio
import pprint
import time

from wraptimer import TimeIt, Timer

# initialize
t = Timer(timer_type="performance")

# start timer
t.start()
# some long running code
time.sleep(1)
# stop timer
t.stop()
# get duration taken to run
print("took", t.time_string)

timeit = TimeIt()


@timeit.byline
def test_by_line():
    a = 10
    b = 20
    time.sleep(0.8)
    c = a + b

    return [a, b, c]


@timeit.byline
async def test_by_line_async():
    a = 10
    b = 20
    await asyncio.sleep(1.25)

    return [a, b]


@timeit.func
def test_func(v=10):
    time.sleep(1.5)
    x = v * 50

    return x


@timeit.func
async def test_func_async(v=10):
    await asyncio.sleep(2.34)
    x = v * 50

    return x


test_by_line()
print()
asyncio.run(test_by_line_async())

test_by_line()
asyncio.run(test_by_line_async())

test_func(200)
asyncio.run(test_func_async(200))


# init
timeit_non_verbose = TimeIt(verbose=False)


# decorate
@timeit_non_verbose.byline
def test_non_verbose(v=1):
    time.sleep(1.5)
    x = v * 50
    return x


resp = test_non_verbose(22)
pprint.pprint(resp)


timeit_non_verbose = TimeIt(show_args=True)


# decorate
@timeit_non_verbose.byline
def test_non_verbose(v=1):
    time.sleep(1.5)
    x = v * 50
    return x


resp = test_non_verbose(22)
pprint.pprint(resp)
