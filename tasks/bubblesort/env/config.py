"""
config.py

Configuration Variables for the Bubblesort NPI Task => Stores Scratch-Pad Dimensions, Vector/Program
Embedding Information, etc.
"""
import numpy as np
import sys
import time

CONFIG = {
    "ENVIRONMENT_ROW": 4,         # In_array, Pointer 1, Pointer 2, Counter
    "ENVIRONMENT_COL": 20,        # Array length=20 Maximum for Bubblesort Task
    "ENVIRONMENT_DEPTH": 10,      # Size of each element vector => One-Hot, Options: 0-9

    "ARGUMENT_NUM": 3,            # Maximum Number of Program Arguments
    "ARGUMENT_DEPTH": 11,         # Size of Argument Vector => One-Hot, Options 0-9, Default (10)
    "DEFAULT_ARG_VALUE": 10,      # Default Argument Value

    "PROGRAM_NUM": 9,             # Maximum Number of Subroutines
    "PROGRAM_KEY_SIZE": 8,        # Size of the Program Keys
    "PROGRAM_EMBEDDING_SIZE": 10  # Size of the Program Embeddings
}

PROGRAM_SET = [
    ("BUBBLESORT",),          # Perform bubble sort (ascending order)
    ("BUBBLE",),              # Perform one sweep of pointers left to right
    ("RESET",),               # Move both pointers all the way left
    ("BSTEP",),               # Conditionally swap and advance pointers
    ("COMPSWAP",),            # Conditionally swap two elements
    ("LSHIFT",),              # Shift a specified pointer one step left
    ("RSHIFT",),              # Shift a specified pointer one step right
    ("SWAP",),                # Swap two values at pointer locations
    ("PTR",),                 # Move pointer
]

PROGRAM_ID = {x[0]: i for i, x in enumerate(PROGRAM_SET)}


