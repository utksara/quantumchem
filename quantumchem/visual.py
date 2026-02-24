import matplotlib.pyplot as plt
import numpy as np
from typing import List, Dict

def plot_potential_energy_surface(distances: List[float], energies: Dict[str, List[float]], save_path: str = None):
    """
    Plots the potential energy surface for ground and excited states.
    energies: Dict like {"Ground State": [e0, e1, ...], "1st Excited State": [e0, e1, ...]}
    """
    plt.figure(figsize=(10, 6))
    for label, energy_list in energies.items():
        plt.plot(distances, energy_list, marker='o', label=label)
    
    plt.title("Potential Energy Surface (VQD)")
    plt.xlabel("Bond distance (Å)")
    plt.ylabel("Energy (Hartree)")
    plt.grid(True)
    plt.legend()
    if save_path:
        plt.savefig(save_path)
        print(f"Plot saved to {save_path}")
    else:
        plt.show()

def plot_wavefunction_density(states: List[np.ndarray], labels: List[str], save_path: str = None):
    """Plots the probability density of different states."""
    num_states = len(states)
    plt.figure(figsize=(12, 4 * num_states))
    
    for i, (state, label) in enumerate(zip(states, labels)):
        plt.subplot(num_states, 1, i + 1)
        density = np.abs(state)**2
        plt.bar(range(len(density)), density, label=label)
        plt.title(f"Probability Density - {label}")
        plt.xlabel("Basis State Index")
        plt.ylabel("Probability")
        plt.ylim(0, 1)
        plt.legend()
    
    plt.tight_layout()
    if save_path:
        plt.savefig(save_path)
        print(f"Plot saved to {save_path}")
    else:
        plt.show()

def plot_vqd_convergence(history: List[float], label: str = "VQD Optimization", save_path: str = None):
    """Plots the optimization convergence curve."""
    plt.figure(figsize=(8, 5))
    plt.plot(history)
    plt.title(f"Convergence: {label}")
    plt.xlabel("Iteration")
    plt.ylabel("Cost Value")
    plt.grid(True)
    if save_path:
        plt.savefig(save_path)
        print(f"Plot saved to {save_path}")
    else:
        plt.show()
