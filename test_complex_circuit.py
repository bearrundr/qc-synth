#!/usr/bin/env python3
"""
복잡한 회로 다이어그램 테스트
"""

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from quantum_engine import QuantumSynthEngine, create_demo_circuits

def test_complex_circuits():
    """복잡한 회로들의 다이어그램 테스트"""
    print("=== 복잡한 회로 다이어그램 테스트 ===")
    
    # 1. 수동으로 복잡한 회로 생성
    print("\n1. 복잡한 수동 회로:")
    engine = QuantumSynthEngine(3)
    
    # 여러 게이트 추가
    engine.apply_hadamard(0)
    engine.apply_hadamard(1)
    engine.apply_pauli_x(2)
    engine.apply_cnot(0, 1)
    engine.apply_cnot(1, 2)
    engine.apply_hadamard(0)
    
    print(f"게이트 수: {len(engine.circuit.data)}, 깊이: {engine.circuit.depth()}")
    
    # 텍스트 다이어그램
    print("\n텍스트 다이어그램:")
    print(engine.circuit.draw('text'))
    
    # 2. 데모 회로들 테스트
    print("\n" + "="*60)
    print("2. 데모 회로들:")
    
    demos = create_demo_circuits()
    
    for name, demo_engine in demos.items():
        print(f"\n--- {name.upper()} ---")
        print(f"게이트 수: {len(demo_engine.circuit.data)}, 깊이: {demo_engine.circuit.depth()}")
        
        # 텍스트 다이어그램
        print("텍스트 다이어그램:")
        print(demo_engine.circuit.draw('text'))
        
        # 다양한 형식 테스트
        try:
            print("\n압축 형식:")
            compressed = demo_engine.circuit.draw('text', vertical_compression='high')
            print(compressed)
        except Exception as e:
            print(f"압축 형식 오류: {e}")
    
    # 3. matplotlib 시각화 테스트
    print("\n" + "="*60)
    print("3. matplotlib 시각화 테스트:")
    
    for name, demo_engine in demos.items():
        try:
            fig, ax = plt.subplots(figsize=(12, 6))
            demo_engine.circuit.draw(output='mpl', ax=ax, style='iqp')
            ax.set_title(f'{name.title()} Circuit', fontsize=14, fontweight='bold')
            
            filename = f'demo_{name}_circuit.png'
            plt.savefig(filename, dpi=120, bbox_inches='tight')
            plt.close(fig)
            
            print(f"✅ {name} 시각화 성공! ({filename} 저장됨)")
            
        except Exception as e:
            print(f"❌ {name} 시각화 실패: {e}")

if __name__ == "__main__":
    test_complex_circuits()
