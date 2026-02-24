import sys
import os
import numpy as np
import matplotlib.pyplot as plt
from quantumchem.hamiltonian import get_h2_hamiltonian
from quantumchem.vqdimlpement import run_vqd_qiskit, run_vqd_pennylane
from quantumchem.visual import plot_potential_energy_surface

dist = 0.735
try:
    print(f"Generating Hamiltonian for H2 at {dist} A...")
    qubit_op, problem = get_h2_hamiltonian(dist)
    print(f"Qubit operator for H2 at {dist} A:")
    print(qubit_op)

    # Run VQD with Qiskit for 2 states
    print("Running VQD with Qiskit for 2 states...")
    energies_qiskit, _ = run_vqd_qiskit(qubit_op, num_states=2)
    print(f"Qiskit energies: {energies_qiskit}")

    # Run VQD with PennyLane for 2 states
    print("Running VQD with PennyLane for 2 states...")
    energies_pennylane, _ = run_vqd_pennylane(qubit_op, num_states=2)
    print(f"PennyLane energies: {energies_pennylane}")

except Exception as e:
    import traceback
    traceback.print_exc()
