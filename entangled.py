import cmatrix as cmat
import qsim
import qgates

# demonstration of basic entangled state simulation (bell state)

# initial state |00>
state = qsim.create_state([0, 0])

# create state 1/sqrt(2)*(|00> + |10>)
state = qsim.apply_gate(state, qgates.H, 0)

# apply cnot to combined state, producing 1/sqrt(2)*(|00> + |11>)
state = qsim.apply_gate(state, qgates.cnot, 0)

# measure state
print("measurement: ", qsim.measure_all_standard(state))

# subsequent measurements must be the same since measuring changes the state
print("measurement: ", qsim.measure_all_standard(state))
print("measurement: ", qsim.measure_all_standard(state))
print("measurement: ", qsim.measure_all_standard(state))

# measurement confirms entangled state!