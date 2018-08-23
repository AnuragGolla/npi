"""
trace.py

Core class definition for a trace object => given an array of integers to sort, builds the execution
trace, calling the specified subprograms.
"""
from tasks.bubblesort.env.config import ScratchPad, PROGRAM_ID as P
BUBBLESORT, BUBBLE, RESET, BSTEP, COMPSWAP, LSHIFT, RSHIFT, SWAP, PTR = \
    "BUBBLESORT", "BUBBLE", "RESET", "BSTEP", "COMPSWAP", "LSHIFT", "RSHIFT", "SWAP", "PTR"

IN_ARRAY, PTR_1, PTR_2, PTR_COUNTER = range(4)
LEFT, RIGHT = 0, 1



class Trace:
    def __init__(self, in_array, debug=False):
        """
        Instantiates a trace object, and builds the exact execution pipeline for adding the given
        parameters.
        """
        self.in_array, self.debug = in_array, debug
        self.trace, self.scratch = [], ScratchPad(in_array)
        self.traceDone = False

        # Build Execution Trace
        self.build()

        # Check answer
        true_ans = sorted(self.in_array, key=int)
        trace_ans = self.scratch[0]

        # print("TRUE: ", in_array, "  ==>  ", true_ans)
        # print("DECISION: ", in_array, true_ans, trace_ans)

        for i in range(len(true_ans)):
            assert(true_ans[i] == trace_ans[i])

    def build(self):
        """
        Builds execution trace, adding individual steps to the instance variable trace. Each
        step is represented by a triple (program_id : Integer, args : List, terminate: Boolean). If
        a subroutine doesn't take arguments, the empty list is returned.
        """
        # Seed with the starting subroutine call
        self.trace.append(((BUBBLESORT, P[BUBBLESORT]), [], False))

        # Execute Trace

        while not self.traceDone:
            self.bubble()
            self.reset()


    def bubble(self):
        # print("BUBBLE SUBROUTINE")
        # Call Bubble Subroutine
        self.trace.append(( (BUBBLE, P[BUBBLE]), [], False ))

        self.trace.append((  (PTR, P[PTR]),  [PTR_2, RIGHT],  False))
        self.scratch.ptr([PTR_2, RIGHT], debug=self.debug)

        while self.scratch.ptr_1[1] < self.scratch.cols - 1:
            self.bstep()


    def bstep(self):
        # print("BTEP SUBROUTINE")

        self.trace.append(((BSTEP, P[BSTEP]), [], False))

        self.compswap()
        self.rshift()


    def compswap(self):
        # print("COMPSWAP SUBROUTINE")

        self.trace.append((  (COMPSWAP, P[COMPSWAP]), [], False))

        if self.scratch.swap([PTR_1, PTR_2], debug=self.debug):
            self.trace.append((  (SWAP, P[SWAP]), [PTR_1, PTR_2], False))

        else:
            pass ##CHECK

    def rshift(self):
        # print("RSHIFT SUBROUTINE")

        self.trace.append((  (RSHIFT, P[RSHIFT]), [], False))

        self.trace.append((  (PTR, P[PTR]), [PTR_1, RIGHT], False))
        self.scratch.ptr([PTR_1, RIGHT], debug=self.debug)

        self.trace.append((  (PTR, P[PTR]), [PTR_2, RIGHT], False))
        self.scratch.ptr([PTR_2, RIGHT], debug=self.debug)


    def reset(self):
        # print("RESET SUBROUTINE")

        self.trace.append((  (RESET, P[RESET]), [], False))

        while self.scratch.ptr_2[1] > 0:
            self.lshift()

        if self.scratch.done():
            self.trace.append(((PTR, P[PTR]), [PTR_COUNTER, RIGHT], True))
            self.scratch.ptr([PTR_COUNTER, RIGHT], debug=self.debug)
            self.traceDone = True

        else:
            self.trace.append(((PTR, P[PTR]), [PTR_COUNTER, RIGHT], False))
            self.scratch.ptr([PTR_COUNTER, RIGHT], debug=self.debug)



    def lshift(self):
        # print("LSHIFT SUBROUTINE")

        self.trace.append(((LSHIFT, P[LSHIFT]), [], False))

        self.trace.append(((PTR, P[PTR]), [PTR_1, LEFT], False))
        self.scratch.ptr([PTR_1, LEFT], debug=self.debug)

        self.trace.append(((PTR, P[PTR]), [PTR_2, LEFT], False))
        self.scratch.ptr([PTR_2, LEFT], debug=self.debug)



