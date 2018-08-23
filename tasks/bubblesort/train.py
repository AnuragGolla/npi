"""
train.py

Core training script for the bubblesort task-specific NPI. Instantiates a model, then trains using
the precomputed data.
"""
from model.npi import NPI
from tasks.bubblesort.bubblesort import BubblesortCore
from tasks.bubblesort.env.config import CONFIG, get_args, ScratchPad
import pickle
import tensorflow as tf




MOVE_PTR_PID, SWAP_ELEM_PID = 8, 7

WRITE_OUT, WRITE_CARRY = 0, 1

IN_ARRAY, PTR_1, PTR_2, PTR_COUNTER = range(4)

LEFT, RIGHT = -1, 1

DATA_PATH = "tasks/bubblesort/data/train.pik"
LOG_PATH = "tasks/bubblesort/log/"


def train_bubblesort(epochs, verbose=0):
    """
    Instantiates an Bubblesort Core, NPI, then loads and fits model to data.

    :param epochs: Number of epochs to train for.
    """
    # Load Data
    with open(DATA_PATH, 'rb') as f:
        data = pickle.load(f)

    # Initialize Addition Core
    print ('initializing bubblesort core ...')
    core = BubblesortCore()

    # Initialize NPI Model
    print ('initializing npi model ...')
    npi = NPI(core, CONFIG, LOG_PATH, verbose=verbose)

    # Initialize TF Saver
    saver = tf.train.Saver()

    # Initialize TF Session
    sess = tf.Session()
    sess.run(tf.global_variables_initializer())

    # Start Training
    for ep in range(1, epochs + 1):
        for i in range(len(data)):
            print("DATA ENTRY #", i+1, "----------------------------------------------------------------------")
            # Reset NPI States
            npi.reset_state()

            # Setup Environment
            in_array, steps = data[i]
            scratch = ScratchPad(in_array)
            x, y = steps[:-1], steps[1:]

            # Run through steps, and fit!
            step_def_loss, step_arg_loss, term_acc, prog_acc, = 0.0, 0.0, 0.0, 0.0
            arg0_acc, arg1_acc, arg2_acc, num_args = 0.0, 0.0, 0.0, 0

            for j in range(len(x)):
                (prog_name, prog_in_id), arg, term = x[j]
                (_, prog_out_id), arg_out, term_out = y[j]

                print("IN:  ", x[j])
                print("OUT: ", y[j])
                print("----------------------------------------")

                # Update Environment if MOVE or WRITE
                if prog_in_id == MOVE_PTR_PID or prog_in_id == SWAP_ELEM_PID:
                    scratch.execute(prog_in_id, arg)

                # Get Environment, Argument Vectors
                env_in = [scratch.get_env()]
                arg_in, arg_out = [get_args(arg, arg_in=True)], get_args(arg_out, arg_in=False)
                prog_in, prog_out = [[prog_in_id]], [prog_out_id]
                term_out = [1] if term_out else [0]

                # Fit!
                if prog_out_id == MOVE_PTR_PID or prog_out_id == SWAP_ELEM_PID:
                    loss, t_acc, p_acc, a_acc, _ = sess.run(
                        [npi.arg_loss, npi.t_metric, npi.p_metric, npi.a_metrics, npi.arg_train_op],
                        feed_dict={npi.env_in: env_in, npi.arg_in: arg_in, npi.prg_in: prog_in,
                                   npi.y_prog: prog_out, npi.y_term: term_out,
                                   npi.y_args[0]: [arg_out[0]], npi.y_args[1]: [arg_out[1]],
                                   npi.y_args[2]: [arg_out[2]]})
                    step_arg_loss += loss
                    term_acc += t_acc
                    prog_acc += p_acc
                    arg0_acc += a_acc[0]
                    arg1_acc += a_acc[1]
                    arg2_acc += a_acc[2]
                    num_args += 1
                else:
                    loss, t_acc, p_acc, _ = sess.run(
                        [npi.default_loss, npi.t_metric, npi.p_metric, npi.default_train_op],
                        feed_dict={npi.env_in: env_in, npi.arg_in: arg_in, npi.prg_in: prog_in,
                                   npi.y_prog: prog_out, npi.y_term: term_out})
                    step_def_loss += loss
                    term_acc += t_acc
                    prog_acc += p_acc

            print ("Epoch {0:02d} Step {1:03d} Default Step Loss {2:05f}, " \
                  "Argument Step Loss {3:05f}, Term: {4:03f}, Prog: {5:03f}, A0: {6:03f}, " \
                  "A1: {7:03f}, A2: {8:03}"\
                .format(ep, i, step_def_loss / len(x), step_arg_loss / len(x), term_acc / len(x),
                        prog_acc / len(x), arg0_acc / num_args, arg1_acc / num_args,
                        arg2_acc / num_args))

        # Save Model
        saver.save(sess, 'tasks/bubblesort/log/model.ckpt')