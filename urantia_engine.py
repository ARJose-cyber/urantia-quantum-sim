import numpy as np
from qiskit_nature.units import DistanceUnit
from qiskit_nature.second_q.drivers import PySCFDriver
from qiskit_nature.second_q.mappers import JordanWignerMapper
from qiskit_algorithms import VQE
from qiskit_algorithms.optimizers import SLSQP
from qiskit.primitives import StatevectorEstimator as Estimator
from qiskit.circuit.library import TwoLocal

def run_urantia_simulation(bond_distance, activity_factor):
    """
    bond_distance: Distance between H atoms (standard is ~0.735)
    activity_factor: Represents the 'slowing down' of ultimatons (0.0 to 1.0)
    """
    # 1. Define Molecule based on Urantia 'Solar System' spacing
    driver = PySCFDriver(
        atom=f"H 0 0 0; H 0 0 {bond_distance}",
        basis="sto3g",
        unit=DistanceUnit.ANGSTROM,
    )
    
    # 2. Setup the Quantum Problem
    problem = driver.run()
    hamiltonian, _ = problem.second_q_ops()
    mapper = JordanWignerMapper()
    qubit_op = mapper.map(hamiltonian)

    # 3. Adjust for 'Electronic Stage' Energy
    # We scale the Hamiltonian by the 'slowing down' factor described in Paper 42
    qubit_op = qubit_op * activity_factor

    # 4. Quantum Ansatz (The 'Complex Organized Unit')
    # Using 4 qubits to represent the 'Internal Structure' of the electron
    ansatz = TwoLocal(qubit_op.num_qubits, rotation_blocks="ry", entanglement_blocks="cz")

    # 5. Solve via VQE
    vqe = VQE(Estimator(), ansatz, SLSQP(maxiter=25))
    result = vqe.compute_minimum_eigenvalue(qubit_op)
    
    total_energy = result.optimal_value + (problem.nuclear_repulsion_energy * activity_factor)
    return total_energy
