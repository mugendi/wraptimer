<!--
 Copyright (c) 2023 Anthony Mugendi
 
 This software is released under the MIT License.
 https://opensource.org/licenses/MIT
-->

# wraptimer

[![github-watchers](https://img.shields.io/github/watchers/mugendi/wraptimer?label=Watch&style=social&logo=github)](https://github.com/mugendi/wraptimer)
[![github-stars](https://img.shields.io/github/stars/mugendi/wraptimer?style=social&logo=github)](https://github.com/mugendi/wraptimer)
[![github-forks](https://img.shields.io/github/forks/mugendi/wraptimer?label=Fork&style=social&logo=github)](https://github.com/mugendi/wraptimer)

- 📖 [Documentation](https://mugendi.github.io/wraptimer/)


An amazing alternative to Python's builtin `timeit` module that allows for high resolution timing of functions as well as in-depth line-by-line timing. It also exposes convenient classes to measure execution time for any arbitrary code.

<!-- 
To generate recording, run

asciinema rec -c "python example.py" docs/images/recording.cast 

ttygif --input docs/images/recording.cast --output docs/images/recording.gif --fps 60 --speed 1 --theme mac --title "Running >> python example.py

 -->
![](./docs/images/recording.gif) ![](./images/recording.gif)

### Sync function example
```python
# imports
import time
from wraptimer import TimeIt
# Init
timeit = TimeIt()

# decorate
@timeit.byline
def test_by_line():
    a = 10
    b = 20
    time.sleep(0.8)
    c = a + b

    return [a, b, c]

# run
test_by_line()
```
![](docs/images/sync-screenshot.png) ![](images/sync-screenshot.png)


### Async function example
```python
# Imports
import asyncio
from wraptimer import TimeIt
# Init
timeit = TimeIt()

# decorate
@timeit.byline
async def test_by_line_async():
    a = 10
    b = 20
    await asyncio.sleep(1.25)

    return [a, b]

# run
asyncio.run(test_by_line_async()) 
```
![](docs/images/async-screenshot.png) ![](images/async-screenshot.png)


## Don't need Line-by-line tracing?
Use `@timeit.func` if you do not want to print **line-by-line** durations.

```python
...
@timeit.func
async def test_by_line_async():
    a = 10
    b = 20
    await asyncio.sleep(1.25)

    return [a, b]
```

![](docs/images/func-screenshot.png) ![](images/func-screenshot.png)


## Read the documentation
For more about wraptimer, [Read The Documentation](https://mugendi.github.io/wraptimer/)




