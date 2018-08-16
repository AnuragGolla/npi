"""
eval.py

Loads in an Mulitplication NPI, and starts a REPL for interactive multiplication.
"""
from model.npi import NPI
from tasks.multiplication.multiplication import MultiplicationCore
from tasks.multiplication.env.config import CONFIG, get_args, PROGRAM_SET, ScratchPad
import numpy as np
import pickle
import tensorflow as tf

LOG_PATH = "tasks/multiplication/log/"
CKPT_PATH = "tasks/multiplication/log/model.ckpt"
TEST_PATH = "tasks/multiplication/data/test.pik"


WRITEMUL, WRITEADD, PTRMUL, PTRADD = 5, 11, 6, 12



def evaluate_multiplication():
    """
    Load NPI Model from Checkpoint, and initialize REPL, for interactive multiplication.
    """
    with tf.Session() as sess:
        # Load Data
        with open(TEST_PATH, 'rb') as f:
            data = pickle.load(f)

        # Initialize Multiplication Core
        core = MultiplicationCore()

        # Initialize NPI Model
        npi = NPI(core, CONFIG, LOG_PATH)

        # Restore from Checkpoint
        saver = tf.train.Saver()
        saver.restore(sess, CKPT_PATH)

        # Run REPL
        repl(sess, npi, data)


def repl(session, npi, data):
    while True:
        inpt = input('Enter Two Numbers, or Hit Enter for Random Pair: ')

        if inpt == "":
            x, y, _ = data[np.random.randint(len(data))]

        else:
            x, y = map(int, inpt.split())

        # Reset NPI States
        print ("")
        npi.reset_state()

        # Setup Environment
        scratch = ScratchPad(x, y)
        prog_name, prog_id, arg, term = 'MULTIPLY', 0, [], False

        cont = 'c'
        while cont == 'c' or cont == 'C':
            # # Print Step Output
            # if len(arg) != 0:
            #     a0, a1, a2 = str(arg[0]), str(arg[1]), str(arg[2])
            #     a_str = "[%s, %s, %s]" % (str(a0), str(a1), str(a2))
            # else:
            #     a_str = "[]"

            a_str = str(arg)

            print ('Step: %s, Arguments: %s, Terminate: %s' % (prog_name, a_str, str(term)))


            # Update Environment if MOVE or WRITE
            if prog_id in [WRITEMUL, WRITEADD, PTRMUL, PTRADD]:
                scratch.execute(prog_id, arg)

            # Print Environment
            scratch.pretty_print()

            # Get Environment, Argument Vectors
            env_in, arg_in, prog_in = [scratch.get_env()], [get_args(arg, arg_in=True)], [[prog_id]]
            t, n_p, n_args = session.run([npi.terminate, npi.program_distribution, npi.arguments],
                                         feed_dict={npi.env_in: env_in, npi.arg_in: arg_in,
                                                    npi.prg_in: prog_in})

            if np.argmax(t) == 1:
                print ('Step: %s, Arguments: %s, Terminate: %s' % (prog_name, a_str, str(True)))

                # Update Environment if MOVE or WRITE
                if prog_id in [WRITEMUL, WRITEADD, PTRMUL, PTRADD]:
                    scratch.execute(prog_id, arg)

                # Print Environment
                scratch.pretty_print()

                output = ''
                for i in range(scratch.cols):
                    output += str(scratch[-1][i])
                output = int(output)


                print ("Model Output: %s + %s = %s" % (str(x), str(y), str(output)))
                print ("Correct Out : %s + %s = %s" % (str(x), str(y), str(x + y)))
                print ("Correct!" if output == (x + y) else "Incorrect!")

            else:
                prog_id = np.argmax(n_p)
                prog_name = PROGRAM_SET[prog_id][0]
                if prog_id in [WRITEMUL, WRITEADD, PTRMUL, PTRADD]:
                    arg = [np.argmax(n_args[0]), np.argmax(n_args[1]), np.argmax(n_args[2])]
                else:
                    arg = []
                term = False

            cont = input('Continue? ')