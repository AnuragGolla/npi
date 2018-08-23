"""
generate_data.py

Core script for generating training/test bubblesort data. First, generates random arrays of numbers,
then steps through an execution trace, computing the exact order of subroutines that need to be
called.
"""
import pickle

import numpy as np

from tasks.bubblesort.env.trace import Trace
from tasks.bubblesort.env.config import CONFIG


def generate_bubblesort(prefix, curriculum_size, debug=False, maximum=10000000000, debug_every=10,
                        elem_size=CONFIG["ENVIRONMENT_DEPTH"], array_len=CONFIG["ENVIRONMENT_COL"]):

    """
    Generates bubblesort data with the given string prefix (i.e. 'train', 'test') and the specified
    number of examples.

    :param prefix: String prefix for saving the file ('train', 'test')
    :param num_examples: Number of examples to generate.

    """
    #
    # data = []
    # for i in range(curriculum_size):
    #     in_arr = np.zeros(array_len, dtype=np.int)
    #     for j in range(array_len):
    #         in_arr[j] = np.random.randint(elem_size)
    #
    #     if debug and i % debug_every == 0:
    #         trace = Trace(in_arr, True).trace
    #     else:
    #         trace = Trace(in_arr).trace
    #     data.append(( in_arr, trace ))




    class_size = curriculum_size // array_len
    data = []
    for i in range(1, array_len+1):
        for j in range(class_size):
            in_arr = np.zeros(i, dtype=np.int)
            for k in range(array_len):
                in_arr[k] = np.random.randint(elem_size)

            if debug and j % debug_every == 0:
                trace = Trace(in_arr, True).trace
            else:
                trace = Trace(in_arr).trace
            data.append((in_arr, trace))


    with open('tasks/bubblesort/data/{}.pik'.format(prefix), 'wb') as f:
        pickle.dump(data, f)