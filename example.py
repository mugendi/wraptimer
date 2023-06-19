import asyncio
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

print("response:", test_by_line())
print("response:", asyncio.run(test_by_line_async()))

print("response:", test_func(200))
print("response:", asyncio.run(test_func_async(200)))
