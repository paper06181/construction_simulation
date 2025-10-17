# BIM 건설 시뮬레이션 가이드

## 실행 방법

### 기본 실행
```bash
python main.py --scenario compare
```

### BIM OFF만 실행
```bash
python main.py --scenario off
```

### BIM ON만 실행
```bash
python main.py --scenario on --quality good
```

### 프로젝트 템플릿 선택
```bash
python main.py --template apartment
python main.py --template office
python main.py --template commercial
```

### BIM 품질 수동 입력
```bash
python main.py --quality custom --wd 7.81 --cd 46.41 --af 0.8 --pl 0.7
```

WD (Warning Density): 0 이상, 낮을수록 좋음
CD (Clash Density): 0 이상, 낮을수록 좋음
AF (Attribute Fill): 0.0~1.0, 높을수록 좋음
PL (Phase Link): 0.0~1.0, 높을수록 좋음

## 출력 파일

시뮬레이션 완료 후 output 폴더에 자동 저장됩니다.

### 비교 결과
output/results/comparison_result_YYYYMMDD_HHMMSS.txt
- BIM OFF vs ON 비교
- 공기 단축, 비용 절감, 탐지율 향상
- ROI 계산

### 시뮬레이션 로그
output/logs/simulation_log_BIM_OFF_YYYYMMDD_HHMMSS.txt
output/logs/simulation_log_BIM_ON_YYYYMMDD_HHMMSS.txt
- 발생 이슈별 상세 내역
- 영향 분석 (지연, 비용, 탐지 여부)
- 협상 결과
- 회의 내용

### 회의록
output/meetings/meetings_BIM_OFF_YYYYMMDD_HHMMSS.txt
output/meetings/meetings_BIM_ON_YYYYMMDD_HHMMSS.txt
- 시뮬레이션당 1개 통합 파일
- 이슈별 초기 논의 + 의사결정 회의
- 협상 과정 (에이전트별 입장, 영향력)
- 협상 결과 (합의 지연, 합의 비용)

### 그래프
output/comparison_bars.png - 주요 메트릭스 비교
output/timeline_comparison.png - 공사 기간 타임라인
output/issue_breakdown.png - 이슈 탐지율 분석
output/roi_analysis.png - ROI 분석

## 핵심 기능

### 1. CPM 기반 지연 계산
이슈 카드에 work_type과 float_days 설정
- 구조: Float 0일 (크리티컬 패스)
- 설비/전기: Float 7일
- 마감: Float 14일

여러 이슈 발생 시 CPM 방식으로 총 지연 계산
- 같은 work_type = 순차 진행
- Float 범위 내 지연 = 흡수
- 크리티컬 패스 = 가장 긴 의존성 체인

### 2. 이슈별 발생 확률
각 이슈마다 occurrence_rate 설정 (일별 발생 확률)
- RFI 폭증: 2.0% (매우 흔함)
- 설비 간섭: 1.5% (흔함)
- 하도급 부도: 0.2% (매우 드묾)

매일 체크하여 현실적인 발생 패턴 구현

### 3. 회의 기반 협상 시스템
에이전트들이 이슈 카드 범위 내에서 협상하여 최종 지연/비용 결정

에이전트별 선호도 (0~100% 위치):
- 건축주: 25% (빡빡하게)
- 설계사: 40%
- 감리사: 50% (중립)
- 금융사: 60%
- 시공사: 75% (여유롭게)

에이전트별 영향력:
- 건축주: 40% (최종 의사결정권자)
- 시공사: 25%
- 감리사: 20%
- 설계사: 10%
- 금융사: 5%

프로젝트 특성 반영:
- BIM 조기 탐지 시: 건축주 영향력 45%로 증가
- 아파트: 건축주 영향력 50% (공기 민감)
- 오피스: 감리사 영향력 25% (품질 중시)
- 주택: 건축주 영향력 55% (직접 관여)
- 공사 막바지 (80% 이상): 압박 강화

협상 결과는 회의록에 상세 기록:
```
[협상 과정]
  건축주 입장: 20% 위치 선호 (빡빡), 영향력 45%
  시공사 입장: 75% 위치 선호 (여유롭게), 영향력 22%
  감리사 입장: 50% 위치 선호 (중립), 영향력 20%
  설계사 입장: 40% 위치 선호, 영향력 10%
  금융사 입장: 50% 위치 선호, 영향력 5%

[협상 결과] 건축주 주도로 빡빡하게 합의
  최종 협상 위치: 42%
  합의 지연: 4.3주 (범위: 3~6주)
  합의 비용: 1.3% (범위: 1.0~1.8%)
```

### 4. BIM 품질 커스터마이징
프리셋 또는 수동 입력 가능
- excellent: WD 0.2, CD 0.1, AF 0.95, PL 0.98
- good: WD 0.5, CD 0.2, AF 0.85, PL 0.90
- average: WD 0.8, CD 0.6, AF 0.70, PL 0.75
- poor: WD 1.0, CD 0.9, AF 0.50, PL 0.60
- custom: 직접 입력

### 5. 프로젝트 템플릿
6가지 프로젝트 템플릿 제공
- cheongdam: 청담동 근린생활시설 (30억, 365일)


## 코드 구조

### models/
project.py - 프로젝트 모델 (예산, 기간, 메트릭스)
bim_quality.py - BIM 품질 계산
financial.py - 금융 비용 계산

### agents/
5개 에이전트 (건축주, 설계사, 시공사, 감리사, 금융사)
LLM 기반 대화 생성

### simulation/
simulation_engine.py - 메인 시뮬레이션 로직
issue_manager.py - 이슈 발생 관리
impact_calculator.py - 영향 계산 (협상 시스템 사용)
meeting_coordinator.py - 회의 진행 및 저장
negotiation_system.py - 협상 시스템
delay_calculator.py - CPM 기반 지연 계산

### config/
issue_cards.json - 27개 이슈 정의
project_templates.py - 프로젝트 템플릿
work_dependencies.py - CPM 의존성 및 Float

### reports/
report_generator.py - 텍스트 리포트
graph_visualizer.py - 그래프 생성
visualizer.py - 텍스트 차트

## 주요 개선 사항

1. CPM 기반 다중 이슈 지연 계산
   - Float (여유시간) 개념 적용
   - 크리티컬 패스 자동 계산
   - 5개 이상 이슈 발생 시 동시다발 오버헤드

2. 이슈별 차별화된 발생 확률
   - 0.2% ~ 2.0% 범위
   - 실제 건설 현장 통계 기반

3. 회의 기반 협상 시스템
   - 에이전트들이 실제로 값을 결정
   - 프로젝트 특성 반영
   - BIM 탐지 효과 반영

4. BIM 품질 수동 입력
   - WD, CD: 상한 없음 (실제 측정값 입력 가능)
   - AF, PL: 0.0~1.0

5. 통합 저장 시스템
   - 시뮬레이션 로그
   - 회의록 (시뮬레이션당 1개 파일)
   - 비교 결과
   - 그래프 4종

