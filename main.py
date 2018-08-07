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




# FLAGS = tf.app.flags.FLAGS
# tf.app.flags.DEFINE_string("task", "addition", "Which NPI Task to run - [addition].")
# tf.app.flags.DEFINE_boolean("generate", True, "Boolean whether to generate training/test data.")
# tf.app.flags.DEFINE_integer("num_training", 1000, "Number of training examples to generate.")
# tf.app.flags.DEFINE_integer("num_test", 100, "Number of test examples to generate.")
#
# tf.app.flags.DEFINE_boolean("do_train", False, "Boolean whether to continue training model.")
# tf.app.flags.DEFINE_boolean("do_eval", True, "Boolean whether to perform model evaluation.")
# tf.app.flags.DEFINE_integer("num_epochs", 5, "Number of training epochs to perform.")
#
#
# def main(_):
#     # print("START ####################")
#     if FLAGS.task == "addition":
#         # Generate Data (if necessary)
#         # print("DATA NOT GENERATED ####################")
#
#         if FLAGS.generate:
#             generate_addition('train', FLAGS.num_training)
#             generate_addition('test', FLAGS.num_test)
#
#             print("DATA GENERATED ####################")
#
#         # Train Model (if necessary)
#         if FLAGS.do_train:
#             train_addition(FLAGS.num_epochs)
#
#         # Evaluate Model
#         if FLAGS.do_eval:
#             evaluate_addition()
#
#
# if __name__ == "__main__":
#     # print("REAL START ####################")
#     tf.app.run()




FLAGS = tf.app.flags.FLAGS
tf.app.flags.DEFINE_string("task", "bubblesort", "Which NPI Task to run - [bubblesort].")
tf.app.flags.DEFINE_boolean("generate",True, "Boolean whether to generate training/test data.")
tf.app.flags.DEFINE_integer("num_training", 5, "Number of training examples to generate.") ###100
tf.app.flags.DEFINE_integer("num_test", 1, "Number of test examples to generate.") ##100

tf.app.flags.DEFINE_boolean("do_train", True, "Boolean whether to continue training model.")
tf.app.flags.DEFINE_boolean("do_eval", False, "Boolean whether to perform model evaluation.")
tf.app.flags.DEFINE_integer("num_epochs", 2, "Number of training epochs to perform.")


def main(_):
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


if __name__ == "__main__":
    print("app preparing to run ...")
    tf.app.run()