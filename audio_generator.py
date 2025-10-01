"""
Audio Generation Module
오디오 생성 모듈 - 사인파 생성 및 WAV 파일 처리
"""

import numpy as np
import scipy.io.wavfile as wavfile
from typing import List, Dict, Tuple, Optional
import io
import base64
import logging

# 로깅 설정
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class AudioGenerator:
    """오디오 생성 클래스"""
    
    def __init__(self, sample_rate: int = 44100):
        """
        오디오 생성기 초기화
        
        Args:
            sample_rate: 샘플링 레이트 (Hz)
        """
        self.sample_rate = sample_rate
        self.bit_depth = 16  # 16-bit audio
        logger.info(f"AudioGenerator initialized with sample_rate={sample_rate}Hz")
    
    def generate_sine_wave(self, 
                          frequency: float, 
                          duration: float, 
                          amplitude: float = 0.5,
                          phase: float = 0.0) -> np.ndarray:
        """
        사인파 생성
        
        Args:
            frequency: 주파수 (Hz)
            duration: 지속 시간 (초)
            amplitude: 진폭 (0.0 ~ 1.0)
            phase: 위상 (라디안)
            
        Returns:
            사인파 오디오 데이터
        """
        if frequency <= 0 or duration <= 0:
            return np.zeros(int(self.sample_rate * duration))
        
        # 시간 배열 생성
        t = np.linspace(0, duration, int(self.sample_rate * duration), False)
        
        # 사인파 생성
        wave = amplitude * np.sin(2 * np.pi * frequency * t + phase)
        
        # 페이드 인/아웃 적용 (클릭 노이즈 방지)
        fade_samples = int(0.01 * self.sample_rate)  # 10ms 페이드
        if len(wave) > 2 * fade_samples:
            # 페이드 인
            wave[:fade_samples] *= np.linspace(0, 1, fade_samples)
            # 페이드 아웃
            wave[-fade_samples:] *= np.linspace(1, 0, fade_samples)
        
        return wave
    
    def generate_harmonic_chord(self, 
                               base_frequency: float, 
                               duration: float,
                               amplitude: float = 0.5,
                               harmonics: List[float] = [1.0, 1.25, 1.5]) -> np.ndarray:
        """
        하모닉 화음 생성 (하다마드 게이트용)
        
        Args:
            base_frequency: 기본 주파수 (Hz)
            duration: 지속 시간 (초)
            amplitude: 전체 진폭
            harmonics: 하모닉 비율 리스트
            
        Returns:
            화음 오디오 데이터
        """
        chord = np.zeros(int(self.sample_rate * duration))
        
        for i, harmonic_ratio in enumerate(harmonics):
            freq = base_frequency * harmonic_ratio
            harmonic_amp = amplitude / len(harmonics) * (1.0 - i * 0.1)  # 점진적 감소
            
            harmonic_wave = self.generate_sine_wave(
                frequency=freq,
                duration=duration,
                amplitude=harmonic_amp
            )
            
            chord += harmonic_wave
        
        # 정규화
        if np.max(np.abs(chord)) > 0:
            chord = chord / np.max(np.abs(chord)) * amplitude
        
        return chord
    
    def generate_toggle_wave(self, 
                            frequency: float, 
                            duration: float,
                            amplitude: float = 0.5,
                            is_on: bool = True) -> np.ndarray:
        """
        토글 파형 생성 (Pauli-X 게이트용)
        
        Args:
            frequency: 주파수 (Hz)
            duration: 지속 시간 (초)
            amplitude: 진폭
            is_on: ON/OFF 상태
            
        Returns:
            토글 파형 오디오 데이터
        """
        if not is_on:
            return np.zeros(int(self.sample_rate * duration))
        
        # 강한 기본파 + 약한 배음으로 "부스트" 효과
        base_wave = self.generate_sine_wave(frequency, duration, amplitude)
        boost_wave = self.generate_sine_wave(frequency * 2, duration, amplitude * 0.3)
        
        return base_wave + boost_wave
    
    def generate_synchronized_harmony(self, 
                                    frequencies: List[float], 
                                    duration: float,
                                    amplitudes: List[float],
                                    sync_factor: float = 1.0) -> np.ndarray:
        """
        동기화된 하모니 생성 (CNOT 게이트용)
        
        Args:
            frequencies: 주파수 리스트
            duration: 지속 시간 (초)
            amplitudes: 각 주파수별 진폭 리스트
            sync_factor: 동기화 강도 (0.0 ~ 1.0)
            
        Returns:
            동기화된 하모니 오디오 데이터
        """
        if len(frequencies) != len(amplitudes):
            raise ValueError("Frequencies and amplitudes must have same length")
        
        harmony = np.zeros(int(self.sample_rate * duration))
        
        # 기본 하모니 생성
        for freq, amp in zip(frequencies, amplitudes):
            if amp > 0.01:  # 최소 임계값
                wave = self.generate_sine_wave(freq, duration, amp)
                harmony += wave
        
        # 동기화 효과 (비트 주파수 추가)
        if sync_factor > 0 and len(frequencies) >= 2:
            beat_freq = abs(frequencies[0] - frequencies[1]) * sync_factor
            if beat_freq > 0:
                t = np.linspace(0, duration, int(self.sample_rate * duration), False)
                beat_envelope = 0.5 * (1 + np.cos(2 * np.pi * beat_freq * t))
                harmony *= beat_envelope
        
        # 정규화
        if np.max(np.abs(harmony)) > 0:
            harmony = harmony / np.max(np.abs(harmony)) * max(amplitudes)
        
        return harmony
    
    def mix_audio_tracks(self, tracks: List[np.ndarray], weights: List[float] = None) -> np.ndarray:
        """
        여러 오디오 트랙 믹싱
        
        Args:
            tracks: 오디오 트랙 리스트
            weights: 각 트랙의 가중치 (None이면 균등)
            
        Returns:
            믹싱된 오디오 데이터
        """
        if not tracks:
            return np.array([])
        
        # 모든 트랙을 같은 길이로 맞춤
        max_length = max(len(track) for track in tracks)
        normalized_tracks = []
        
        for track in tracks:
            if len(track) < max_length:
                # 제로 패딩
                padded_track = np.pad(track, (0, max_length - len(track)), 'constant')
                normalized_tracks.append(padded_track)
            else:
                normalized_tracks.append(track[:max_length])
        
        # 가중치 설정
        if weights is None:
            weights = [1.0] * len(tracks)
        elif len(weights) != len(tracks):
            raise ValueError("Weights must have same length as tracks")
        
        # 믹싱
        mixed = np.zeros(max_length)
        for track, weight in zip(normalized_tracks, weights):
            mixed += track * weight
        
        # 정규화 (클리핑 방지)
        if np.max(np.abs(mixed)) > 0:
            mixed = mixed / np.max(np.abs(mixed)) * 0.8  # 80% 최대값으로 제한
        
        return mixed
    
    def apply_envelope(self, audio: np.ndarray, 
                      attack: float = 0.1, 
                      decay: float = 0.1, 
                      sustain: float = 0.7, 
                      release: float = 0.2) -> np.ndarray:
        """
        ADSR 엔벨로프 적용
        
        Args:
            audio: 입력 오디오 데이터
            attack: 어택 시간 (초)
            decay: 디케이 시간 (초)
            sustain: 서스테인 레벨 (0.0 ~ 1.0)
            release: 릴리즈 시간 (초)
            
        Returns:
            엔벨로프가 적용된 오디오 데이터
        """
        if len(audio) == 0:
            return audio
        
        duration = len(audio) / self.sample_rate
        envelope = np.ones(len(audio))
        
        # 샘플 수 계산
        attack_samples = int(attack * self.sample_rate)
        decay_samples = int(decay * self.sample_rate)
        release_samples = int(release * self.sample_rate)
        
        # 어택 구간
        if attack_samples > 0 and attack_samples < len(audio):
            envelope[:attack_samples] = np.linspace(0, 1, attack_samples)
        
        # 디케이 구간
        decay_start = attack_samples
        decay_end = min(decay_start + decay_samples, len(audio))
        if decay_end > decay_start:
            envelope[decay_start:decay_end] = np.linspace(1, sustain, decay_end - decay_start)
        
        # 서스테인 구간 (중간 부분)
        sustain_start = decay_end
        sustain_end = max(0, len(audio) - release_samples)
        if sustain_end > sustain_start:
            envelope[sustain_start:sustain_end] = sustain
        
        # 릴리즈 구간
        if release_samples > 0 and sustain_end < len(audio):
            envelope[sustain_end:] = np.linspace(sustain, 0, len(audio) - sustain_end)
        
        return audio * envelope
    
    def to_wav_bytes(self, audio: np.ndarray) -> bytes:
        """
        오디오 데이터를 WAV 바이트로 변환
        
        Args:
            audio: 오디오 데이터
            
        Returns:
            WAV 형식 바이트 데이터
        """
        # 16-bit 정수로 변환
        audio_int16 = (audio * 32767).astype(np.int16)
        
        # 메모리 버퍼에 WAV 파일 작성
        buffer = io.BytesIO()
        wavfile.write(buffer, self.sample_rate, audio_int16)
        buffer.seek(0)
        
        return buffer.getvalue()
    
    def save_wav_file(self, audio: np.ndarray, filename: str):
        """
        오디오 데이터를 WAV 파일로 저장
        
        Args:
            audio: 오디오 데이터
            filename: 저장할 파일명
        """
        # 16-bit 정수로 변환
        audio_int16 = (audio * 32767).astype(np.int16)
        
        # WAV 파일 저장
        wavfile.write(filename, self.sample_rate, audio_int16)
        logger.info(f"Audio saved to {filename}")
    
    def get_audio_base64(self, audio: np.ndarray) -> str:
        """
        오디오 데이터를 Base64 문자열로 변환 (웹 재생용)
        
        Args:
            audio: 오디오 데이터
            
        Returns:
            Base64 인코딩된 WAV 데이터
        """
        wav_bytes = self.to_wav_bytes(audio)
        return base64.b64encode(wav_bytes).decode('utf-8')


