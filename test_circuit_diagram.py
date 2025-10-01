#!/usr/bin/env python3
"""
회로 다이어그램 시각화 테스트
"""

import matplotlib
matplotlib.use('Agg')  # GUI 없는 백엔드 사용
import matplotlib.pyplot as plt
from quantum_engine import QuantumSynthEngine
from io import BytesIO
import base64

def test_circuit_visualization():
    """회로 시각화 테스트"""
    print("=== 회로 다이어그램 시각화 테스트 ===")
    
    # 테스트 회로 생성
    engine = QuantumSynthEngine(3)
    
    # 게이트 추가
    engine.apply_hadamard(0)
    engine.apply_pauli_x(1)
    engine.apply_cnot(0, 2)
    
    print(f"회로 생성 완료:")
    print(f"- 게이트 수: {len(engine.circuit.data)}")
    print(f"- 회로 깊이: {engine.circuit.depth()}")
    
    # 텍스트 다이어그램
    print(f"\n텍스트 다이어그램:")
    print(engine.circuit)
    
    # matplotlib 시각화 테스트
    try:
        fig, ax = plt.subplots(figsize=(10, 6))
        engine.circuit.draw(output='mpl', ax=ax, style='iqp')
        ax.set_title('Test Quantum Circuit', fontsize=14, fontweight='bold')
        
        # 이미지 저장 테스트
        plt.savefig('test_circuit.png', dpi=120, bbox_inches='tight')
        plt.close(fig)
        
        print("✅ matplotlib 시각화 성공! (test_circuit.png 저장됨)")
        
    except Exception as e:
        print(f"❌ matplotlib 시각화 실패: {e}")
    
    # Base64 인코딩 테스트
    try:
        fig, ax = plt.subplots(figsize=(10, 6))
        engine.circuit.draw(output='mpl', ax=ax)
        
        buffer = BytesIO()
        plt.savefig(buffer, format='png', dpi=120, bbox_inches='tight')
        buffer.seek(0)
        
        img_base64 = base64.b64encode(buffer.getvalue()).decode()
        plt.close(fig)
        
        print(f"✅ Base64 인코딩 성공! (길이: {len(img_base64)} 문자)")
        
    except Exception as e:
        print(f"❌ Base64 인코딩 실패: {e}")

if __name__ == "__main__":
    test_circuit_visualization()
