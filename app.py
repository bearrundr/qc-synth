"""
Quantum Circuit Synthesizer - Streamlit Web Interface
양자 회로 신디사이저 Streamlit 웹 인터페이스
"""

import streamlit as st
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import pandas as pd
import base64
import io
import time
from typing import Dict, List, Any

# 로컬 모듈 임포트
from quantum_synth import QuantumCircuitSynthesizer, SynthConfig
from quantum_engine import QuantumSynthEngine
from audio_generator import AudioGenerator

# 페이지 설정
st.set_page_config(
    page_title="🎵 Quantum Circuit Synthesizer",
    page_icon="🎵",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 커스텀 CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        text-align: center;
        color: #ffffff;
        margin-bottom: 2rem;
        padding: 2rem 1rem;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f093fb 100%);
        background-size: 400% 400%;
        animation: gradientShift 8s ease infinite;
        border-radius: 1rem;
        box-shadow: 0 8px 32px rgba(0,0,0,0.2);
        position: relative;
        overflow: hidden;
    }
    
    .main-header::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background-image: 
            /* 양자 회로 노드들 */
            radial-gradient(circle at 15% 25%, rgba(255,255,255,0.15) 3px, transparent 3px),
            radial-gradient(circle at 85% 75%, rgba(255,255,255,0.15) 3px, transparent 3px),
            radial-gradient(circle at 35% 85%, rgba(255,255,255,0.1) 2px, transparent 2px),
            radial-gradient(circle at 65% 15%, rgba(255,255,255,0.1) 2px, transparent 2px),
            radial-gradient(circle at 50% 50%, rgba(255,255,255,0.08) 1px, transparent 1px),
            /* 회로 연결선들 */
            linear-gradient(90deg, transparent 48%, rgba(255,255,255,0.12) 49%, rgba(255,255,255,0.12) 51%, transparent 52%),
            linear-gradient(0deg, transparent 48%, rgba(255,255,255,0.08) 49%, rgba(255,255,255,0.08) 51%, transparent 52%),
            linear-gradient(45deg, transparent 48%, rgba(255,255,255,0.06) 49%, rgba(255,255,255,0.06) 51%, transparent 52%),
            /* 음파 패턴 */
            repeating-linear-gradient(90deg, transparent, transparent 10px, rgba(255,255,255,0.04) 10px, rgba(255,255,255,0.04) 12px),
            repeating-linear-gradient(0deg, transparent, transparent 15px, rgba(255,255,255,0.03) 15px, rgba(255,255,255,0.03) 17px);
        background-size: 
            80px 80px, 90px 90px, 60px 60px, 70px 70px, 40px 40px,
            120px 120px, 150px 150px, 100px 100px,
            25px 25px, 30px 30px;
        background-position: 
            0 0, 40px 40px, 20px 20px, 60px 60px, 10px 10px,
            0 0, 0 0, 0 0,
            0 0, 0 0;
        animation: circuitFlow 20s linear infinite;
        z-index: 1;
    }
    
    .main-header h1 {
        position: relative;
        z-index: 2;
        margin: 0;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }
    
    @keyframes gradientShift {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
    @keyframes circuitFlow {
        0% { 
            transform: translateX(0) translateY(0) rotate(0deg);
            opacity: 0.8;
        }
        25% { 
            transform: translateX(-15px) translateY(-8px) rotate(1deg);
            opacity: 0.9;
        }
        50% { 
            transform: translateX(-30px) translateY(0) rotate(0deg);
            opacity: 1;
        }
        75% { 
            transform: translateX(-15px) translateY(8px) rotate(-1deg);
            opacity: 0.9;
        }
        100% { 
            transform: translateX(0) translateY(0) rotate(0deg);
            opacity: 0.8;
        }
    }
    
    /* 호버 효과 추가 */
    .main-header:hover {
        transform: scale(1.02);
        transition: transform 0.3s ease;
    }
    
    .main-header:hover::before {
        animation-duration: 10s;
    }
    .section-header {
        font-size: 1.5rem;
        font-weight: bold;
        color: #2c3e50;
        margin-top: 1rem;
        margin-bottom: 1rem;
    }
    .qubit-info {
        background-color: #f8f9fa;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1f77b4;
        margin: 0.5rem 0;
    }
    .gate-button {
        margin: 0.2rem;
    }
    .audio-player {
        margin: 1rem 0;
    }
    .metric-card {
        background-color: #ffffff;
        padding: 1rem;
        border-radius: 0.5rem;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        margin: 0.5rem 0;
    }
</style>
""", unsafe_allow_html=True)


@st.cache_resource
def initialize_synthesizer():
    """신디사이저 초기화 (캐시됨)"""
    config = SynthConfig(
        sample_rate=44100,
        default_duration=2.0,
        num_qubits=3,
        measurement_shots=1024,
        master_volume=0.8
    )
    return QuantumCircuitSynthesizer(config)


def create_probability_chart(probabilities: Dict[int, float]) -> go.Figure:
    """큐빗 확률 차트 생성"""
    qubits = list(probabilities.keys())
    probs = list(probabilities.values())
    
    colors = ['#FF6B6B', '#4ECDC4', '#45B7D1']
    
    fig = go.Figure(data=[
        go.Bar(
            x=[f'Qubit {q}' for q in qubits],
            y=probs,
            marker_color=colors[:len(qubits)],
            text=[f'{p:.3f}' for p in probs],
            textposition='auto',
        )
    ])
    
    fig.update_layout(
        title='Qubit Measurement Probabilities (|1⟩ state)',
        xaxis_title='Qubits',
        yaxis_title='Probability',
        yaxis=dict(range=[0, 1]),
        height=400,
        showlegend=False
    )
    
    return fig


def create_frequency_spectrum(track_info: List[Dict]) -> go.Figure:
    """주파수 스펙트럼 차트 생성"""
    if not track_info:
        fig = go.Figure()
        fig.add_annotation(text="No active tracks", 
                          xref="paper", yref="paper",
                          x=0.5, y=0.5, showarrow=False)
        return fig
    
    frequencies = [track['frequency'] for track in track_info]
    amplitudes = [track['amplitude'] for track in track_info]
    qubit_ids = [track['qubit_id'] for track in track_info]
    gate_types = [track['gate_type'] for track in track_info]
    
    colors = ['#FF6B6B', '#4ECDC4', '#45B7D1']
    
    fig = go.Figure()
    
    for i, (freq, amp, qubit, gate) in enumerate(zip(frequencies, amplitudes, qubit_ids, gate_types)):
        fig.add_trace(go.Scatter(
            x=[freq],
            y=[amp],
            mode='markers',
            marker=dict(
                size=max(20, amp * 100),
                color=colors[qubit % len(colors)],
                opacity=0.7
            ),
            name=f'Qubit {qubit} ({gate})',
            text=f'Qubit {qubit}<br>Freq: {freq:.1f}Hz<br>Amp: {amp:.3f}<br>Gate: {gate}',
            hovertemplate='%{text}<extra></extra>'
        ))
    
    fig.update_layout(
        title='Audio Frequency Spectrum',
        xaxis_title='Frequency (Hz)',
        yaxis_title='Amplitude',
        height=400,
        xaxis=dict(range=[200, 500]),
        yaxis=dict(range=[0, 1])
    )
    
    return fig


def create_circuit_diagram_visual(circuit, gate_sequence: List[Dict]):
    """Qiskit 회로 다이어그램 시각화"""
    import matplotlib
    matplotlib.use('Agg')  # GUI 없는 백엔드 사용
    import matplotlib.pyplot as plt
    from io import BytesIO
    import base64
    
    if not gate_sequence:
        return None, "Empty circuit"
    
    try:
        # matplotlib 설정
        plt.style.use('default')
        
        # 회로 크기에 따라 figure 크기 조정
        num_gates = len(gate_sequence)
        fig_width = max(8, min(16, 2 + num_gates * 1.5))
        fig_height = max(4, circuit.num_qubits * 1.5)
        
        fig, ax = plt.subplots(figsize=(fig_width, fig_height))
        
        # 회로 그리기 (다양한 스타일 시도)
        try:
            # IQP 스타일로 시도
            circuit.draw(output='mpl', ax=ax, style='iqp')
        except:
            try:
                # 기본 스타일로 시도
                circuit.draw(output='mpl', ax=ax)
            except:
                # 텍스트 출력으로 대체
                ax.text(0.5, 0.5, str(circuit), 
                       horizontalalignment='center',
                       verticalalignment='center',
                       transform=ax.transAxes,
                       fontfamily='monospace',
                       fontsize=10)
                ax.set_xlim(0, 1)
                ax.set_ylim(0, 1)
                ax.axis('off')
        
        # 제목 설정
        ax.set_title('🔬 Quantum Circuit Diagram', fontsize=14, fontweight='bold', pad=20)
        
        # 레이아웃 조정
        plt.tight_layout()
        
        # 이미지를 바이트로 변환
        buffer = BytesIO()
        plt.savefig(buffer, format='png', dpi=120, bbox_inches='tight', 
                   facecolor='white', edgecolor='none')
        buffer.seek(0)
        
        # Base64 인코딩
        img_base64 = base64.b64encode(buffer.getvalue()).decode()
        plt.close(fig)
        
        # 텍스트 다이어그램도 생성
        text_diagram = create_circuit_diagram_text(gate_sequence, circuit)
        
        return img_base64, text_diagram
        
    except Exception as e:
        # 오류 발생 시 텍스트 다이어그램만 반환
        text_diagram = create_circuit_diagram_text(gate_sequence, circuit)
        return None, text_diagram


def create_circuit_diagram_text(gate_sequence: List[Dict], circuit=None) -> str:
    """텍스트 기반 회로 다이어그램 생성"""
    if not gate_sequence:
        return "Empty circuit"
    
    # Qiskit 네이티브 텍스트 다이어그램 시도
    if circuit is not None:
        try:
            qiskit_text = circuit.draw('text')
            
            # 추가 정보와 함께 반환
            info_lines = [
                "🔬 Quantum Circuit Diagram",
                "=" * 60,
                "",
                str(qiskit_text),
                "",
                "📋 Gate Sequence:",
                "-" * 40
            ]
            
            for i, gate in enumerate(gate_sequence):
                gate_name = gate['name'].upper()
                qubits = gate['qubits']
                
                if gate_name == 'H':
                    info_lines.append(f"Step {i+1:2d}: 🌊 H gate on qubit {qubits[0]} (Hadamard - Superposition)")
                elif gate_name == 'X':
                    info_lines.append(f"Step {i+1:2d}: ⚡ X gate on qubit {qubits[0]} (Pauli-X - Bit Flip)")
                elif gate_name == 'CX':
                    info_lines.append(f"Step {i+1:2d}: 🔗 CNOT gate (control: Q{qubits[0]} → target: Q{qubits[1]}) (Entanglement)")
                else:
                    info_lines.append(f"Step {i+1:2d}: 🎛️ {gate_name} gate on qubits {qubits}")
            
            info_lines.extend([
                "",
                "=" * 60,
                f"Total gates: {len(gate_sequence)}",
                f"Circuit depth: {circuit.depth() if hasattr(circuit, 'depth') else len(gate_sequence)}"
            ])
            
            return "\n".join(info_lines)
            
        except Exception as e:
            # Qiskit 텍스트 다이어그램 실패 시 폴백
            pass
    
    # 폴백: 기본 텍스트 다이어그램
    diagram_lines = [
        "🔬 Quantum Circuit Diagram",
        "=" * 60,
        ""
    ]
    
    for i, gate in enumerate(gate_sequence):
        gate_name = gate['name'].upper()
        qubits = gate['qubits']
        
        if gate_name == 'H':
            diagram_lines.append(f"Step {i+1:2d}: 🌊 H gate on qubit {qubits[0]} (Hadamard - Superposition)")
        elif gate_name == 'X':
            diagram_lines.append(f"Step {i+1:2d}: ⚡ X gate on qubit {qubits[0]} (Pauli-X - Bit Flip)")
        elif gate_name == 'CX':
            diagram_lines.append(f"Step {i+1:2d}: 🔗 CNOT gate (control: Q{qubits[0]} → target: Q{qubits[1]}) (Entanglement)")
        else:
            diagram_lines.append(f"Step {i+1:2d}: 🎛️ {gate_name} gate on qubits {qubits}")
    
    diagram_lines.extend([
        "",
        "=" * 60,
        f"Total gates: {len(gate_sequence)}",
        f"Circuit depth: {max([len(gate_sequence), 1])}"
    ])
    
    return "\n".join(diagram_lines)


def create_audio_player(audio_base64: str) -> str:
    """HTML 오디오 플레이어 생성"""
    audio_html = f"""
    <audio controls class="audio-player">
        <source src="data:audio/wav;base64,{audio_base64}" type="audio/wav">
        Your browser does not support the audio element.
    </audio>
    """
    return audio_html


def main():
    """메인 애플리케이션"""
    
    # 헤더
    st.markdown('''
    <div class="main-header">
        <h1>🎵 Quantum Circuit Synthesizer</h1>
    </div>
    ''', unsafe_allow_html=True)
    st.markdown("**IBM Qiskit을 활용한 교육용 양자 회로 음악 변환기**")
    st.markdown("---")
    
    # 신디사이저 초기화
    if 'synthesizer' not in st.session_state:
        st.session_state.synthesizer = initialize_synthesizer()
        st.session_state.last_audio = None
        st.session_state.synthesis_count = 0
    
    synth = st.session_state.synthesizer
    
    # 사이드바 - 설정 및 제어
    with st.sidebar:
        st.markdown('<h2 class="section-header">⚙️ 제어판</h2>', unsafe_allow_html=True)
        
        # 회로 초기화
        if st.button("🔄 회로 초기화 → |000⟩", use_container_width=True):
            synth.reset_circuit()
            st.session_state.last_audio = None
            st.session_state.synthesis_count = 0
            st.rerun()
        
        st.markdown("---")
        
        # 데모 회로 로드
        st.markdown("### 📚 데모 회로")
        demo_options = {
            "superposition": "중첩 상태",
            "mixed_states": "혼합 상태", 
            "entanglement": "얽힘 상태"
        }
        
        selected_demo = st.selectbox(
            "데모 선택:",
            options=list(demo_options.keys()),
            format_func=lambda x: demo_options[x]
        )
        
        if st.button("📥 데모 로드", use_container_width=True):
            result = synth.load_demo_circuit(selected_demo)
            if result['success']:
                st.session_state.synthesis_count += 1
                st.success(f"데모 '{demo_options[selected_demo]}' 로드됨!")
                st.rerun()
            else:
                st.error(f"데모 로드 실패: {result['error']}")
        
        st.markdown("---")
        
        # 설정
        st.markdown("### ⚙️ 오디오 설정")
        
        # 마스터 볼륨
        master_volume = st.slider(
            "마스터 볼륨",
            min_value=0.0,
            max_value=1.0,
            value=synth.config.master_volume,
            step=0.1
        )
        synth.config.master_volume = master_volume
        
        # 지속 시간
        duration = st.slider(
            "음표 지속 시간 (초)",
            min_value=0.5,
            max_value=5.0,
            value=synth.config.default_duration,
            step=0.5
        )
        synth.config.default_duration = duration
        
        # 측정 횟수
        shots = st.selectbox(
            "측정 횟수",
            options=[256, 512, 1024, 2048, 4096],
            index=2
        )
        synth.config.measurement_shots = shots
    
    # 메인 3컬럼 레이아웃
    col1, col2, col3 = st.columns([1, 1, 1])
    
    # 왼쪽 컬럼: 양자 게이트 제어
    with col1:
        st.markdown('<h2 class="section-header">🎛️ 양자 게이트 제어</h2>', 
                   unsafe_allow_html=True)
        
        # 초기 상태 표시 및 초기화
        st.markdown("### 🔄 회로 상태")
        
        # 현재 상태 확인
        viz_data = synth.get_circuit_visualization_data()
        current_probs = viz_data['qubit_probabilities']
        is_initial_state = all(prob == 0.0 for prob in current_probs.values())
        
        if is_initial_state:
            st.success("✅ 초기 상태: 모든 큐빗이 |0⟩ 상태")
            st.markdown("**현재 상태**: |000⟩ (무음)")
        else:
            st.info("🔄 게이트가 적용된 상태")
            prob_text = " ".join([f"Q{i}:{prob:.1%}" for i, prob in current_probs.items()])
            st.markdown(f"**확률**: {prob_text}")
        
        # 초기 상태 재생 버튼만 유지
        if st.button("🎵 초기 상태 재생", key="initial_play", use_container_width=True, disabled=not is_initial_state):
            if is_initial_state:
                # 초기 상태는 무음이므로 짧은 무음 생성
                st.info("초기 상태는 모든 큐빗이 |0⟩이므로 무음입니다.")
        
        st.markdown("---")
        
        # 큐빗 정보 표시
        st.markdown("### 큐빗 → 악기 매핑")
        qubit_info = [
            ("Qubit 0", "Bass Line", "220Hz (A3)", "#FF6B6B"),
            ("Qubit 1", "Melody", "330Hz (E4)", "#4ECDC4"),
            ("Qubit 2", "Harmony", "440Hz (A4)", "#45B7D1")
        ]
        
        for qubit, instrument, freq, color in qubit_info:
            st.markdown(f"""
            <div class="qubit-info" style="border-left-color: {color};">
                <strong>{qubit}</strong>: {instrument}<br>
                <small>{freq}</small>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # 하다마드 게이트
        st.markdown("### 🌊 하다마드 게이트 (중첩)")
        st.markdown("*효과: 2개 주파수 화음*")
        
        h_col1, h_col2, h_col3 = st.columns(3)
        with h_col1:
            if st.button("H → Q0", key="h0", use_container_width=True):
                result = synth.add_hadamard_gate(0)
                if result['success']:
                    st.session_state.synthesis_count += 1
                    st.rerun()
        
        with h_col2:
            if st.button("H → Q1", key="h1", use_container_width=True):
                result = synth.add_hadamard_gate(1)
                if result['success']:
                    st.session_state.synthesis_count += 1
                    st.rerun()
        
        with h_col3:
            if st.button("H → Q2", key="h2", use_container_width=True):
                result = synth.add_hadamard_gate(2)
                if result['success']:
                    st.session_state.synthesis_count += 1
                    st.rerun()
        
        # Pauli-X 게이트
        st.markdown("### ⚡ Pauli-X 게이트 (비트 플립)")
        st.markdown("*효과: ON/OFF 토글 + 부스트*")
        
        x_col1, x_col2, x_col3 = st.columns(3)
        with x_col1:
            if st.button("X → Q0", key="x0", use_container_width=True):
                result = synth.add_pauli_x_gate(0)
                if result['success']:
                    st.session_state.synthesis_count += 1
                    st.rerun()
        
        with x_col2:
            if st.button("X → Q1", key="x1", use_container_width=True):
                result = synth.add_pauli_x_gate(1)
                if result['success']:
                    st.session_state.synthesis_count += 1
                    st.rerun()
        
        with x_col3:
            if st.button("X → Q2", key="x2", use_container_width=True):
                result = synth.add_pauli_x_gate(2)
                if result['success']:
                    st.session_state.synthesis_count += 1
                    st.rerun()
        
        # CNOT 게이트
        st.markdown("### 🔗 CNOT 게이트 (얽힘)")
        st.markdown("*효과: 동기화된 하모니*")
        
        cnot_options = [
            ("Q0 → Q1", 0, 1),
            ("Q0 → Q2", 0, 2),
            ("Q1 → Q0", 1, 0),
            ("Q1 → Q2", 1, 2),
            ("Q2 → Q0", 2, 0),
            ("Q2 → Q1", 2, 1)
        ]
        
        cnot_col1, cnot_col2 = st.columns(2)
        for i, (label, control, target) in enumerate(cnot_options):
            col = cnot_col1 if i % 2 == 0 else cnot_col2
            with col:
                if st.button(label, key=f"cnot_{control}_{target}", use_container_width=True):
                    result = synth.add_cnot_gate(control, target)
                    if result['success']:
                        st.session_state.synthesis_count += 1
                        st.rerun()
    
    # 가운데 컬럼: 시각화
    with col2:
        st.markdown('<h2 class="section-header">📊 양자 상태 시각화</h2>', 
                   unsafe_allow_html=True)
        
        # 현재 상태 가져오기
        viz_data = synth.get_circuit_visualization_data()
        
        # 큐빗 확률 차트
        current_probs = viz_data['qubit_probabilities']
        is_initial_state = all(prob == 0.0 for prob in current_probs.values())
        
        if is_initial_state:
            # 초기 상태 전용 차트
            st.markdown("### 📊 초기 상태 확률")
            st.info("🔵 모든 큐빗이 |0⟩ 상태 (확률 100%)")
            
            # 초기 상태 시각화
            initial_chart = create_probability_chart({0: 0.0, 1: 0.0, 2: 0.0})
            st.plotly_chart(initial_chart, use_container_width=True)
            
            st.markdown("""
            **초기 상태 설명:**
            - 모든 큐빗이 |0⟩ 상태로 확정됨
            - |1⟩ 상태 확률은 0%
            - 측정하면 항상 '000' 결과
            - 음악적으로는 무음 상태
            """)
        else:
            st.markdown("### 📊 큐빗 |1⟩ 상태 확률")
            prob_chart = create_probability_chart(current_probs)
            st.plotly_chart(prob_chart, use_container_width=True)
            
            # 상태 해석
            total_prob = sum(current_probs.values())
            if total_prob > 0:
                st.markdown("**상태 해석:**")
                for qubit_id, prob in current_probs.items():
                    if prob > 0.1:  # 10% 이상인 경우만 표시
                        st.markdown(f"- Q{qubit_id}: {prob:.1%} 확률로 |1⟩ 상태")
                    elif prob > 0:
                        st.markdown(f"- Q{qubit_id}: {prob:.1%} 확률로 |1⟩ 상태 (약함)")
                    else:
                        st.markdown(f"- Q{qubit_id}: |0⟩ 상태 (확정)")
            else:
                st.warning("모든 큐빗이 |0⟩ 상태입니다.")
        
        # 회로 정보
        st.markdown("### 🔧 회로 정보")
        circuit_info = viz_data['circuit_info']
        
        info_col1, info_col2 = st.columns(2)
        with info_col1:
            st.metric("회로 깊이", circuit_info['circuit_depth'])
            st.metric("게이트 수", circuit_info['gate_count'])
        
        with info_col2:
            st.metric("큐빗 수", circuit_info['num_qubits'])
            st.metric("합성 횟수", st.session_state.synthesis_count)
        
        # 회로 다이어그램
        st.markdown("### 📋 회로 다이어그램")
        
        if viz_data['gate_sequence']:
            # 게이트가 적용된 회로
            # 시각적 다이어그램 시도
            img_base64, text_diagram = create_circuit_diagram_visual(
                synth.quantum_engine.circuit, 
                viz_data['gate_sequence']
            )
            
            if img_base64:
                # 시각적 다이어그램 표시
                st.markdown(
                    f'<img src="data:image/png;base64,{img_base64}" style="width:100%; max-width:600px;">',
                    unsafe_allow_html=True
                )
                
                # 접을 수 있는 텍스트 다이어그램
                with st.expander("📝 텍스트 다이어그램 보기"):
                    st.code(text_diagram, language=None)
            else:
                # 시각적 다이어그램 실패 시 텍스트만 표시
                st.code(text_diagram, language=None)
        else:
            # 초기 상태 (게이트 없음)
            st.info("🔵 초기 상태: 게이트가 적용되지 않은 빈 회로")
            
            initial_diagram = """
🔬 초기 양자 회로 상태
============================================================

q_0: ─────
          
q_1: ─────
          
q_2: ─────
          
c: 3/═════

📋 회로 정보:
- 게이트 수: 0
- 회로 깊이: 0
- 상태: |000⟩ (모든 큐빗이 |0⟩)
- 음향: 무음 (Silent)

💡 게이트를 적용하여 양자 상태를 변경하고 음악을 생성해보세요!
            """
            st.code(initial_diagram, language=None)
    
    # 오른쪽 컬럼: 오디오 출력
    with col3:
        st.markdown('<h2 class="section-header">🎵 오디오 출력</h2>', 
                   unsafe_allow_html=True)
        
        # 오디오 생성 및 재생
        if st.session_state.synthesis_count > 0:
            try:
                # 오디오 생성
                with st.spinner("오디오 생성 중..."):
                    mixed_audio = synth.get_mixed_audio()
                    audio_base64 = synth.get_audio_base64()
                    st.session_state.last_audio = audio_base64
                
                # 오디오 플레이어
                st.markdown("### 🎧 재생")
                audio_html = create_audio_player(audio_base64)
                st.markdown(audio_html, unsafe_allow_html=True)
                
                # 다운로드 버튼
                wav_bytes = synth.audio_generator.to_wav_bytes(mixed_audio)
                st.download_button(
                    label="💾 WAV 파일 다운로드",
                    data=wav_bytes,
                    file_name=f"quantum_synth_{int(time.time())}.wav",
                    mime="audio/wav",
                    use_container_width=True
                )
                
            except Exception as e:
                st.error(f"오디오 생성 오류: {str(e)}")
        
        else:
            st.info("게이트를 적용하여 음악을 생성하세요!")
        
        # 주파수 스펙트럼
        st.markdown("### 📈 주파수 스펙트럼")
        track_info = synth.get_track_info()
        
        if track_info:
            freq_chart = create_frequency_spectrum(track_info)
            st.plotly_chart(freq_chart, use_container_width=True)
            
            # 트랙 정보 테이블
            st.markdown("### 📋 활성 트랙")
            track_df = pd.DataFrame(track_info)
            if not track_df.empty:
                display_df = track_df[['qubit_id', 'frequency', 'probability', 'amplitude', 'gate_type']].copy()
                display_df.columns = ['큐빗', '주파수(Hz)', '확률', '진폭', '게이트']
                display_df['주파수(Hz)'] = display_df['주파수(Hz)'].round(1)
                display_df['확률'] = display_df['확률'].round(3)
                display_df['진폭'] = display_df['진폭'].round(3)
                st.dataframe(display_df, use_container_width=True)
        
        else:
            st.info("활성 트랙이 없습니다.")
    
    # 하단 정보
    st.markdown("---")
    st.markdown("### 📖 사용법")
    
    usage_col1, usage_col2, usage_col3 = st.columns(3)
    
    with usage_col1:
        st.markdown("""
        **🌊 하다마드 게이트**
        - 큐빗을 중첩 상태로 만듦
        - 2개 주파수 화음 효과
        - 확률적 음량 변화
        """)
    
    with usage_col2:
        st.markdown("""
        **⚡ Pauli-X 게이트**
        - 큐빗 상태 반전 (0↔1)
        - ON/OFF 토글 효과
        - 부스트된 음색
        """)
    
    with usage_col3:
        st.markdown("""
        **🔗 CNOT 게이트**
        - 두 큐빗 얽힘 생성
        - 동기화된 하모니
        - 비트 주파수 효과
        """)
    
    # 푸터
    st.markdown("---")
    st.markdown(
        "<div style='text-align: center; color: #666;'>"
        "🎵 Quantum Circuit Synthesizer v1.0 | "
        "Built with IBM Qiskit & Streamlit | "
        f"Session ID: {id(st.session_state) % 10000}"
        "</div>", 
        unsafe_allow_html=True
    )


if __name__ == "__main__":
    main()