class QuantumAudioMapper:
    """양자 상태를 오디오로 매핑하는 클래스"""
    
    def __init__(self, audio_generator: AudioGenerator):
        """
        양자 오디오 매퍼 초기화
        
        Args:
            audio_generator: AudioGenerator 인스턴스
        """
        self.audio_gen = audio_generator
        
        # 큐빗별 기본 주파수 (Hz)
        self.qubit_frequencies = {
            0: 220.0,  # Bass Line (A3)
            1: 330.0,  # Melody (E4)
            2: 440.0,  # Harmony (A4)
        }
        
        # 게이트별 오디오 효과 설정
        self.gate_effects = {
            'h': 'harmonic_chord',      # 하다마드 → 화음
            'x': 'toggle_wave',         # Pauli-X → 토글
            'cx': 'synchronized_harmony' # CNOT → 동기화 하모니
        }
    
    def probability_to_amplitude(self, probability: float, min_threshold: float = 0.1) -> float:
        """
        확률을 오디오 진폭으로 변환
        
        Args:
            probability: 측정 확률 (0.0 ~ 1.0)
            min_threshold: 최소 임계값 (이하는 무음)
            
        Returns:
            오디오 진폭 (0.0 ~ 1.0)
        """
        if probability < min_threshold:
            return 0.0
        
        # 로그 스케일 적용 (작은 확률도 들리도록)
        normalized_prob = (probability - min_threshold) / (1.0 - min_threshold)
        return np.sqrt(normalized_prob)  # 제곱근으로 더 자연스러운 볼륨 곡선
    
    def generate_qubit_audio(self, 
                           qubit_id: int, 
                           probability: float, 
                           gate_type: str,
                           duration: float = 1.0) -> np.ndarray:
        """
        특정 큐빗의 오디오 생성
        
        Args:
            qubit_id: 큐빗 ID
            probability: 측정 확률
            gate_type: 적용된 게이트 타입
            duration: 지속 시간 (초)
            
        Returns:
            생성된 오디오 데이터
        """
        if qubit_id not in self.qubit_frequencies:
            return np.zeros(int(self.audio_gen.sample_rate * duration))
        
        frequency = self.qubit_frequencies[qubit_id]
        amplitude = self.probability_to_amplitude(probability)
        
        if amplitude == 0.0:
            return np.zeros(int(self.audio_gen.sample_rate * duration))
        
        # 게이트 타입에 따른 오디오 생성
        if gate_type == 'h':
            # 하다마드: 화음 효과
            return self.audio_gen.generate_harmonic_chord(
                base_frequency=frequency,
                duration=duration,
                amplitude=amplitude
            )
        elif gate_type == 'x':
            # Pauli-X: 토글 효과
            return self.audio_gen.generate_toggle_wave(
                frequency=frequency,
                duration=duration,
                amplitude=amplitude,
                is_on=probability > 0.5
            )
        else:
            # 기본: 사인파
            return self.audio_gen.generate_sine_wave(
                frequency=frequency,
                duration=duration,
                amplitude=amplitude
            )


if __name__ == "__main__":
    # 테스트 코드
    print("=== Audio Generator Test ===")
    
    # 오디오 생성기 초기화
    audio_gen = AudioGenerator(sample_rate=44100)
    
    # 테스트 사인파 생성
    sine_wave = audio_gen.generate_sine_wave(440.0, 1.0, 0.5)
    print(f"Generated sine wave: {len(sine_wave)} samples")
    
    # 화음 생성 테스트
    chord = audio_gen.generate_harmonic_chord(220.0, 1.0, 0.5)
    print(f"Generated chord: {len(chord)} samples")
    
    # 양자 오디오 매퍼 테스트
    mapper = QuantumAudioMapper(audio_gen)
    qubit_audio = mapper.generate_qubit_audio(0, 0.7, 'h', 1.0)
    print(f"Generated qubit audio: {len(qubit_audio)} samples")
    
    print("Audio generation test completed!")
