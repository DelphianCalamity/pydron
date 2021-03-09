import pydron
import math
import time


@pydron.functional
def foo(num):
    time.sleep(5)
    return num
    # return num + math.log(num)


@pydron.schedule
def calibration_pipeline(inputs):
    outputs = []
    for num in inputs:
        output = foo(num)
        outputs = outputs + [output]
    return outputs


if __name__ == '__main__':
    start = time.time()
    vals = [n for n in range(10)]
    print(calibration_pipeline(vals))
    end = time.time()
    print(end - start)
