import sys
import os
sys.path.append('..') # add the root directory to path

import numpy as np
import matplotlib.pyplot as plt
from quantumchem.hamiltonian import get_h2_hamiltonian
from quantumchem.vqdimlpement import run_vqd_qiskit, run_vqd_pennylane
from quantumchem.visual import plot_potential_energy_surface


dist = 0.735
qubit_op, problem = get_h2_hamiltonian(dist)
print(f"Qubit operator for H2 at {dist} A:")
print(qubit_op)

# Run VQD with Qiskit for 2 states
energies_qiskit, _ = run_vqd_qiskit(qubit_op, num_states=2)
print(f"Qiskit VQD Energies (Hartree): Ground={energies_qiskit[0]:.4f}, 1st Excited={energies_qiskit[1]:.4f}")

distances = np.linspace(0.2, 2.5, 10)
ground_energies = []
excited_energies = []

for dist in distances:
    print(f"Calculating for distance: {dist:.2f} A...")
    qubit_op, problem = get_h2_hamiltonian(dist)
    energies, _ = run_vqd_qiskit(qubit_op, num_states=2)
    ground_energies.append(energies[0])
    excited_energies.append(energies[1])

pes_data = {
    "Ground State": ground_energies,
    "1st Excited State": excited_energies
}

plot_potential_energy_surface(distances, pes_data, save_path="pes_vqd.png")

# dist = 0.735
# qubit_op, _ = get_h2_hamiltonian(dist)
# energies_pennylane, _ = run_vqd_pennylane(qubit_op, num_states=2)
# print(f"PennyLane VQD Energies (Hartree): Ground={energies_pennylane[0]:.4f}, 1st Excited={energies_pennylane[1]:.4f}")