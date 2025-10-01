"""
Quantum Circuit Engine using IBM Qiskit
양자 회로 엔진 - H, X, CNOT 게이트 지원
"""

import os
# Qiskit 1.0 import 오류 억제
os.environ['QISKIT_SUPPRESS_1_0_IMPORT_ERROR'] = '1'

import numpy as np
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister, transpile
from qiskit.quantum_info import Statevector
from typing import Dict, List, Tuple, Optional
import logging

# AerSimulator import with fallback
try:
    from qiskit_aer import AerSimulator
except ImportError:
    try:
        from qiskit.providers.aer import AerSimulator
    except ImportError:
        from qiskit.providers.basic_provider import BasicProvider
        AerSimulator = BasicProvider().get_backend('basic_simulator')

# 로깅 설정
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class QuantumSynthEngine:
    """양자 회로 신디사이저 엔진"""
    
    def __init__(self, num_qubits: int = 3):
        """
        양자 엔진 초기화
        
        Args:
            num_qubits: 사용할 큐빗 수 (기본값: 3)
        """
        self.num_qubits = num_qubits
        self.simulator = AerSimulator()
        self.circuit = None
        self.reset_circuit()
        
        # 큐빗별 주파수 매핑 (Hz)
        self.qubit_frequencies = {
            0: 220.0,  # Bass Line (A3)
            1: 330.0,  # Melody (E4)  
            2: 440.0,  # Harmony (A4)
        }
        
        logger.info(f"QuantumSynthEngine initialized with {num_qubits} qubits")
    
    def reset_circuit(self):
        """양자 회로 초기화"""
        self.qreg = QuantumRegister(self.num_qubits, 'q')
        self.creg = ClassicalRegister(self.num_qubits, 'c')
        self.circuit = QuantumCircuit(self.qreg, self.creg)
        logger.info("Quantum circuit reset")
    
    def apply_hadamard(self, qubit: int):
        """
        하다마드 게이트 적용 (중첩 상태 생성)
        
        Args:
            qubit: 게이트를 적용할 큐빗 인덱스
        """
        if 0 <= qubit < self.num_qubits:
            self.circuit.h(qubit)
            logger.info(f"Hadamard gate applied to qubit {qubit}")
        else:
            raise ValueError(f"Invalid qubit index: {qubit}")
    
    def apply_pauli_x(self, qubit: int):
        """
        Pauli-X 게이트 적용 (비트 플립)
        
        Args:
            qubit: 게이트를 적용할 큐빗 인덱스
        """
        if 0 <= qubit < self.num_qubits:
            self.circuit.x(qubit)
            logger.info(f"Pauli-X gate applied to qubit {qubit}")
        else:
            raise ValueError(f"Invalid qubit index: {qubit}")
    
    def apply_cnot(self, control: int, target: int):
        """
        CNOT 게이트 적용 (얽힘 상태 생성)
        
        Args:
            control: 제어 큐빗 인덱스
            target: 타겟 큐빗 인덱스
        """
        if (0 <= control < self.num_qubits and 
            0 <= target < self.num_qubits and 
            control != target):
            self.circuit.cx(control, target)
            logger.info(f"CNOT gate applied: control={control}, target={target}")
        else:
            raise ValueError(f"Invalid CNOT parameters: control={control}, target={target}")
    
    def get_statevector(self) -> np.ndarray:
        """
        현재 양자 상태벡터 반환
        
        Returns:
            복소수 배열로 표현된 상태벡터
        """
        try:
            statevector = Statevector.from_instruction(self.circuit)
            return statevector.data
        except Exception as e:
            logger.error(f"Error getting statevector: {e}")
            return np.array([1.0] + [0.0] * (2**self.num_qubits - 1), dtype=complex)
    
    def measure_circuit(self, shots: int = 1024) -> Dict[str, int]:
        """
        양자 회로 측정 실행
        
        Args:
            shots: 측정 횟수
            
        Returns:
            측정 결과 딕셔너리 {'000': count, '001': count, ...}
        """
        # 측정 게이트 추가
        temp_circuit = self.circuit.copy()
        temp_circuit.measure_all()
        
        try:
            # 회로 컴파일 및 실행
            compiled_circuit = transpile(temp_circuit, self.simulator)
            job = self.simulator.run(compiled_circuit, shots=shots)
            result = job.result()
            counts = result.get_counts()
            
            logger.info(f"Circuit measured with {shots} shots")
            return counts
            
        except Exception as e:
            logger.error(f"Error measuring circuit: {e}")
            # 기본값 반환 (모든 큐빗이 0 상태)
            return {'0' * self.num_qubits: shots}
    
    def get_measurement_probabilities(self, shots: int = 1024) -> Dict[str, float]:
        """
        측정 확률 계산
        
        Args:
            shots: 측정 횟수
            
        Returns:
            각 상태의 확률 딕셔너리
        """
        counts = self.measure_circuit(shots)
        total_shots = sum(counts.values())
        
        probabilities = {}
        for state, count in counts.items():
            probabilities[state] = count / total_shots
            
        return probabilities
    
    def get_qubit_probabilities(self, shots: int = 1024) -> Dict[int, float]:
        """
        각 큐빗의 |1⟩ 상태 확률 계산
        
        Args:
            shots: 측정 횟수
            
        Returns:
            큐빗별 |1⟩ 확률 딕셔너리
        """
        counts = self.measure_circuit(shots)
        total_shots = sum(counts.values())
        
        qubit_probs = {i: 0.0 for i in range(self.num_qubits)}
        
        for state, count in counts.items():
            # 공백으로 분리된 경우 첫 번째 부분만 사용 (클래식 비트 부분)
            if ' ' in state:
                state = state.split()[0]
            
            # 상태 문자열을 큐빗 수에 맞게 패딩
            padded_state = state.zfill(self.num_qubits)
            
            # 상태 문자열을 역순으로 읽어야 함 (Qiskit 규칙)
            for i, bit in enumerate(reversed(padded_state)):
                if i < self.num_qubits and bit == '1':
                    qubit_probs[i] += count / total_shots
        
        return qubit_probs
    
    def get_circuit_info(self) -> Dict:
        """
        현재 회로 정보 반환
        
        Returns:
            회로 정보 딕셔너리
        """
        return {
            'num_qubits': self.num_qubits,
            'circuit_depth': self.circuit.depth(),
            'gate_count': len(self.circuit.data),
            'qubit_frequencies': self.qubit_frequencies,
            'circuit_diagram': str(self.circuit)
        }
    
    def get_gate_sequence(self) -> List[Dict]:
        """
        적용된 게이트 시퀀스 반환
        
        Returns:
            게이트 정보 리스트
        """
        gates = []
        for instruction in self.circuit.data:
            gate_info = {
                'name': instruction.operation.name,
                'qubits': [self.circuit.find_bit(q).index for q in instruction.qubits],
                'params': instruction.operation.params
            }
            gates.append(gate_info)
        
        return gates


