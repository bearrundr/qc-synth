#!/usr/bin/env python3
"""
측정 결과 디버깅 스크립트
"""

from quantum_engine import QuantumSynthEngine, create_demo_circuits

def debug_measurement():
    """측정 결과 디버깅"""
    print("=== 측정 결과 디버깅 ===")
    
    # 간단한 테스트 회로
    engine = QuantumSynthEngine(3)
    
    print("\n1. 초기 상태 (모든 큐빗 |0⟩)")
    counts = engine.measure_circuit(1024)
    print(f"측정 결과: {counts}")
    probs = engine.get_qubit_probabilities(1024)
    print(f"큐빗 확률: {probs}")
    
    print("\n2. H 게이트 적용 후 (큐빗 0)")
    engine.apply_hadamard(0)
    counts = engine.measure_circuit(1024)
    print(f"측정 결과: {counts}")
    probs = engine.get_qubit_probabilities(1024)
    print(f"큐빗 확률: {probs}")
    
    print("\n3. X 게이트 적용 후 (큐빗 1)")
    engine.apply_pauli_x(1)
    counts = engine.measure_circuit(1024)
    print(f"측정 결과: {counts}")
    probs = engine.get_qubit_probabilities(1024)
    print(f"큐빗 확률: {probs}")
    
    print("\n4. 데모 회로 테스트")
    demos = create_demo_circuits()
    
    for name, demo_engine in demos.items():
        print(f"\n--- {name} ---")
        counts = demo_engine.measure_circuit(1024)
        print(f"측정 결과: {counts}")
        probs = demo_engine.get_qubit_probabilities(1024)
        print(f"큐빗 확률: {probs}")
        print(f"회로: {demo_engine.circuit}")

if __name__ == "__main__":
    debug_measurement()
