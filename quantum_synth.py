"""
Quantum Circuit Synthesizer - Main Integration Logic
양자 회로 신디사이저 메인 통합 로직
"""

import numpy as np
from typing import Dict, List, Tuple, Optional, Any
import logging
from dataclasses import dataclass
import time

from quantum_engine import QuantumSynthEngine, create_demo_circuits
from audio_generator import AudioGenerator, QuantumAudioMapper

# 로깅 설정
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class SynthConfig:
    """신디사이저 설정 클래스"""
    sample_rate: int = 44100
    default_duration: float = 2.0
    num_qubits: int = 3
    measurement_shots: int = 1024
    min_probability_threshold: float = 0.1
    enable_envelope: bool = True
    master_volume: float = 0.8


@dataclass
class AudioTrack:
    """오디오 트랙 데이터 클래스"""
    qubit_id: int
    frequency: float
    probability: float
    amplitude: float
    gate_type: str
    audio_data: np.ndarray
    duration: float


class QuantumCircuitSynthesizer:
    """양자 회로 신디사이저 메인 클래스"""
    
    def __init__(self, config: SynthConfig = None):
        """
        양자 신디사이저 초기화
        
        Args:
            config: 신디사이저 설정
        """
        self.config = config or SynthConfig()
        
        # 컴포넌트 초기화
        self.quantum_engine = QuantumSynthEngine(self.config.num_qubits)
        self.audio_generator = AudioGenerator(self.config.sample_rate)
        self.audio_mapper = QuantumAudioMapper(self.audio_generator)
        
        # 상태 변수
        self.current_tracks: List[AudioTrack] = []
        self.synthesis_history: List[Dict] = []
        self.is_playing = False
        
        logger.info("QuantumCircuitSynthesizer initialized")
    
    def reset_circuit(self):
        """양자 회로 및 오디오 트랙 초기화"""
        self.quantum_engine.reset_circuit()
        self.current_tracks.clear()
        self.is_playing = False
        logger.info("Circuit and tracks reset")
    
    def add_hadamard_gate(self, qubit: int) -> Dict[str, Any]:
        """
        하다마드 게이트 추가 및 오디오 생성
        
        Args:
            qubit: 타겟 큐빗
            
        Returns:
            게이트 적용 결과 정보
        """
        try:
            # 양자 게이트 적용
            self.quantum_engine.apply_hadamard(qubit)
            
            # 측정 및 오디오 생성
            result = self._synthesize_current_state('h', qubit)
            
            logger.info(f"Hadamard gate added to qubit {qubit}")
            return {
                'success': True,
                'gate_type': 'hadamard',
                'qubit': qubit,
                'result': result
            }
            
        except Exception as e:
            logger.error(f"Error adding Hadamard gate: {e}")
            return {
                'success': False,
                'error': str(e)
            }
    
    def add_pauli_x_gate(self, qubit: int) -> Dict[str, Any]:
        """
        Pauli-X 게이트 추가 및 오디오 생성
        
        Args:
            qubit: 타겟 큐빗
            
        Returns:
            게이트 적용 결과 정보
        """
        try:
            # 양자 게이트 적용
            self.quantum_engine.apply_pauli_x(qubit)
            
            # 측정 및 오디오 생성
            result = self._synthesize_current_state('x', qubit)
            
            logger.info(f"Pauli-X gate added to qubit {qubit}")
            return {
                'success': True,
                'gate_type': 'pauli_x',
                'qubit': qubit,
                'result': result
            }
            
        except Exception as e:
            logger.error(f"Error adding Pauli-X gate: {e}")
            return {
                'success': False,
                'error': str(e)
            }
    
    def add_cnot_gate(self, control: int, target: int) -> Dict[str, Any]:
        """
        CNOT 게이트 추가 및 오디오 생성
        
        Args:
            control: 제어 큐빗
            target: 타겟 큐빗
            
        Returns:
            게이트 적용 결과 정보
        """
        try:
            # 양자 게이트 적용
            self.quantum_engine.apply_cnot(control, target)
            
            # 측정 및 오디오 생성 (두 큐빗 모두 영향)
            result = self._synthesize_current_state('cx', [control, target])
            
            logger.info(f"CNOT gate added: control={control}, target={target}")
            return {
                'success': True,
                'gate_type': 'cnot',
                'control': control,
                'target': target,
                'result': result
            }
            
        except Exception as e:
            logger.error(f"Error adding CNOT gate: {e}")
            return {
                'success': False,
                'error': str(e)
            }
    
    def _synthesize_current_state(self, gate_type: str, affected_qubits) -> Dict[str, Any]:
        """
        현재 양자 상태를 오디오로 합성
        
        Args:
            gate_type: 적용된 게이트 타입
            affected_qubits: 영향받은 큐빗(들)
            
        Returns:
            합성 결과 정보
        """
        # 큐빗 확률 측정
        qubit_probabilities = self.quantum_engine.get_qubit_probabilities(
            self.config.measurement_shots
        )
        
        # 오디오 트랙 생성
        new_tracks = []
        
        if gate_type == 'cx' and isinstance(affected_qubits, list):
            # CNOT: 동기화된 하모니 생성
            frequencies = [self.audio_mapper.qubit_frequencies[q] for q in affected_qubits]
            amplitudes = [
                self.audio_mapper.probability_to_amplitude(qubit_probabilities[q])
                for q in affected_qubits
            ]
            
            # 동기화된 하모니 생성
            harmony_audio = self.audio_generator.generate_synchronized_harmony(
                frequencies=frequencies,
                duration=self.config.default_duration,
                amplitudes=amplitudes,
                sync_factor=0.8
            )
            
            # 각 큐빗별 트랙 생성
            for i, qubit in enumerate(affected_qubits):
                track = AudioTrack(
                    qubit_id=qubit,
                    frequency=frequencies[i],
                    probability=qubit_probabilities[qubit],
                    amplitude=amplitudes[i],
                    gate_type=gate_type,
                    audio_data=harmony_audio * (amplitudes[i] / max(amplitudes) if max(amplitudes) > 0 else 0),
                    duration=self.config.default_duration
                )
                new_tracks.append(track)
        
        else:
            # 단일 큐빗 게이트들
            if isinstance(affected_qubits, list):
                qubits_to_process = affected_qubits
            else:
                qubits_to_process = [affected_qubits]
            
            for qubit in qubits_to_process:
                probability = qubit_probabilities[qubit]
                amplitude = self.audio_mapper.probability_to_amplitude(probability)
                
                # 큐빗별 오디오 생성
                audio_data = self.audio_mapper.generate_qubit_audio(
                    qubit_id=qubit,
                    probability=probability,
                    gate_type=gate_type,
                    duration=self.config.default_duration
                )
                
                # 엔벨로프 적용
                if self.config.enable_envelope and len(audio_data) > 0:
                    audio_data = self.audio_generator.apply_envelope(audio_data)
                
                track = AudioTrack(
                    qubit_id=qubit,
                    frequency=self.audio_mapper.qubit_frequencies[qubit],
                    probability=probability,
                    amplitude=amplitude,
                    gate_type=gate_type,
                    audio_data=audio_data,
                    duration=self.config.default_duration
                )
                new_tracks.append(track)
        
        # 트랙 업데이트
        self.current_tracks = new_tracks
        
        # 히스토리 저장
        synthesis_record = {
            'timestamp': time.time(),
            'gate_type': gate_type,
            'affected_qubits': affected_qubits,
            'probabilities': qubit_probabilities,
            'num_tracks': len(new_tracks)
        }
        self.synthesis_history.append(synthesis_record)
        
        return {
            'probabilities': qubit_probabilities,
            'tracks': new_tracks,
            'synthesis_record': synthesis_record
        }
    
    def get_mixed_audio(self, normalize: bool = True) -> np.ndarray:
        """
        모든 트랙을 믹싱하여 최종 오디오 생성
        
        Args:
            normalize: 정규화 여부
            
        Returns:
            믹싱된 오디오 데이터
        """
        if not self.current_tracks:
            return np.zeros(int(self.config.sample_rate * self.config.default_duration))
        
        # 트랙별 오디오 데이터 수집
        track_audios = [track.audio_data for track in self.current_tracks if len(track.audio_data) > 0]
        
        if not track_audios:
            return np.zeros(int(self.config.sample_rate * self.config.default_duration))
        
        # 트랙 가중치 (확률 기반)
        weights = [track.amplitude for track in self.current_tracks if len(track.audio_data) > 0]
        
        # 믹싱
        mixed_audio = self.audio_generator.mix_audio_tracks(track_audios, weights)
        
        # 마스터 볼륨 적용
        mixed_audio *= self.config.master_volume
        
        return mixed_audio
    
    def get_track_info(self) -> List[Dict]:
        """
        현재 트랙 정보 반환
        
        Returns:
            트랙 정보 리스트
        """
        track_info = []
        for track in self.current_tracks:
            info = {
                'qubit_id': track.qubit_id,
                'frequency': track.frequency,
                'probability': track.probability,
                'amplitude': track.amplitude,
                'gate_type': track.gate_type,
                'duration': track.duration,
                'audio_length': len(track.audio_data)
            }
            track_info.append(info)
        
        return track_info
    
    def get_circuit_visualization_data(self) -> Dict:
        """
        회로 시각화용 데이터 반환
        
        Returns:
            시각화 데이터 딕셔너리
        """
        circuit_info = self.quantum_engine.get_circuit_info()
        gate_sequence = self.quantum_engine.get_gate_sequence()
        qubit_probs = self.quantum_engine.get_qubit_probabilities()
        
        return {
            'circuit_info': circuit_info,
            'gate_sequence': gate_sequence,
            'qubit_probabilities': qubit_probs,
            'track_info': self.get_track_info(),
            'synthesis_history': self.synthesis_history[-10:]  # 최근 10개만
        }
    
    def export_audio_file(self, filename: str = None) -> str:
        """
        현재 오디오를 WAV 파일로 내보내기
        
        Args:
            filename: 저장할 파일명 (None이면 자동 생성)
            
        Returns:
            저장된 파일명
        """
        if filename is None:
            timestamp = int(time.time())
            filename = f"quantum_synth_{timestamp}.wav"
        
        mixed_audio = self.get_mixed_audio()
        self.audio_generator.save_wav_file(mixed_audio, filename)
        
        return filename
    
    def get_audio_base64(self) -> str:
        """
        현재 오디오를 Base64 문자열로 반환 (웹 재생용)
        
        Returns:
            Base64 인코딩된 오디오 데이터
        """
        mixed_audio = self.get_mixed_audio()
        return self.audio_generator.get_audio_base64(mixed_audio)
    
    def load_demo_circuit(self, demo_name: str) -> Dict[str, Any]:
        """
        데모 회로 로드
        
        Args:
            demo_name: 데모 이름 ('superposition', 'mixed_states', 'entanglement')
            
        Returns:
            로드 결과 정보
        """
        try:
            demo_circuits = create_demo_circuits()
            
            if demo_name not in demo_circuits:
                return {
                    'success': False,
                    'error': f"Demo '{demo_name}' not found"
                }
            
            # 데모 회로 복사
            demo_engine = demo_circuits[demo_name]
            self.quantum_engine.circuit = demo_engine.circuit.copy()
            
            # 오디오 합성
            result = self._synthesize_current_state('demo', list(range(self.config.num_qubits)))
            
            logger.info(f"Demo circuit '{demo_name}' loaded")
            return {
                'success': True,
                'demo_name': demo_name,
                'result': result
            }
            
        except Exception as e:
            logger.error(f"Error loading demo circuit: {e}")
            return {
                'success': False,
                'error': str(e)
            }


