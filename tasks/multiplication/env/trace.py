"""
trace.py

Core class definition for a trace object => given a pair of integers to multiply, builds the execution
trace, calling the specified subprograms.
"""
from tasks.multiplication.env.config import ScratchPad, PROGRAM_ID as P

MULTIPLY, MULSTAGE, MULTIPLY1, MULSHIFT, MULCARRY, MULWRITE, MULPTR, \
    ADD, ADD1, ADDWRITE, ADDSHIFT, ADDCARRY, ADDPTR = \
        "MULTIPLY", "MULSTAGE", "MULTIPLY1", "MULSHIFT", "MULCARRY", "MULWRITE", "MULPTR", \
        "ADD", "ADD1", "ADDWRITE", "ADDSHIFT", "ADDCARRY", "ADDPTR"

WRITE_OUT, WRITE_CARRY = 0, 1

PTR_IN1, PTR_IN2, PTR_C1, PTR_C2, PTR_C3, PTR_C4, PTR_C5, PTR_O1, \
    PTR_O2, PTR_O3, PTR_O4, PTR_O5, PTR_CF, PTR_OF = range(14)

LEFT, RIGHT = 0, 1


class Trace():
    def __init__(self, in1, in2, debug=False):
        """
        Instantiates a trace object, and builds the exact execution pipeline for adding the given
        parameters.
        """
        self.in1, self.in2, self.debug = in1, in2, debug
        self.trace, self.scratch = [], ScratchPad(in1, in2)

        # Build Execution Trace
        self.build()

        # Check answer
        true_ans = self.in1 * self.in2

        trace_ans = ''

        for i in range(self.scratch.cols):
            trace_ans += str(self.scratch[-1][i])

        trace_ans = int(trace_ans)

        assert(true_ans == trace_ans)   #########CHECK

    def build(self):
        """
        Builds execution trace, adding individual steps to the instance variable trace. Each
        step is represented by a triple (program_id : Integer, args : List, terminate: Boolean). If
        a subroutine doesn't take arguments, the empty list is returned.
        """
        # Seed with the starting subroutine call
        self.trace.append(((MULTIPLY, P[MULTIPLY]), [], False))

        # Execute Trace
        while not self.scratch.muldone():
            self.mulstage()
            self.mulstageshift()

        self.trace.append(((ADD, P[ADD]), [], False))


        for i in range(5):
            self.trace.append(((MULPTR, P[MULPTR]), [PTR_O1, None, RIGHT], False))
            self.trace.append(((MULPTR, P[MULPTR]), [PTR_O2, None, RIGHT], False))
            self.trace.append(((MULPTR, P[MULPTR]), [PTR_O3, None, RIGHT], False))
            self.trace.append(((MULPTR, P[MULPTR]), [PTR_O4, None, RIGHT], False))
            self.trace.append(((MULPTR, P[MULPTR]), [PTR_O5, None, RIGHT], False))


        self.scratch.initAdd()

        while self.scratch.ptr_of[1] != 9:
            self.add1()
            self.addshift()


    def getMulStage_Out(self):
        stage_Out = - self.scratch.ptr_in2[1]
        stages_Out = {
            1: PTR_O1,
            2: PTR_O2,
            3: PTR_O3,
            4: PTR_O4,
            5: PTR_O5,
            6: PTR_OF
        }
        return stages_Out[stage_Out]

    def getMulStage_Carry(self):
        stage_Carry = - self.scratch.ptr_in2[1]
        stages_Carry = {
            1: PTR_C1,
            2: PTR_C2,
            3: PTR_C3,
            4: PTR_C4,
            5: PTR_C5,
            6: PTR_CF
        }
        return stages_Carry[stage_Carry]


    def mulstage(self):

        self.trace.append(((MULSTAGE, P[MULSTAGE]), [], False))

        while not self.scratch.mulstagedone():
            self.multiply1()
            self.mulshift()


    def multiply1(self):
        # print("MULTIPLY1")
        # Call Multiply1 Subroutine

        self.trace.append(( (MULTIPLY1, P[MULTIPLY1]), [], False ))
        out, mul_carry = self.scratch.multiply1()

        # Write to Output
        PTR = self.getMulStage_Out()
        self.trace.append(( (MULWRITE, P[MULWRITE]), [PTR, WRITE_OUT, out], False ))
        self.scratch.mulwrite([PTR, WRITE_OUT, out], self.debug)

        # Carry Condition
        if mul_carry > 0:
            self.mulcarry(mul_carry)


    def mulcarry(self, mul_carry):
        # print("MULCARRY")

        self.trace.append(((MULCARRY, P[MULCARRY]), [], False))

        # Shift Carry Pointer Left
        PTR = self.getMulStage_Carry()
        self.scratch.mulptr([PTR, None, LEFT], self.debug)
        self.trace.append(((MULPTR, P[MULPTR]), [PTR, None, LEFT], False))


        # Perform Carry Logic on Scratchpad
        self.scratch.mulwrite([PTR, WRITE_CARRY, mul_carry], self.debug)
        # Write Carry Value
        self.trace.append(((MULWRITE, P[MULWRITE]), [PTR, WRITE_CARRY, mul_carry], False))

        # Shift Carry Pointer Right
        self.scratch.mulptr([PTR, None, RIGHT], self.debug)
        self.trace.append(((MULPTR, P[MULPTR]), [PTR, None, RIGHT], False))




    def mulshift(self):
        # print("MULSHIFT")

        self.scratch.mulshift()

        self.trace.append(((MULPTR, P[MULPTR]), [PTR_IN1, None, LEFT], False))
        self.trace.append(((MULPTR, P[MULPTR]), [PTR_C1, None, LEFT], False))
        self.trace.append(((MULPTR, P[MULPTR]), [PTR_C2, None, LEFT], False))
        self.trace.append(((MULPTR, P[MULPTR]), [PTR_C3, None, LEFT], False))
        self.trace.append(((MULPTR, P[MULPTR]), [PTR_C4, None, LEFT], False))
        self.trace.append(((MULPTR, P[MULPTR]), [PTR_C5, None, LEFT], False))
        self.trace.append(((MULPTR, P[MULPTR]), [PTR_O1, None, LEFT], False))
        self.trace.append(((MULPTR, P[MULPTR]), [PTR_O2, None, LEFT], False))
        self.trace.append(((MULPTR, P[MULPTR]), [PTR_O3, None, LEFT], False))
        self.trace.append(((MULPTR, P[MULPTR]), [PTR_O4, None, LEFT], False))
        self.trace.append(((MULPTR, P[MULPTR]), [PTR_O5, None, LEFT], False))

    def mulstageshift(self):
        # print("MULSTAGESHIFT")



        self.trace.append(((MULPTR, P[MULPTR]), [PTR_IN2, None, LEFT], False))

        for i in range(self.scratch.ptr_in2[1] + self.scratch.cols):
            self.trace.append(((MULPTR, P[MULPTR]), [PTR_IN1, None, RIGHT], False))
            self.trace.append(((MULPTR, P[MULPTR]), [PTR_C1, None, RIGHT], False))
            self.trace.append(((MULPTR, P[MULPTR]), [PTR_C2, None, RIGHT], False))
            self.trace.append(((MULPTR, P[MULPTR]), [PTR_C3, None, RIGHT], False))
            self.trace.append(((MULPTR, P[MULPTR]), [PTR_C4, None, RIGHT], False))
            self.trace.append(((MULPTR, P[MULPTR]), [PTR_C5, None, RIGHT], False))
            self.trace.append(((MULPTR, P[MULPTR]), [PTR_O1, None, RIGHT], False))
            self.trace.append(((MULPTR, P[MULPTR]), [PTR_O2, None, RIGHT], False))
            self.trace.append(((MULPTR, P[MULPTR]), [PTR_O3, None, RIGHT], False))
            self.trace.append(((MULPTR, P[MULPTR]), [PTR_O4, None, RIGHT], False))
            self.trace.append(((MULPTR, P[MULPTR]), [PTR_O5, None, RIGHT], False))

        for i in range(1):
            self.trace.append(((MULPTR, P[MULPTR]), [PTR_IN1, None, RIGHT], False))

        self.scratch.mulstageshift()


    def add1(self):
        # print("ADD1")
        # Call Add1 Subroutine

        self.trace.append(( (ADD1, P[ADD1]), [], False ))
        out, add_carry = self.scratch.add1()

        # Write to Output
        self.trace.append(( (ADDWRITE, P[ADDWRITE]), [PTR_OF, WRITE_OUT, out], False ))
        self.scratch.addwrite([PTR_OF, WRITE_OUT, out], self.debug)

        # Carry Condition
        if add_carry > 0:
            self.addcarry(add_carry)

    def addcarry(self, add_carry):
        # print("ADDCARRY")
        # Call Carry Subroutine

        self.trace.append(( (ADDCARRY, P[ADDCARRY]), [], False ))

        # Shift Carry Pointer Left
        self.trace.append(( (ADDPTR, P[ADDPTR]), [PTR_CF, None, LEFT], False ))

        # Write Carry Value
        self.trace.append(( (ADDWRITE, P[ADDWRITE]), [PTR_CF, WRITE_CARRY, add_carry], False ))

        # Shift Carry Pointer Right
        self.trace.append(( (ADDPTR, P[ADDPTR]), [PTR_CF, None, RIGHT], False ))

        # Perform Carry Logic on Scratchpad
        self.scratch.addwrite([PTR_CF, WRITE_CARRY, add_carry], self.debug)


    def addshift(self):
        # print("ADDSHIFT")
        # Perform ADDShift Logic on Scratchpad


        self.trace.append(((ADDPTR, P[ADDPTR]), [PTR_O1, None, LEFT], False))
        self.trace.append(((ADDPTR, P[ADDPTR]), [PTR_O2, None, LEFT], False))
        self.trace.append(((ADDPTR, P[ADDPTR]), [PTR_O3, None, LEFT], False))
        self.trace.append(((ADDPTR, P[ADDPTR]), [PTR_O4, None, LEFT], False))
        self.trace.append(((ADDPTR, P[ADDPTR]), [PTR_O5, None, LEFT], False))
        self.trace.append(((ADDPTR, P[ADDPTR]), [PTR_CF, None, LEFT], False))


        if self.scratch.add_shift():
            self.trace.append(((ADDPTR, P[ADDPTR]), [PTR_OF, None, LEFT], True))

        else:
            self.trace.append(((ADDPTR, P[ADDPTR]), [PTR_OF, None, LEFT], False))