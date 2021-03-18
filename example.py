import pydron
import math
import time


@pydron.functional
def foo1(num, delay):
    time.sleep(delay)
    return num


@pydron.functional
def foo2(num, delay):
    time.sleep(delay)
    return num


def control(inputs, delay):
    outputs = []
    for num in inputs:
        output = foo1(num, delay) + foo2(num, delay)
        outputs = outputs + [output]
    return outputs


@pydron.schedule
def experiment1(inputs, delay):
    # var = var + [v]
    outputs = []
    for num in inputs:
        output = foo1(num, delay) + foo2(num, delay)
        outputs = outputs + [output]

    return outputs


@pydron.schedule
def experiment2(inputs, delay):
    # var += [v]
    outputs = []
    for num in inputs:
        output = foo1(num, delay) + foo2(num, delay)
        outputs += [output]

    return outputs


@pydron.schedule
def experiment3(inputs, delay):
    # var[i] = v
    outputs = [0] * len(inputs)
    for i in range(len(inputs)):
        num = inputs[i]
        output = foo1(num, delay) + foo2(num, delay)
        outputs[i] = output

    return outputs


@pydron.schedule
def experiment4(inputs, delay):  # TODO doesn't work with pydron
    # v.append(v)
    outputs = []
    for i in range(len(inputs)):
        num = inputs[i]
        output = foo1(num, delay) + foo2(num, delay)
        outputs.append(output)

    return outputs


def test_iteration_times(vals, min_delay, max_delay):
    # for expensive loops, parallelized runtime ~= 3x iteration runtime
    control_times = []
    exp_times = []

    while min_delay < max_delay:
        min_delay *= 2

        # start = time.time()
        # control(vals, min_delay)
        # end = time.time()
        # control_times.append(end - start)

        start = time.time()
        experiment1(vals, min_delay)
        end = time.time()
        exp_times.append(end - start)
        print(min_delay, end - start, (end - start) / min_delay)

    # print(control_times)
    # print(exp_times)


def test_append_methods(vals, test_num, delay):
    # for expensive loops, exp1 >> exp2 ~ exp3 > control
    # exp2/exp3 are pydron synchronization points
    control_times = []
    exp1_times = []
    exp2_times = []
    exp3_times = []

    for _ in range(test_num):
        start = time.time()
        control(vals, delay)
        end = time.time()
        control_times.append(end - start)

        start = time.time()
        experiment1(vals, delay)
        end = time.time()
        exp1_times.append(end - start)

        start = time.time()
        experiment2(vals, delay)
        end = time.time()
        exp2_times.append(end - start)

        start = time.time()
        experiment3(vals, delay)
        end = time.time()
        exp3_times.append(end - start)

    print(control_times)
    print(exp1_times)
    print(exp2_times)
    print(exp3_times)


if __name__ == '__main__':
    vals = [n for n in range(5)]
    min_delay = .1
    max_delay = 20
    test_num = 10

    test_iteration_times(vals, min_delay, max_delay)
    # test_append_methods(vals, test_num, max_delay)
