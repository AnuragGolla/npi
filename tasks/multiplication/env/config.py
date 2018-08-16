"""
config.py

Configuration Variables for the Multiplication NPI Task => Stores Scratch-Pad Dimensions, Vector/Program
Embedding Information, etc.
"""
import numpy as np
import sys
import time

CONFIG = {
    "ENVIRONMENT_ROW": 14,         # Input 1, Input 2, Carry and Output (5), Final Carry, Final Output
    "ENVIRONMENT_COL": 10,        # 10-Digit Maximum for Multiplication Task
    "ENVIRONMENT_DEPTH": 10,      # Size of each element vector => One-Hot, Options: 0-9

    "ARGUMENT_NUM": 3,            # Maximum Number of Program Arguments
    "ARGUMENT_DEPTH": 15,         # Size of Argument Vector => One-Hot, Options 0-13, Default (14)
    "DEFAULT_ARG_VALUE": 10,      # Default Argument Value

    "PROGRAM_NUM": 13,             # Maximum Number of Subroutines  ##########CHECK
    "PROGRAM_KEY_SIZE": 12,        # Size of the Program Keys #########CHECK
    "PROGRAM_EMBEDDING_SIZE": 10  # Size of the Program Embeddings
}

PROGRAM_SET = [
    ("MULTIPLY",),
    ("MULSTAGE",),
    ("MULTIPLY1",),
    ("MULSHIFT",),
    ("MULCARRY",),
    ("MULWRITE",),
    ("MULPTR",),
    ("ADD",),
    ("ADD1",),
    ("ADDSHIFT",),
    ("ADDCARRY",),
    ("ADDWRITE",),
    ("ADDPTR",),
]

PROGRAM_ID = {x[0]: i for i, x in enumerate(PROGRAM_SET)}