class ScratchPad:           # Bubblesort Environment
    def __init__(self, in_array, rows=CONFIG["ENVIRONMENT_ROW"], cols=CONFIG["ENVIRONMENT_COL"]):
        # Setup Internal ScratchPad
        self.rows, self.cols = rows, cols
        self.in_array = in_array
        self.scratchpad = np.zeros((self.rows, self.cols), dtype=np.int8)
        self.sttime = 1
        self.stct = 1

        # Initialize ScratchPad In_array
        self.init_scratchpad(in_array)
        # print("SCRATCHPAD: ", self.scratchpad)

        # Pointers initially all start at the left
        self.ptr_1, self.ptr_2, self.ptr_counter = [(x + 1, 0) for x in range(3)]
        self.ptrs = [self.in_array, self.ptr_1, self.ptr_2, self.ptr_counter]

    def init_scratchpad(self, in_array):
        """
        Initialize the scratchpad with the given input array (to be added sorted).
        """
        for inpt in range(len(in_array)):
            self.scratchpad[0, inpt] = int(in_array[inpt])

    def done(self):
        if self.ptr_counter[1] == self.cols - 1:
            return True
        else:
            return False


    def swap(self, args, debug=False):
        if self.scratchpad[0][self.ptr_1[1]] > self.scratchpad[0][self.ptr_2[1]]:
            # print("SWAP SUBROUTINE")

            self.scratchpad[0][self.ptr_1[1]], self.scratchpad[0][self.ptr_2[1]] = \
                self.scratchpad[0][self.ptr_2[1]], self.scratchpad[0][self.ptr_1[1]]

            # self.pretty_print()

            if debug:
                self.pretty_print()

            return True

        else:
            return False

    def ptr(self, args, debug=False):

        if args[0] == 0:
            print("Error: Direction applied to array")
        elif args[0] == 1:
            self.ptr_1 = (self.ptr_1[0], self.ptr_1[1] + 2 * args[2] - 1 )

            if self.ptr_1[1] < 0:
                self.ptr_1 = (self.ptr_1[0], 0)
            elif self.ptr_1[1] >= self.cols:
                self.ptr_1 = (self.ptr_1[0], self.cols - 1)

        elif args[0] == 2:
            self.ptr_2 = (self.ptr_2[0], self.ptr_2[1] + 2 * args[2] - 1  )

            if self.ptr_2[1] < 0:
                self.ptr_2 = (self.ptr_2[0], 0)
            elif self.ptr_2[1] >= self.cols:
                self.ptr_2 = (self.ptr_2[0], self.cols - 1)

        elif args[0] == 3:
            self.ptr_counter = (self.ptr_counter[0], self.ptr_counter[1] + 2 * args[2] - 1  )

            if self.ptr_counter[1] < 0:
                self.ptr_counter = (self.ptr_counter[0], 0)
            elif self.ptr_counter[1] >= self.cols:
                self.ptr_counter = (self.ptr_counter[0], self.cols - 1)

        else:
            print("Error: Invalid pointer")

        # self.pretty_print()

        if debug:
            self.pretty_print()

    def pretty_print(self):

        print(self.scratchpad[0])
        print("  " * self.ptr_1[1] + "*")
        print("  " * self.ptr_2[1] + "*")
        print("  " * self.ptr_counter[1] + "*")


        time.sleep(0.03)
        # sys.stdout.flush()

    def get_env(self): #####CHECK!!!
        env = np.zeros((CONFIG["ENVIRONMENT_ROW"], CONFIG["ENVIRONMENT_COL"]), dtype=np.int32)

        env[self.ptr_1] = 1
        env[self.ptr_2] = 1
        env[self.ptr_counter] = 1

        return env.flatten()

    def execute(self, prog_id, args):
        if prog_id == 8:               # MOVE!

            if args[0] == 0:
                print("Error: Trying to move ptr on array")
            elif args[0] == 1:
                self.ptr_1 = (self.ptr_1[0], self.ptr_1[1] + 2 * args[2] - 1  )
            elif args[0] == 2:
                self.ptr_2 = (self.ptr_2[0], self.ptr_2[1] + 2 * args[2] - 1  )
            elif args[0] == 3:
                self.ptr_counter = (self.ptr_counter[0], self.ptr_counter[1] + 2 * args[2] - 1  )
            else:
                raise NotImplementedError
            self.ptrs = [self.in_array, self.ptr_1, self.ptr_2, self.ptr_counter]



            if self.ptr_1[1] < 0:
                self.ptr_1 = (self.ptr_1[0], 0)
            elif self.ptr_1[1] >= self.cols:
                self.ptr_1 = (self.ptr_1[0], self.cols - 1)

            if self.ptr_2[1] < 0:
                self.ptr_2 = (self.ptr_2[0], 0)
            elif self.ptr_2[1] >= self.cols:
                self.ptr_2 = (self.ptr_2[0], self.cols - 1)

            if self.ptr_counter[1] < 0:
                self.ptr_counter = (self.ptr_counter[0], 0)
            elif self.ptr_counter[1] >= self.cols:
                self.ptr_counter = (self.ptr_counter[0], self.cols - 1)



        elif prog_id == 7:             # WRITE!

            self.scratchpad[0][self.ptr_1[1]], self.scratchpad[0][self.ptr_2[1]] = \
                self.scratchpad[0][self.ptr_2[1]], self.scratchpad[0][self.ptr_1[1]]


        self.pretty_print()



    def __getitem__(self, item):
        return self.scratchpad[item]

    def __setitem__(self, key, value):
        self.scratchpad[key] = value


class Arguments():             # Program Arguments
    def __init__(self, args, num_args=CONFIG["ARGUMENT_NUM"], arg_depth=CONFIG["ARGUMENT_DEPTH"]):
        self.args = args
        self.arg_vec = np.zeros((num_args, arg_depth), dtype=np.float32)


def get_args(args, arg_in=True):
    if arg_in:
        arg_vec = np.zeros((CONFIG["ARGUMENT_NUM"], CONFIG["ARGUMENT_DEPTH"]), dtype=np.int32)
    else:
        arg_vec = [np.zeros((CONFIG["ARGUMENT_DEPTH"]), dtype=np.int32) for _ in
                   range(CONFIG["ARGUMENT_NUM"])]
    if len(args) > 0:
        for i in range(CONFIG["ARGUMENT_NUM"]):
            if i >= len(args):
                arg_vec[i][CONFIG["DEFAULT_ARG_VALUE"]] = 1
            else:
                arg_vec[i][args[i]] = 1
    else:
        for i in range(CONFIG["ARGUMENT_NUM"]):
            arg_vec[i][CONFIG["DEFAULT_ARG_VALUE"]] = 1
    return arg_vec.flatten() if arg_in else arg_vec

