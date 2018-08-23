"""
eval.py

Loads in an Addition NPI, and starts a REPL for interactive bubblesort.
"""
from model.npi import NPI
from tasks.bubblesort.bubblesort import BubblesortCore
from tasks.bubblesort.env.config import CONFIG, get_args, PROGRAM_SET, ScratchPad
import numpy as np
import pickle
import tensorflow as tf




LOG_PATH = "tasks/bubblesort/log/"
CKPT_PATH = "tasks/bubblesort/log/model.ckpt"
TEST_PATH = "tasks/bubblesort/data/test.pik"
MOVE_PTR_PID, SWAP_ELEM_PID = 8, 7
W_PTRS = {0: "PTR_1", 1: "PTR_2"}
PTRS = {0: "IN_ARRAY", 1: "PTR_1", 2: "PTR_2", 3: "PTR_COUNTER"}
DRC = {0: "LEFT", 1: "RIGHT"}


def evaluate_bubblesort():
    """
    Load NPI Model from Checkpoint, and initialize REPL, for interactive bubblesort.
    """
    with tf.Session() as sess:
        # Load Data
        with open(TEST_PATH, 'rb') as f:
            data = pickle.load(f)

        # Initialize Addition Core
        print('initializing bubblesort core ...')
        core = BubblesortCore()

        # Initialize NPI Model
        print('initializing npi model ...')
        npi = NPI(core, CONFIG, LOG_PATH)

        # Restore from Checkpoint
        saver = tf.train.Saver()
        saver.restore(sess, CKPT_PATH)

        # Run REPL
        repl(sess, npi, data)


def repl(session, npi, data):
    while True:
        inpt = input('Enter An Array, or Hit Enter for Random Pair: ')

        if inpt == "":
            eval_arr, _ = data[np.random.randint(len(data))]

        else:
            eval_arr = inpt.split(",")


        # Reset NPI States
        print ("")
        npi.reset_state()

        # Setup Environment
        scratch = ScratchPad(eval_arr)
        prog_name, prog_id, arg, term = 'BUBBLESORT', 0, [], False

        cont = 'c'
        while cont == 'c' or cont == 'C':
            # Print Step Output
            # if prog_id == MOVE_PTR_PID:
            #     a0, a1, a2 = PTRS.get(arg[0], "OOPS!"), PTRS.get(arg[1], "OOPS!"), PTRS.get(arg[2], "OOPS!"),
            #     a_str = "[%s, %s, %s]" % (str(a0), str(a1), str(a2))
            # elif prog_id == SWAP_ELEM_PID:
            #     a0, a1 = W_PTRS[arg[0]], W_PTRS[arg[1]]
            #     a_str = "[%s, %s, %s]" % (str(a0), str(a1), str(a2))
            # else:
            #     a_str = "[None, None, None]"

            a_str = str(arg)

            # print ('Step: %s, Arguments: %s, Terminate: %s' % (prog_name, a_str, str(term)))
            # print ('IN ARRAY: %s, PTR 1: %s, PTR 2: %s, PTR COUNTER: %s' % (scratch[0],
            #                                                   scratch.ptr_1[1],
            #                                                   scratch.ptr_2[1],
            #                                                   scratch.ptr_counter[1]))

            # Update Environment if MOVE or SWAP
            if prog_id == MOVE_PTR_PID or prog_id == SWAP_ELEM_PID:
                # print("DETERMINED: ", prog_id, prog_name, arg)
                scratch.execute(prog_id, arg)

            # Print Environment
            scratch.pretty_print()

            # Get Environment, Argument Vectors
            env_in, arg_in, prog_in = [scratch.get_env()], [get_args(arg, arg_in=True)], [[prog_id]]
            t, n_p, n_args = session.run([npi.terminate, npi.program_distribution, npi.arguments],
                                         feed_dict={npi.env_in: env_in, npi.arg_in: arg_in,
                                                    npi.prg_in: prog_in})



            if np.argmax(t) == 1:
                # print ('Step: %s, Arguments: %s, Terminate: %s' % (prog_name, a_str, str(True)))
                # print('IN ARRAY: %s, PTR 1: %s, PTR 2: %s, PTR COUNTER: %s' % (scratch[1],
                #                                                                scratch.ptr_1[1],
                #                                                                scratch.ptr_2[1],
                #                                                                scratch.ptr_counter[1]))


                # Update Environment if MOVE or SWAP
                if prog_id == MOVE_PTR_PID or prog_id == SWAP_ELEM_PID:
                    scratch.execute(prog_id, arg)

                # Print Environment
                scratch.pretty_print()


                output = scratch[0]
                print ("Model Output: %s ==> %s" % (eval_arr, output))
                print ("Correct Out : %s" % (eval_arr.sort()))
                print ("Correct!" if output == eval_arr.sort() else "Incorrect!")

            else:
                prog_id = np.argmax(n_p)
                prog_name = PROGRAM_SET[prog_id][0]

                # print("N_ARGS", n_args)
                if prog_id == MOVE_PTR_PID or prog_id == SWAP_ELEM_PID:
                    arg = [np.argmax(n_args[0]), np.argmax(n_args[1]), np.argmax(n_args[2])]
                    # print("ARG CHANGE: ", arg)
                else:
                    arg = []
                    # print("ARG NO CHANGE: ", arg)
                term = False

                # cont = input('Continue? ')
                cont = "c"