def create_demo_circuits() -> Dict[str, QuantumSynthEngine]:
    """
    데모용 양자 회로들 생성
    
    Returns:
        데모 회로 딕셔너리
    """
    circuits = {}
    
    # 1. 단순 중첩 상태
    engine1 = QuantumSynthEngine(3)
    engine1.apply_hadamard(0)
    engine1.apply_hadamard(1)
    circuits['superposition'] = engine1
    
    # 2. 비트 플립 + 중첩
    engine2 = QuantumSynthEngine(3)
    engine2.apply_pauli_x(0)
    engine2.apply_hadamard(1)
    engine2.apply_hadamard(2)
    circuits['mixed_states'] = engine2
    
    # 3. 얽힘 상태
    engine3 = QuantumSynthEngine(3)
    engine3.apply_hadamard(0)
    engine3.apply_cnot(0, 1)
    engine3.apply_cnot(1, 2)
    circuits['entanglement'] = engine3
    
    return circuits


if __name__ == "__main__":
    # 테스트 코드
    print("=== Quantum Circuit Synthesizer Engine Test ===")
    
    engine = QuantumSynthEngine(3)
    
    # 게이트 적용
    engine.apply_hadamard(0)
    engine.apply_pauli_x(1)
    engine.apply_cnot(0, 2)
    
    # 회로 정보 출력
    info = engine.get_circuit_info()
    print(f"Circuit Info: {info}")
    
    # 측정 확률 계산
    probs = engine.get_qubit_probabilities()
    print(f"Qubit Probabilities: {probs}")
    
    # 상태벡터 출력
    statevector = engine.get_statevector()
    print(f"Statevector shape: {statevector.shape}")
    print(f"Statevector (first 4 elements): {statevector[:4]}")
