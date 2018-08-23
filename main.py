"""
main.py
"""
import tensorflow as tf
import warnings
warnings.filterwarnings("ignore", message="numpy.dtype size changed")
warnings.filterwarnings("ignore", message="numpy.ufunc size changed")


from tasks.addition.env.generate_data import generate_addition
from tasks.addition.eval import evaluate_addition
from tasks.addition.train import train_addition

from tasks.bubblesort.env.generate_data import generate_bubblesort
from tasks.bubblesort.eval import evaluate_bubblesort
from tasks.bubblesort.train import train_bubblesort

from tasks.multiplication.env.generate_data import generate_multiplication
from tasks.multiplication.eval import evaluate_multiplication
from tasks.multiplication.train import train_multiplication




FLAGS = tf.app.flags.FLAGS
tf.app.flags.DEFINE_string("task", "bubblesort", "Which NPI Task to run.")
tf.app.flags.DEFINE_boolean("generate", False, "Boolean whether to generate training/test data.")
tf.app.flags.DEFINE_integer("num_training", 100, "Number of training examples to generate.")
tf.app.flags.DEFINE_integer("num_test", 10, "Number of test examples to generate.")

tf.app.flags.DEFINE_boolean("do_train", False, "Boolean whether to continue training model.")
tf.app.flags.DEFINE_boolean("do_eval", True, "Boolean whether to perform model evaluation.")
tf.app.flags.DEFINE_integer("num_epochs", 1, "Number of training epochs to perform.")




def main(_):

    """
    ADDITION
    """

    if FLAGS.task == "addition":
        # Generate Data (if necessary)
        if FLAGS.generate:
            print("generating addition data ...")
            generate_addition('train', FLAGS.num_training)
            generate_addition('test', FLAGS.num_test)

        # Train Model (if necessary)
        if FLAGS.do_train:
            print("training model ...")
            train_addition(FLAGS.num_epochs)

        # Evaluate Model
        if FLAGS.do_eval:
            print("evaluating model ...")
            evaluate_addition()



    """
    BUBBLESORT
    """

    if FLAGS.task == "bubblesort":
        # Generate Data (if necessary)
        if FLAGS.generate:
            print("generating bubblesort data ...")
            generate_bubblesort('train', FLAGS.num_training)
            generate_bubblesort('test', FLAGS.num_test)

        # Train Model (if necessary)
        if FLAGS.do_train:
            print("training model ...")
            train_bubblesort(FLAGS.num_epochs)

        # Evaluate Model
        if FLAGS.do_eval:
            print("evaluating model ...")
            evaluate_bubblesort()


    """
    MULTIPLICATION
    """

    if FLAGS.task == "multiplication":
        # Generate Data (if necessary)
        if FLAGS.generate:
            print("generating multiplication data ...")
            generate_multiplication('train', FLAGS.num_training)
            generate_multiplication('test', FLAGS.num_test)

        # Train Model (if necessary)
        if FLAGS.do_train:
            print("training model ...")
            train_multiplication(FLAGS.num_epochs)

        # Evaluate Model
        if FLAGS.do_eval:
            print("evaluating model ...")
            evaluate_multiplication()


if __name__ == "__main__":
    print("app preparing to run ...")
    tf.app.run()






