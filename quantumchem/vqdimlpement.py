import numpy as np
from typing import List, Optional
from qiskit.circuit.library import TwoLocal
from qiskit.primitives import StatevectorEstimator, StatevectorSampler
from qiskit_algorithms import VQD, VQE
from qiskit_algorithms.optimizers import SLSQP
from qiskit_algorithms.state_fidelities import ComputeUncompute

import pennylane as qml
from pennylane import numpy as pnp

def run_vqd_qiskit(qubit_op, num_states=2):
    """
    Run VQD using Qiskit to find the ground and first excited states.
    """
    ansatz = TwoLocal(qubit_op.num_qubits, "ry", "cz", reps=2, entanglement="full")
    optimizer = SLSQP(maxiter=100)
    estimator = StatevectorEstimator()
    sampler = StatevectorSampler()
    fidelity = ComputeUncompute(sampler)
    
    vqd = VQD(estimator, fidelity, ansatz, optimizer, k=num_states)
    result = vqd.compute_eigenvalues(qubit_op)
    
    return result.eigenvalues.real, result.optimal_parameters

def run_vqd_pennylane(qubit_op_qiskit, num_states=2, num_qubits=None):
    """
    Run VQD using PennyLane. 
    Converts Qiskit qubit operator to PennyLane Hamiltonian.
    """
    if num_qubits is None:
        num_qubits = qubit_op_qiskit.num_qubits
    
    # Simple conversion helper (basic implementation)
    # In a real scenario, use qml.from_qiskit if available or manual mapping
    # For now, we'll assume the qubit_op is already in a form we can handle or use a placeholder
    # Let's use a more robust approach if possible
    
    # Re-build Hamiltonian in PennyLane or convert
    # For simplicity, let's assume we can map the Paulis
    coeffs = []
    obs = []
    
    # Qiskit SparsePauliOp to PennyLane
    for pauli, coeff in qubit_op_qiskit.label_iter():
        coeffs.append(coeff.real)
        ops = []
        for i, char in enumerate(pauli):
            if char == 'X':
                ops.append(qml.PauliX(num_qubits - 1 - i))
            elif char == 'Y':
                ops.append(qml.PauliY(num_qubits - 1 - i))
            elif char == 'Z':
                ops.append(qml.PauliZ(num_qubits - 1 - i))
        if ops:
            if len(ops) > 1:
                obs.append(qml.prod(*ops))
            else:
                obs.append(ops[0])
        else:
            obs.append(qml.Identity(0)) # Identity
            
    H = qml.Hamiltonian(coeffs, obs)
    dev = qml.device("default.qubit", wires=num_qubits)
    
    @qml.qnode(dev)
    def ansatz(params, wires):
        qml.StronglyEntanglingLayers(params, wires=wires)
        return qml.state()

    @qml.qnode(dev)
    def cost_fn(params, H):
        qml.StronglyEntanglingLayers(params, wires=dev.wires)
        return qml.expval(H)

    # VQD implementation in PennyLane
    energies = []
    all_params = []
    
    # Shape for StronglyEntanglingLayers: (layers, num_qubits, 3)
    shape = qml.StronglyEntanglingLayers.shape(n_layers=2, n_wires=num_qubits)
    
    for k in range(num_states):
        params = pnp.random.random(shape, requires_grad=True)
        opt = qml.GradientDescentOptimizer(stepsize=0.1)
        
        def total_cost(p):
            # Energy term
            energy = cost_fn(p, H)
            # Penalty term (overlap with previous states)
            penalty = 0
            for prev_p in all_params:
                # Compute overlap |<psi(p)|psi(prev_p)>|^2
                # In PennyLane, we can use qml.math.fidelity or similar if we have states
                # For simplicity, let's use the state vector overlap
                state_k = ansatz(p, wires=dev.wires)
                state_prev = ansatz(prev_p, wires=dev.wires)
                overlap = pnp.abs(pnp.dot(pnp.conj(state_k), state_prev))**2
                penalty += 10.0 * overlap # Penalty weight
            return energy + penalty

        for i in range(100):
            params = opt.step(total_cost, params)
            if i % 20 == 0:
                pass # logging could go here
                
        energies.append(cost_fn(params, H))
        all_params.append(params)
        
    return energies, all_params
