from qiskit_nature.units import DistanceUnit
from qiskit_nature.second_q.drivers import PySCFDriver
from qiskit_nature.second_q.mappers import JordanWignerMapper, QubitMapper
from qiskit_nature.second_q.operators import SparseLabelOp
from qiskit_nature.second_q.problems import ElectronicStructureProblem

def get_molecular_hamiltonian(molecule_str: str, basis: str = "sto3g"):
    """
    Generates a qubit Hamiltonian for a given molecule string.
    Example molecule_str: "H 0 0 0; H 0 0 0.735"
    """
    driver = PySCFDriver(
        atom=molecule_str,
        basis=basis,
        charge=0,
        spin=0,
        unit=DistanceUnit.ANGSTROM,
    )
    problem = driver.run()
    
    # Get the electronic Hamiltonian in second quantization
    hamiltonian = problem.hamiltonian.second_q_op()
    
    # Map to qubit operator
    mapper = JordanWignerMapper()
    qubit_op = mapper.map(hamiltonian)
    
    return qubit_op, problem

def get_h2_hamiltonian(distance: float = 0.735):
    """Returns the H2 Hamiltonian at a given distance."""
    molecule_str = f"H 0 0 0; H 0 0 {distance}"
    return get_molecular_hamiltonian(molecule_str)

def get_h2_plus_hamiltonian(distance: float = 1.05):
    """Returns the H2+ Hamiltonian at a given distance."""
    # Note: For H2+, charge is 1 and spin is 1/2 (multiplicity 2)
    driver = PySCFDriver(
        atom=f"H 0 0 0; H 0 0 {distance}",
        basis="sto3g",
        charge=1,
        spin=1, # spin = 2*S
        unit=DistanceUnit.ANGSTROM,
    )
    problem = driver.run()
    hamiltonian = problem.hamiltonian.second_q_op()
    mapper = JordanWignerMapper()
    qubit_op = mapper.map(hamiltonian)
    return qubit_op, problem
