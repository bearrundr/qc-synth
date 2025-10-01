#!/usr/bin/env python3
"""
웹 애플리케이션에서 X 게이트 테스트
"""

from quantum_synth import QuantumCircuitSynthesizer, SynthConfig
import numpy as np

def test_x_gate_in_web_context():
    """웹 애플리케이션 컨텍스트에서 X 게이트 테스트"""
    print("=== 웹 애플리케이션 X 게이트 테스트 ===")
    
    # 신디사이저 초기화 (웹 애플리케이션과 동일한 설정)
    config = SynthConfig(
        num_qubits=3,
        sample_rate=44100,
        default_duration=2.0,
        min_probability_threshold=0.1,
        master_volume=0.8
    )
    synth = QuantumCircuitSynthesizer(config)
    
    print(f"초기 설정:")
    print(f"- 큐빗 수: {config.num_qubits}")
    print(f"- 샘플레이트: {config.sample_rate}")
    print(f"- 기본 지속시간: {config.default_duration}")
    print(f"- 마스터 볼륨: {config.master_volume}")
    print(f"- 최소 확률 임계값: {config.min_probability_threshold}")
    
    # 1. H 게이트 먼저 테스트 (비교용)
    print(f"\n1. H 게이트 테스트 (큐빗 0)")
    result_h = synth.add_hadamard_gate(0)
    print(f"H 게이트 결과: {result_h['success']}")
    
    if result_h['success']:
        viz_data = synth.get_circuit_visualization_data()
        print(f"큐빗 확률: {viz_data['qubit_probabilities']}")
        
        try:
            mixed_audio = synth.get_mixed_audio()
            print(f"H 게이트 오디오 길이: {len(mixed_audio)}")
            print(f"H 게이트 오디오 최대값: {max(mixed_audio) if len(mixed_audio) > 0 else 0:.6f}")
            print(f"H 게이트 오디오 RMS: {np.sqrt(np.mean(mixed_audio**2)):.6f}")
        except Exception as e:
            print(f"H 게이트 오디오 오류: {e}")
    
    # 회로 리셋
    synth.reset_circuit()
    
    # 2. X 게이트 테스트
    print(f"\n2. X 게이트 테스트 (큐빗 0)")
    result_x = synth.add_pauli_x_gate(0)
    print(f"X 게이트 결과: {result_x['success']}")
    
    if result_x['success']:
        viz_data = synth.get_circuit_visualization_data()
        print(f"큐빗 확률: {viz_data['qubit_probabilities']}")
        
        try:
            mixed_audio = synth.get_mixed_audio()
            print(f"X 게이트 오디오 길이: {len(mixed_audio)}")
            print(f"X 게이트 오디오 최대값: {max(mixed_audio) if len(mixed_audio) > 0 else 0:.6f}")
            print(f"X 게이트 오디오 RMS: {np.sqrt(np.mean(mixed_audio**2)):.6f}")
            
            # 오디오 데이터 분석
            non_zero_samples = np.count_nonzero(mixed_audio)
            print(f"X 게이트 0이 아닌 샘플 수: {non_zero_samples}/{len(mixed_audio)}")
            
            # Base64 테스트
            audio_base64 = synth.get_audio_base64()
            print(f"X 게이트 Base64 길이: {len(audio_base64)}")
            
        except Exception as e:
            print(f"X 게이트 오디오 오류: {e}")
    
    # 3. 여러 X 게이트 테스트
    print(f"\n3. 여러 X 게이트 테스트")
    synth.reset_circuit()
    
    # 모든 큐빗에 X 게이트 적용
    for i in range(3):
        result = synth.add_pauli_x_gate(i)
        print(f"X 게이트 Q{i}: {result['success']}")
    
    viz_data = synth.get_circuit_visualization_data()
    print(f"모든 X 게이트 후 확률: {viz_data['qubit_probabilities']}")
    
    try:
        mixed_audio = synth.get_mixed_audio()
        print(f"모든 X 게이트 오디오 길이: {len(mixed_audio)}")
        print(f"모든 X 게이트 오디오 최대값: {max(mixed_audio) if len(mixed_audio) > 0 else 0:.6f}")
        print(f"모든 X 게이트 오디오 RMS: {np.sqrt(np.mean(mixed_audio**2)):.6f}")
        
        # 트랙 정보
        track_info = synth.get_track_info()
        print(f"트랙 수: {len(track_info)}")
        for i, track in enumerate(track_info):
            print(f"  트랙 {i}: Q{track['qubit_id']}, 주파수={track['frequency']}Hz, 진폭={track['amplitude']:.3f}")
            
    except Exception as e:
        print(f"모든 X 게이트 오디오 오류: {e}")
    
    # 4. 토글 웨이브 직접 테스트
    print(f"\n4. 토글 웨이브 직접 테스트")
    from audio_generator import AudioGenerator
    
    audio_gen = AudioGenerator(44100)
    
    # 다양한 설정으로 토글 웨이브 테스트
    test_cases = [
        (220.0, 1.0, 0.8, True),   # 정상 케이스
        (220.0, 1.0, 0.8, False),  # OFF 케이스
        (330.0, 2.0, 1.0, True),   # 다른 주파수
    ]
    
    for freq, dur, amp, is_on in test_cases:
        toggle_wave = audio_gen.generate_toggle_wave(freq, dur, amp, is_on)
        print(f"토글웨이브 ({freq}Hz, {dur}s, {amp}, {is_on}): 길이={len(toggle_wave)}, 최대값={max(toggle_wave) if len(toggle_wave) > 0 else 0:.6f}")

if __name__ == "__main__":
    test_x_gate_in_web_context()
