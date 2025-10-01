first created file
# 🎵 Quantum Circuit Synthesizer

**IBM Qiskit을 활용한 교육용 양자 회로 음악 변환기**

양자 게이트(H, X, CNOT)의 측정 결과를 실시간으로 음악으로 변환하는 혁신적인 교육용 웹 애플리케이션입니다.

![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)
![Qiskit](https://img.shields.io/badge/Qiskit-0.44.0-purple.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-red.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)

## 📅 개발 일정

- **개발 시작**: 2025-10-01 12:55 KST
- **목표 완료**: 2025-10-01 15:55 KST (3시간 내)
- **현재 상태**: ✅ **완료** (모든 핵심 기능 구현됨)

## 🎯 프로젝트 개요

### 핵심 아이디어
양자 컴퓨팅의 추상적 개념을 직관적인 음악으로 변환하여, 학습자가 양자 상태와 게이트의 동작을 청각적으로 이해할 수 있도록 돕는 교육 도구입니다.

### 주요 특징
- **실시간 양자 시뮬레이션**: IBM Qiskit 기반 정확한 양자 계산
- **직관적 음악 변환**: 양자 상태 → 음악적 표현의 자연스러운 매핑
- **인터랙티브 웹 UI**: Streamlit 기반 사용자 친화적 인터페이스
- **교육적 시각화**: 실시간 확률 차트 및 주파수 스펙트럼

## 🔧 기술 스택

### 핵심 기술
- **양자 컴퓨팅**: [IBM Qiskit 0.44.0](https://qiskit.org/)
- **웹 프레임워크**: [Streamlit](https://streamlit.io/)
- **오디오 처리**: NumPy + SciPy
- **시각화**: [Plotly](https://plotly.com/)
- **패키지 관리**: [uv](https://github.com/astral-sh/uv)

### 의존성
```toml
qiskit==0.44.0
streamlit>=1.28.0
numpy>=1.24.0
scipy>=1.11.0
plotly>=5.15.0
matplotlib>=3.7.0
pandas>=2.0.0
```

## 🎼 음악 변환 규칙

### 양자 게이트 → 음악 효과 매핑

| 게이트 | 양자 효과 | 음악 효과 | 설명 |
|--------|-----------|-----------|------|
| **H (하다마드)** | 중첩 상태 생성 | 2개 주파수 화음 | 기본파 + 하모닉으로 중첩 표현 |
| **X (Pauli-X)** | 비트 플립 | ON/OFF 토글 + 부스트 | 완전한 상태 반전을 강한 음색으로 표현 |
| **CNOT** | 얽힘 상태 생성 | 동기화된 하모니 | 비트 주파수로 얽힘 효과 구현 |

### 큐빗 → 악기 매핑

| 큐빗 | 악기 역할 | 주파수 | 음표 |
|------|-----------|--------|------|
| **Qubit 0** | Bass Line | 220Hz | A3 |
| **Qubit 1** | Melody | 330Hz | E4 |
| **Qubit 2** | Harmony | 440Hz | A4 |

### 확률 → 음량 변환
- **측정 확률 ∝ 음량**: 높은 확률 = 큰 볼륨
- **임계값 처리**: 10% 미만 확률은 무음 처리
- **로그 스케일**: 작은 확률도 들릴 수 있도록 제곱근 변환

## 🚀 설치 및 실행

### 1. 환경 설정 (uv 사용)

```bash
# 저장소 클론
git clone https://github.com/your-username/qc-synth.git
cd qc-synth

# uv로 의존성 설치
uv sync

# 또는 pip 사용 시
pip install -r requirements.txt
```

### 2. 애플리케이션 실행

```bash
# uv 환경에서 실행
uv run streamlit run app.py

# 또는 직접 실행
streamlit run app.py
```

### 3. 웹 브라우저 접속
```
http://localhost:8501
```

## 📱 사용법

### 기본 워크플로우
1. **게이트 선택**: 왼쪽 패널에서 H, X, CNOT 게이트 중 선택
2. **큐빗 지정**: 게이트를 적용할 큐빗 선택
3. **음악 생성**: 자동으로 양자 상태가 음악으로 변환됨
4. **재생 및 분석**: 가운데/오른쪽 패널에서 시각화 및 오디오 재생

### 인터페이스 구성

#### 왼쪽 컬럼: 🎛️ 양자 게이트 제어
- 큐빗별 악기 매핑 정보
- H, X, CNOT 게이트 버튼
- 직관적인 게이트 적용 인터페이스

#### 가운데 컬럼: 📊 양자 상태 시각화  
- 실시간 큐빗 확률 차트
- 회로 깊이/게이트 수 메트릭
- 텍스트 기반 회로 다이어그램

#### 오른쪽 컬럼: 🎵 오디오 출력
- HTML5 오디오 플레이어
- WAV 파일 다운로드
- 주파수 스펙트럼 시각화
- 활성 트랙 정보 테이블

### 사이드바: ⚙️ 제어판
- 회로 초기화 버튼
- 데모 회로 로드 (중첩/혼합/얽힘 상태)
- 오디오 설정 (볼륨, 지속시간, 측정횟수)

## 🏗️ 프로젝트 구조

```
qc-synth/
├── app.py                 # Streamlit 웹 인터페이스
├── quantum_engine.py      # Qiskit 기반 양자 회로 엔진
├── audio_generator.py     # 오디오 생성 및 처리 모듈
├── quantum_synth.py       # 양자-음악 변환 통합 로직
├── pyproject.toml         # uv 프로젝트 설정
├── requirements.txt       # 의존성 목록
└── README.md             # 프로젝트 문서 (이 파일)
```

### 모듈별 역할

#### `quantum_engine.py`
- **QuantumSynthEngine**: Qiskit 기반 양자 회로 시뮬레이션
- H, X, CNOT 게이트 구현
- 상태벡터 및 측정 확률 계산
- 데모 회로 생성 기능

#### `audio_generator.py`  
- **AudioGenerator**: 사인파, 화음, WAV 파일 생성
- **QuantumAudioMapper**: 양자 상태 → 오디오 매핑
- ADSR 엔벨로프, 믹싱, Base64 인코딩

#### `quantum_synth.py`
- **QuantumCircuitSynthesizer**: 메인 통합 클래스
- 게이트 적용 및 오디오 합성 워크플로우
- 트랙 관리 및 히스토리 기록
- 설정 관리 (SynthConfig)

#### `app.py`
- Streamlit 기반 3컬럼 웹 인터페이스
- 실시간 시각화 (Plotly 차트)
- 오디오 플레이어 및 다운로드 기능
- 반응형 UI 및 사용자 경험 최적화

## 🎓 교육적 활용

### 학습 목표
1. **양자 중첩**: 하다마드 게이트로 생성되는 화음을 통해 중첩 개념 이해
2. **양자 얽힘**: CNOT 게이트의 동기화된 하모니로 얽힘 현상 체험
3. **측정 확률**: 음량 변화를 통한 확률적 측정 결과 직관적 이해
4. **게이트 조합**: 복잡한 양자 알고리즘의 음악적 패턴 탐구

### 교육 시나리오
- **기초 과정**: 단일 게이트 효과 체험
- **중급 과정**: 게이트 조합으로 복잡한 음악 패턴 생성
- **고급 과정**: 양자 알고리즘의 음악적 해석

## 🔬 기술적 세부사항

### 양자 시뮬레이션
- **시뮬레이터**: Qiskit AerSimulator (로컬 실행)
- **측정 방식**: 통계적 샘플링 (기본 1024 shots)
- **상태 표현**: 복소수 상태벡터 + 확률 분포

### 오디오 처리
- **샘플링 레이트**: 44.1kHz (CD 품질)
- **비트 깊이**: 16-bit
- **파형 생성**: 순수 사인파 기반
- **믹싱**: 가중 평균 + 정규화

### 성능 최적화
- **캐싱**: Streamlit @st.cache_resource로 초기화 최적화
- **비동기 처리**: 오디오 생성과 UI 업데이트 분리
- **메모리 관리**: 대용량 오디오 데이터 효율적 처리

## 🧪 테스트 및 검증

### 단위 테스트
각 모듈은 독립적인 테스트 코드를 포함합니다:

```bash
# 개별 모듈 테스트
python quantum_engine.py
python audio_generator.py  
python quantum_synth.py
```

### 통합 테스트
```bash
# 전체 애플리케이션 테스트
uv run streamlit run app.py
```

## 🚧 알려진 제한사항

1. **브라우저 호환성**: HTML5 오디오 지원 브라우저 필요
2. **실시간 성능**: 복잡한 회로에서 지연 발생 가능
3. **오디오 품질**: 웹 기반 재생으로 인한 품질 제한
4. **큐빗 수**: 현재 3큐빗으로 제한 (확장 가능)

## 🔮 향후 개발 계획

### Phase 2: 고급 기능
- [ ] 더 많은 양자 게이트 지원 (Y, Z, T, S 게이트)
- [ ] 다중 큐빗 시스템 (4+ 큐빗)
- [ ] 실제 양자 하드웨어 연동 (IBM Quantum Network)
- [ ] 고급 오디오 효과 (리버브, 딜레이, 필터)

### Phase 3: 교육 플랫폼
- [ ] 단계별 튜토리얼 시스템
- [ ] 양자 알고리즘 프리셋 (Grover, Shor 등)
- [ ] 학습 진도 추적 및 평가
- [ ] 다국어 지원

### Phase 4: 커뮤니티 기능
- [ ] 음악 작품 공유 플랫폼
- [ ] 협업 작곡 도구
- [ ] 양자 음악 콘테스트
- [ ] API 제공 (외부 연동)

## 🤝 기여하기

### 개발 환경 설정
```bash
# 개발 의존성 설치
uv sync --dev

# 코드 포맷팅
uv run black .

# 린팅
uv run flake8 .
```

### 기여 가이드라인
1. Fork 후 feature 브랜치 생성
2. 코드 변경 및 테스트 추가
3. Pull Request 제출
4. 코드 리뷰 및 머지

## 📄 라이선스

MIT License - 자세한 내용은 [LICENSE](LICENSE) 파일 참조

## 👥 개발팀

- **Lead Developer**: Quantum Synth Team
- **Quantum Computing**: IBM Qiskit Community
- **Audio Processing**: NumPy/SciPy Contributors  
- **Web Framework**: Streamlit Team

## 📞 연락처

- **이슈 리포트**: [GitHub Issues](https://github.com/your-username/qc-synth/issues)
- **기능 요청**: [GitHub Discussions](https://github.com/your-username/qc-synth/discussions)
- **이메일**: team@quantumsynth.dev

## 🙏 감사의 말

이 프로젝트는 다음 오픈소스 프로젝트들의 도움으로 완성되었습니다:

- [IBM Qiskit](https://qiskit.org/) - 양자 컴퓨팅 프레임워크
- [Streamlit](https://streamlit.io/) - 웹 애플리케이션 프레임워크  
- [NumPy](https://numpy.org/) & [SciPy](https://scipy.org/) - 과학 계산
- [Plotly](https://plotly.com/) - 인터랙티브 시각화

---

**🎵 양자 세계의 음악을 함께 탐험해보세요! 🎵**
