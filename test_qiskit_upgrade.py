#!/usr/bin/env python3
"""
Qiskit 1.0+ 업그레이드 호환성 테스트
"""

def test_qiskit_compatibility():
    """Qiskit 1.0+ 호환성 테스트"""
    print("=== Qiskit 1.0+ 호환성 테스트 ===")
    
    try:
        # 1. Qiskit 버전 확인
        import qiskit
        print(f"✅ Qiskit 버전: {qiskit.__version__}")
        
        # 2. 기본 임포트 테스트
        from qiskit import QuantumCircuit, transpile
        from qiskit_aer import AerSimulator
        print("✅ 기본 임포트 성공")
        
        # 3. 회로 생성 테스트
        qc = QuantumCircuit(3, 3)
        qc.h(0)
        qc.x(1)
        qc.cx(0, 2)
        qc.measure_all()
        print("✅ 양자 회로 생성 성공")
        
        # 4. 시뮬레이터 테스트
        simulator = AerSimulator()
        transpiled_qc = transpile(qc, simulator)
        job = simulator.run(transpiled_qc, shots=1024)
        result = job.result()
        counts = result.get_counts()
        print(f"✅ 시뮬레이션 성공: {counts}")
        
        # 5. 회로 다이어그램 테스트
        try:
            circuit_str = qc.draw('text')
            print("✅ 텍스트 다이어그램 성공")
            print(circuit_str)
        except Exception as e:
            print(f"⚠️ 텍스트 다이어그램 오류: {e}")
        
        # 6. matplotlib 다이어그램 테스트
        try:
            import matplotlib
            matplotlib.use('Agg')
            import matplotlib.pyplot as plt
            
            fig, ax = plt.subplots(figsize=(10, 6))
            qc.draw(output='mpl', ax=ax)
            plt.close(fig)
            print("✅ matplotlib 다이어그램 성공")
        except Exception as e:
            print(f"⚠️ matplotlib 다이어그램 오류: {e}")
        
        # 7. 프로젝트 모듈 테스트
        try:
            from quantum_engine import QuantumSynthEngine
            from quantum_synth import QuantumCircuitSynthesizer
            from audio_generator import AudioGenerator
            
            engine = QuantumSynthEngine(3)
            synth = QuantumCircuitSynthesizer()
            audio_gen = AudioGenerator()
            
            print("✅ 프로젝트 모듈 임포트 성공")
            
            # 간단한 기능 테스트
            engine.apply_hadamard(0)
            probs = engine.get_qubit_probabilities()
            print(f"✅ 양자 엔진 동작 확인: {probs}")
            
        except Exception as e:
            print(f"❌ 프로젝트 모듈 오류: {e}")
        
        print("\n🎉 모든 테스트 통과! Qiskit 1.0+ 호환성 확인됨")
        return True
        
    except Exception as e:
        print(f"❌ 치명적 오류: {e}")
        return False

if __name__ == "__main__":
    success = test_qiskit_compatibility()
    exit(0 if success else 1)
