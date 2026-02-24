import sys
import os

try:
    import numpy as np
    print(f"NumPy version: {np.__version__}")
except ImportError as e:
    print(f"NumPy import failed: {e}")

try:
    import qiskit
    print(f"Qiskit version: {qiskit.__version__}")
except ImportError as e:
    print(f"Qiskit import failed: {e}")
except AttributeError:
    print("Qiskit imported but version not found")

try:
    import qiskit_algorithms
    print(f"Qiskit Algorithms version: {qiskit_algorithms.__version__}")
except ImportError as e:
    print(f"Qiskit Algorithms import failed: {e}")

try:
    import qiskit_nature
    print(f"Qiskit Nature version: {qiskit_nature.__version__}")
except ImportError as e:
    print(f"Qiskit Nature import failed: {e}")

try:
    import pennylane as qml
    print(f"PennyLane version: {qml.__version__}")
except ImportError as e:
    print(f"PennyLane import failed: {e}")

try:
    import pyscf
    print(f"PySCF version: {pyscf.__version__}")
except ImportError as e:
    print(f"PySCF import failed: {e}")

try:
    from qiskit.primitives import StatevectorEstimator
    print("Successfully imported StatevectorEstimator")
except ImportError as e:
    print(f"Failed to import StatevectorEstimator: {e}")

try:
    from qiskit_algorithms import VQD
    print("Successfully imported VQD")
except ImportError as e:
    print(f"Failed to import VQD: {e}")