class ScratchPad():           # Mulitplication Environment
    def __init__(self, in1, in2, rows=CONFIG["ENVIRONMENT_ROW"], cols=CONFIG["ENVIRONMENT_COL"]):
        # Setup Internal ScratchPad
        self.rows, self.cols = rows, cols
        self.in1, self.in2 = in1, in2
        self.scratchpad = np.zeros((self.rows, self.cols), dtype=np.int8)
        self.adddone_bool = False

        # Initialize ScratchPad In1, In2
        self.init_scratchpad(in1, in2)

        # Pointers initially all start at the right
        self.ptr_in1, self.ptr_in2, self.ptr_c1, self.ptr_c2, self.ptr_c3, self.ptr_c4, \
            self.ptr_c5, self.ptr_o1, self.ptr_o2, self.ptr_o3, self.ptr_o4, self.ptr_o5, \
            self.ptr_cf, self.ptr_of = [(x, -1) for x in range(self.rows)]

        self.ptrs = [self.ptr_in1, self.ptr_in2, self.ptr_c1, self.ptr_c2, self.ptr_c3, self.ptr_c4, \
            self.ptr_c5, self.ptr_o1, self.ptr_o2, self.ptr_o3, self.ptr_o4, self.ptr_o5, \
            self.ptr_cf, self.ptr_of]

    def init_scratchpad(self, in1, in2):
        """
        Initialize the scratchpad with the given input numbers (to be added together).
        """
        lst = [str(in1), str(in2)]
        for inpt in range(len(lst)):
            for i in range(1, len(lst[inpt]) + 1):
                self.scratchpad[inpt, -i] = int(lst[inpt][-i])
        # print(self.scratchpad)


    def mulstagedone(self):
        # stages = len(str(self.in1))
        if self.ptr_o5[1] == - self.cols - 1:
            return True
        else:
            return False

    def getstage(self, typ):
        stage = - self.ptr_in2[1]
        stages_carry = {
            1: self.ptr_c1,
            2: self.ptr_c2,
            3: self.ptr_c3,
            4: self.ptr_c4,
            5: self.ptr_c5,
            6: self.ptr_cf
        }
        stages_out = {
            1: self.ptr_o1,
            2: self.ptr_o2,
            3: self.ptr_o3,
            4: self.ptr_o4,
            5: self.ptr_o5,
            6: self.ptr_of
        }

        if typ == "carry":
            return stages_carry[stage]
        elif typ == "out":
            return stages_out[stage]
        else:
            raise TypeError



    def multiply1(self):
        carry_ptr = self.getstage("carry")
        temp = self[self.ptr_in1] * self[self.ptr_in2] + self[carry_ptr]

        return temp % 10, temp // 10

    def mulptr(self, args, debug):

        if args[0] == 0:
            self.ptr_in1 = self.ptr_in1[0], self.ptr_in1[1] + 2 * args[2] - 1
        elif args[0] == 1:
            self.ptr_in2 = self.ptr_in2[0], self.ptr_in2[1] + 2 * args[2] - 1
        elif args[0] == 2:
            self.ptr_c1 = self.ptr_c1[0], self.ptr_c1[1] + 2 * args[2] - 1
        elif args[0] == 3:
            self.ptr_c2 = self.ptr_c2[0], self.ptr_c2[1] + 2 * args[2] - 1
        elif args[0] == 4:
            self.ptr_c3 = self.ptr_c3[0], self.ptr_c3[1] + 2 * args[2] - 1
        elif args[0] == 5:
            self.ptr_c4 = self.ptr_c4[0], self.ptr_c4[1] + 2 * args[2] - 1
        elif args[0] == 6:
            self.ptr_c5 = self.ptr_c5[0], self.ptr_c5[1] + 2 * args[2] - 1
        elif args[0] == 7:
            self.ptr_o1 = self.ptr_o1[0], self.ptr_o1[1] + 2 * args[2] - 1
        elif args[0] == 8:
            self.ptr_o2 = self.ptr_o2[0], self.ptr_o2[1] + 2 * args[2] - 1
        elif args[0] == 9:
            self.ptr_o3 = self.ptr_o3[0], self.ptr_o3[1] + 2 * args[2] - 1
        elif args[0] == 10:
            self.ptr_o4 = self.ptr_o4[0], self.ptr_o4[1] + 2 * args[2] - 1
        elif args[0] == 11:
            self.ptr_o5 = self.ptr_o5[0], self.ptr_o5[1] + 2 * args[2] - 1
        elif args[0] == 12:
            self.ptr_cf = self.ptr_cf[0], self.ptr_cf[1] + 2 * args[2] - 1
        elif args[0] == 13:
            self.ptr_of = self.ptr_of[0], self.ptr_of[1] + 2 * args[2] - 1


        # self.pretty_print()


    def mulwrite(self, args, debug):
        val = args[2]
        if args[1] == 0:
            self[(args[0], self.ptr_in1[1] + self.ptr_in2[1] + 1)] = val
        else:
            self[(args[0], self.ptr_in1[1] + self.ptr_in2[1])] = val

        # self.pretty_print()

    def mulshift(self):
        self.ptrs_mulshift = [self.ptr_in1, self.ptr_c1, self.ptr_c2, self.ptr_c3, self.ptr_c4,
                              self.ptr_c5, self.ptr_o1, self.ptr_o2, self.ptr_o3, self.ptr_o4, self.ptr_o5]

        self.ptr_in1, self.ptr_c1, self.ptr_c2, self.ptr_c3, self.ptr_c4, self.ptr_c5, \
            self.ptr_o1, self.ptr_o2, self.ptr_o3, self.ptr_o4, self.ptr_o5 = [(x, y - 1) for (x, y) in self.ptrs_mulshift]

    def mulstageshift(self):

        self.ptrs_mulstageshift = [self.ptr_c1, self.ptr_c2, self.ptr_c3, self.ptr_c4,
                              self.ptr_c5, self.ptr_o1, self.ptr_o2, self.ptr_o3, self.ptr_o4, self.ptr_o5]

        self.ptr_in2 = (self.ptr_in2[0], self.ptr_in2[1] - 1)
        self.ptr_in1 = self.ptr_in1[0], -1

        self.ptr_c1, self.ptr_c2, self.ptr_c3, self.ptr_c4, self.ptr_c5, \
            self.ptr_o1, self.ptr_o2, self.ptr_o3, self.ptr_o4, self.ptr_o5 = [(x, self.ptr_in2[1]) for (x, y) in self.ptrs_mulstageshift]



    def muldone(self):
        return True if self.ptr_in2 == (1, -6) else False


    def add1(self):
        temp = self[self.ptr_o1] + self[self.ptr_o2] + self[self.ptr_o3] + self[self.ptr_o4] + self[self.ptr_o5] + self[self.ptr_cf]

        return temp % 10, temp // 10

    def addwrite(self, args, debug):
        if args[1] == 0:
            self[self.ptr_of] = args[2]
        elif args[1] == 1:
            self[self.ptr_cf[0], self.ptr_cf[1] - 1] = args[2]
        else:
            raise ValueError

        # self.pretty_print()

    def add_shift(self):

        self.ptrs_addshift = [self.ptr_o1, self.ptr_o2, self.ptr_o3, self.ptr_o4, self.ptr_o5, self.ptr_cf, self.ptr_of]

        if self.ptr_of[1] == -10:
            self.ptr_o1, self.ptr_o2, self.ptr_o3, self.ptr_o4, self.ptr_o5, \
                self.ptr_cf, self.ptr_of = [(x, 9) for (x, y) in self.ptrs_addshift]
            return True

        else:
            self.ptr_o1, self.ptr_o2, self.ptr_o3, self.ptr_o4, self.ptr_o5, \
                self.ptr_cf, self.ptr_of = [(x, y - 1) for (x, y) in self.ptrs_addshift]
            return False


    def adddone(self):
        return self.adddone_bool


    def pretty_print(self):
        # new_strs = ["".join(map(str, self[i])) for i in range(4)]
        # line_length = len('Input 1:' + " " * 5 + new_strs[0])
        # print ('Input 1:' + " " * 5 + new_strs[0])
        # print ('Input 2:' + " " * 5 + new_strs[1])
        # print ('Carry  :' + " " * 5 + new_strs[2])
        # print ('-' * line_length)
        # print ('Output :' + " " * 5 + new_strs[3])
        # print ('')


        # print(self.scratchpad)

        self.ptrs = [self.ptr_in1, self.ptr_in2, self.ptr_c1, self.ptr_c2, self.ptr_c3, self.ptr_c4, \
                     self.ptr_c5, self.ptr_o1, self.ptr_o2, self.ptr_o3, self.ptr_o4, self.ptr_o5, \
                     self.ptr_cf, self.ptr_of]

        for x in self.ptrs:
            loc = 1 + self.cols + x[1]
            invLoc = self.cols - loc
            print(" _ " * loc, x[1], " _ " * invLoc)

        print("----------------------------------")


        time.sleep(0.03)
        # sys.stdout.flush()


    def initAdd(self):

        self.ptrs_initAdd = [self.ptr_o1, self.ptr_o2, self.ptr_o3, self.ptr_o4, self.ptr_o5, self.ptr_cf, self.ptr_of]

        self.ptr_o1, self.ptr_o2, self.ptr_o3, self.ptr_o4, self.ptr_o5, self.ptr_cf, \
            self.ptr_of = [(x, -1) for (x, y) in self.ptrs_initAdd]




    def get_env(self):
        env = np.zeros((CONFIG["ENVIRONMENT_ROW"], CONFIG["ENVIRONMENT_DEPTH"]), dtype=np.int32)

        if self.ptr_in1[1] < -CONFIG["ENVIRONMENT_COL"]:
            env[0][0] = 1
        else:
            env[0][self[self.ptr_in1]] = 1
        if self.ptr_in2[1] < -CONFIG["ENVIRONMENT_COL"]:
            env[1][0] = 1
        else:
            env[1][self[self.ptr_in2]] = 1
        if self.ptr_c1[1] < -CONFIG["ENVIRONMENT_COL"]:
            env[2][0] = 1
        else:
            env[2][self[self.ptr_c1]] = 1
        if self.ptr_c2[1] < -CONFIG["ENVIRONMENT_COL"]:
            env[3][0] = 1
        else:
            env[3][self[self.ptr_c2]] = 1
        if self.ptr_c3[1] < -CONFIG["ENVIRONMENT_COL"]:
            env[4][0] = 1
        else:
            env[4][self[self.ptr_c3]] = 1
        if self.ptr_c4[1] < -CONFIG["ENVIRONMENT_COL"]:
            env[5][0] = 1
        else:
            env[5][self[self.ptr_c4]] = 1
        if self.ptr_c5[1] < -CONFIG["ENVIRONMENT_COL"]:
            env[6][0] = 1
        else:
            env[6][self[self.ptr_c5]] = 1
        if self.ptr_o1[1] < -CONFIG["ENVIRONMENT_COL"]:
            env[7][0] = 1
        else:
            env[7][self[self.ptr_o1]] = 1
        if self.ptr_o2[1] < -CONFIG["ENVIRONMENT_COL"]:
            env[8][0] = 1
        else:
            env[8][self[self.ptr_o2]] = 1
        if self.ptr_o3[1] < -CONFIG["ENVIRONMENT_COL"]:
            env[9][0] = 1
        else:
            env[9][self[self.ptr_o3]] = 1
        if self.ptr_o4[1] < -CONFIG["ENVIRONMENT_COL"]:
            env[10][0] = 1
        else:
            env[10][self[self.ptr_o4]] = 1
        if self.ptr_o5[1] < -CONFIG["ENVIRONMENT_COL"]:
            env[11][0] = 1
        else:
            env[11][self[self.ptr_o5]] = 1
        if self.ptr_cf[1] < -CONFIG["ENVIRONMENT_COL"]:
            env[12][0] = 1
        else:
            env[12][self[self.ptr_cf]] = 1
        if self.ptr_of[1] < -CONFIG["ENVIRONMENT_COL"]:
            env[13][0] = 1
        else:
            env[13][self[self.ptr_of]] = 1

        return env.flatten()




    def execute(self, prog_id, args):

        ptr, woc, dirVal = args[0], args[1], args[2]

        # self.pretty_print()

        if prog_id == 5 or prog_id == 11:                # MULWRITE/ADDWRITE [PTR, W/C, Val]
            if ptr == 0:
                self[self.ptr_in1] = dirVal
            elif ptr == 1:
                self[self.ptr_in2] = dirVal
            elif ptr == 2:
                self[self.ptr_c1] = dirVal
            elif ptr == 3:
                self[self.ptr_c2] = dirVal
            elif ptr == 4:
                self[self.ptr_c3] = dirVal
            elif ptr == 5:
                self[self.ptr_c4] = dirVal
            elif ptr == 6:
                self[self.ptr_c5] = dirVal
            elif ptr == 7:
                self[self.ptr_o1] = dirVal
            elif ptr == 8:
                self[self.ptr_o2] = dirVal
            elif ptr == 9:
                self[self.ptr_o3] = dirVal
            elif ptr == 10:
                self[self.ptr_o4] = dirVal
            elif ptr == 11:
                self[self.ptr_o5] = dirVal
            elif ptr == 12:
                self[self.ptr_cf] = dirVal
            elif ptr == 13:
                self[self.ptr_of] = dirVal
            else:
                raise NotImplementedError

        elif prog_id == 6 or prog_id == 12:              # MULPTR/ADDPTR [PTR, None, L/R]
            lr = 2 * dirVal - 1
            if ptr == 0:
                self.ptr_in1 = self.ptr_in1[0], self.ptr_in1[1] + lr
            elif ptr == 1:
                self.ptr_in2 = self.ptr_in2[0], self.ptr_in2[1] + lr
            elif ptr == 2:
                self.ptr_c1 = self.ptr_c1[0], self.ptr_c1[1] + lr
            elif ptr == 3:
                self.ptr_c2 = self.ptr_c2[0], self.ptr_c2[1] + lr
            elif ptr == 4:
                self.ptr_c3 = self.ptr_c3[0], self.ptr_c3[1] + lr
            elif ptr == 5:
                self.ptr_c4 = self.ptr_c4[0], self.ptr_c4[1] + lr
            elif ptr == 6:
                self.ptr_c5 = self.ptr_c5[0], self.ptr_c5[1] + lr
            elif ptr == 7:
                self.ptr_o1 = self.ptr_o1[0], self.ptr_o1[1] + lr
            elif ptr == 8:
                self.ptr_o2 = self.ptr_o2[0], self.ptr_o2[1] + lr
            elif ptr == 9:
                self.ptr_o3 = self.ptr_o3[0], self.ptr_o3[1] + lr
            elif ptr == 10:
                self.ptr_o4 = self.ptr_o4[0], self.ptr_o4[1] + lr
            elif ptr == 11:
                self.ptr_o5 = self.ptr_o5[0], self.ptr_o5[1] + lr
            elif ptr == 12:
                self.ptr_cf = self.ptr_cf[0], self.ptr_cf[1] + lr
            elif ptr == 13:
                self.ptr_of = self.ptr_of[0], self.ptr_of[1] + lr
            else:
                raise NotImplementedError





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

