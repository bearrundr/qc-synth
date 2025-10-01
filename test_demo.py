#!/usr/bin/env python3
"""
데모 로드 기능 테스트 스크립트
"""

from quantum_synth import QuantumCircuitSynthesizer, SynthConfig

def test_demo_load():
    """데모 로드 기능 테스트"""
    print("=== 데모 로드 테스트 ===")
    
    # 신디사이저 초기화
    config = SynthConfig()
    synth = QuantumCircuitSynthesizer(config)
    
    # 각 데모 테스트
    demos = ['superposition', 'mixed_states', 'entanglement']
    
    for demo_name in demos:
        print(f"\n테스트 중: {demo_name}")
        result = synth.load_demo_circuit(demo_name)
        
        if result['success']:
            print(f"✅ {demo_name} 로드 성공!")
            
            # 회로 정보 확인
            viz_data = synth.get_circuit_visualization_data()
            print(f"  - 게이트 수: {viz_data['circuit_info']['gate_count']}")
            print(f"  - 회로 깊이: {viz_data['circuit_info']['circuit_depth']}")
            print(f"  - 큐빗 확률: {viz_data['qubit_probabilities']}")
            
        else:
            print(f"❌ {demo_name} 로드 실패: {result.get('error', 'Unknown error')}")
        
        # 회로 초기화
        synth.reset_circuit()

if __name__ == "__main__":
    test_demo_load()
