#!/usr/bin/env python3
"""
X 게이트 오디오 생성 디버깅
"""

from quantum_synth import QuantumCircuitSynthesizer, SynthConfig
from quantum_engine import QuantumSynthEngine

def debug_x_gate_audio():
    """X 게이트 오디오 생성 디버깅"""
    print("=== X 게이트 오디오 디버깅 ===")
    
    # 신디사이저 초기화
    config = SynthConfig()
    synth = QuantumCircuitSynthesizer(config)
    
    print("\n1. 초기 상태 (모든 큐빗 |0⟩)")
    viz_data = synth.get_circuit_visualization_data()
    print(f"큐빗 확률: {viz_data['qubit_probabilities']}")
    
    # 오디오 트랙 정보
    track_info = synth.get_track_info()
    print(f"트랙 수: {len(track_info)}")
    for i, track in enumerate(track_info):
        print(f"  트랙 {i}: {track}")
    
    print("\n2. X 게이트 적용 (큐빗 0)")
    result = synth.add_pauli_x_gate(0)
    print(f"X 게이트 결과: {result}")
    
    # 상태 확인
    viz_data = synth.get_circuit_visualization_data()
    print(f"큐빗 확률: {viz_data['qubit_probabilities']}")
    
    # 오디오 트랙 정보
    track_info = synth.get_track_info()
    print(f"트랙 수: {len(track_info)}")
    for i, track in enumerate(track_info):
        print(f"  트랙 {i}: {track}")
    
    print("\n3. X 게이트 적용 (큐빗 1)")
    result = synth.add_pauli_x_gate(1)
    print(f"X 게이트 결과: {result}")
    
    # 상태 확인
    viz_data = synth.get_circuit_visualization_data()
    print(f"큐빗 확률: {viz_data['qubit_probabilities']}")
    
    # 오디오 트랙 정보
    track_info = synth.get_track_info()
    print(f"트랙 수: {len(track_info)}")
    for i, track in enumerate(track_info):
        print(f"  트랙 {i}: {track}")
    
    print("\n4. 오디오 생성 테스트")
    try:
        mixed_audio = synth.get_mixed_audio()
        print(f"오디오 길이: {len(mixed_audio)} 샘플")
        print(f"오디오 최대값: {max(mixed_audio) if len(mixed_audio) > 0 else 0}")
        print(f"오디오 최소값: {min(mixed_audio) if len(mixed_audio) > 0 else 0}")
        
        # Base64 인코딩 테스트
        audio_base64 = synth.get_audio_base64()
        print(f"Base64 길이: {len(audio_base64)} 문자")
        
    except Exception as e:
        print(f"오디오 생성 오류: {e}")
    
    print("\n5. 직접 X 게이트 테스트")
    engine = QuantumSynthEngine(3)
    
    print("초기 상태:")
    probs = engine.get_qubit_probabilities()
    print(f"큐빗 확률: {probs}")
    
    print("\nX 게이트 적용 후:")
    engine.apply_pauli_x(0)
    probs = engine.get_qubit_probabilities()
    print(f"큐빗 확률: {probs}")
    
    print("\n6. 오디오 매퍼 테스트")
    from audio_generator import AudioGenerator, QuantumAudioMapper
    
    audio_gen = AudioGenerator()
    mapper = QuantumAudioMapper(audio_gen)
    
    # 확률 1.0 (X 게이트 결과)에 대한 오디오 생성
    test_prob = 1.0
    amplitude = mapper.probability_to_amplitude(test_prob)
    print(f"확률 {test_prob} → 진폭 {amplitude}")
    
    # 토글 웨이브 생성 테스트
    frequency = 220.0  # A3
    duration = 1.0
    toggle_audio = audio_gen.generate_toggle_wave(frequency, duration, amplitude)
    print(f"토글 웨이브 길이: {len(toggle_audio)} 샘플")
    print(f"토글 웨이브 최대값: {max(toggle_audio) if len(toggle_audio) > 0 else 0}")

if __name__ == "__main__":
    debug_x_gate_audio()
