import qsim
import qgates
import cmatrix as cmat

# program to test the ability to measure arbitrary qubits and affect entangled states appropriately

# construct state: |0000> + |0110> + |1000> + |1110>
state = qsim.create_state([0, 0, 0, 0])
state = qsim.apply_gate(state, qgates.H, 0)
state = qsim.apply_gate(state, qgates.H, 1)
state = qsim.apply_gate(state, qgates.cnot, 1)
print("In state  |0000> + |0110> + |1000> + |1110> ")
print("Chance of measuring |0000> (expect 1/4)", cmat.expected_value(qsim.get_projector_range(0, 0, 3, 4), state))
print("Chance of measuring |xxx0> (expect 1)", cmat.expected_value(qsim.get_projector_range(0, 3, 3, 4), state))
print("Chance of measuring |x11x> (expect 1/2)", cmat.expected_value(qsim.get_projector_range(3, 1, 2, 4), state))
print("Chance of measuring |x01x> (expect 0)", cmat.expected_value(qsim.get_projector_range(1, 1, 2, 4), state))
print("Chance of measuring |0110> (expect 1/4)", cmat.expected_value(qsim.get_projector_range(6, 0, 3, 4), state))

# measure the second qubit (changing state)
print("second qubit measured as:", qsim.measure_range_standard(state, 1, 1))

# report the new chances
print("Chance of measuring |0000>", cmat.expected_value(qsim.get_projector_range(0, 0, 3, 4), state))
print("Chance of measuring |xxx0>", cmat.expected_value(qsim.get_projector_range(0, 3, 3, 4), state))
print("Chance of measuring |x11x>", cmat.expected_value(qsim.get_projector_range(3, 1, 2, 4), state))
print("Chance of measuring |x01x>", cmat.expected_value(qsim.get_projector_range(1, 1, 2, 4), state))
print("Chance of measuring |0110>", cmat.expected_value(qsim.get_projector_range(6, 0, 3, 4), state))