def create_preset_synthesizers() -> Dict[str, QuantumCircuitSynthesizer]:
    """
    프리셋 신디사이저들 생성
    
    Returns:
        프리셋 신디사이저 딕셔너리
    """
    presets = {}
    
    # 기본 설정
    default_config = SynthConfig()
    presets['default'] = QuantumCircuitSynthesizer(default_config)
    
    # 고음질 설정
    hq_config = SynthConfig(
        sample_rate=48000,
        default_duration=3.0,
        measurement_shots=2048,
        master_volume=0.9
    )
    presets['high_quality'] = QuantumCircuitSynthesizer(hq_config)
    
    # 빠른 응답 설정
    fast_config = SynthConfig(
        sample_rate=22050,
        default_duration=1.0,
        measurement_shots=512,
        enable_envelope=False
    )
    presets['fast_response'] = QuantumCircuitSynthesizer(fast_config)
    
    return presets


if __name__ == "__main__":
    # 테스트 코드
    print("=== Quantum Circuit Synthesizer Test ===")
    
    # 신디사이저 초기화
    synth = QuantumCircuitSynthesizer()
    
    # 게이트 적용 테스트
    print("\n1. Adding Hadamard gate to qubit 0...")
    result1 = synth.add_hadamard_gate(0)
    print(f"Result: {result1['success']}")
    
    print("\n2. Adding Pauli-X gate to qubit 1...")
    result2 = synth.add_pauli_x_gate(1)
    print(f"Result: {result2['success']}")
    
    print("\n3. Adding CNOT gate (0 -> 2)...")
    result3 = synth.add_cnot_gate(0, 2)
    print(f"Result: {result3['success']}")
    
    # 트랙 정보 출력
    print("\n4. Track information:")
    track_info = synth.get_track_info()
    for i, track in enumerate(track_info):
        print(f"  Track {i}: Qubit {track['qubit_id']}, "
              f"Freq: {track['frequency']:.1f}Hz, "
              f"Prob: {track['probability']:.3f}")
    
    # 오디오 생성 테스트
    print("\n5. Generating mixed audio...")
    mixed_audio = synth.get_mixed_audio()
    print(f"Mixed audio length: {len(mixed_audio)} samples")
    
    # 시각화 데이터
    print("\n6. Visualization data:")
    viz_data = synth.get_circuit_visualization_data()
    print(f"Circuit depth: {viz_data['circuit_info']['circuit_depth']}")
    print(f"Gate count: {viz_data['circuit_info']['gate_count']}")
    
    print("\nQuantum synthesizer test completed!")
