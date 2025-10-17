# BIM 건설 시뮬레이션

건설 프로젝트에서 BIM 적용 여부에 따른 차이를 시뮬레이션하는 프로그램입니다.

## 설치

```bash
pip install -r requirements.txt
```

## 실행 방법

기본 실행 (BIM OFF vs ON 비교):
```bash
python main.py --scenario compare
```

BIM OFF만 실행:
```bash
python main.py --scenario off
```

BIM ON만 실행:
```bash
python main.py --scenario on --quality good
```

프로젝트 템플릿 선택:
```bash
python main.py --template apartment
python main.py --template office
python main.py --template commercial
```

BIM 품질 수동 입력:
```bash
python main.py --quality custom --wd 7.81 --cd 46.41 --af 0.8 --pl 0.7
```

WD (Warning Density): 0 이상, 낮을수록 좋음
CD (Clash Density): 0 이상, 낮을수록 좋음
AF (Attribute Fill): 0.0~1.0, 높을수록 좋음
PL (Phase Link): 0.0~1.0, 높을수록 좋음

## 출력 결과

시뮬레이션이 끝나면 output 폴더에 자동으로 저장됩니다.

비교 결과: output/results/comparison_result_YYYYMMDD_HHMMSS.txt
시뮬레이션 로그: output/logs/simulation_log_BIM_OFF_YYYYMMDD_HHMMSS.txt
회의록: output/meetings/meetings_BIM_OFF_YYYYMMDD_HHMMSS.txt
그래프: output/*.png (4종)

## 핵심 기능

1. CPM 기반 지연 계산
   여러 이슈가 동시에 발생해도 크리티컬 패스와 Float 개념으로 실제 지연을 계산합니다.

2. 이슈별 발생 확률
   각 이슈마다 다른 발생 확률을 가지고 있어서 현실적인 패턴을 만듭니다.

3. 회의 기반 협상 시스템
   에이전트들이 회의를 통해 실제로 지연과 비용을 결정합니다.
   건축주, 설계사, 시공사, 감리사, 금융사가 각자 입장을 가지고 협상합니다.

4. BIM 품질 커스터마이징
   프리셋(excellent/good/average/poor) 또는 직접 입력 가능합니다.

5. 프로젝트 템플릿
   6가지 프로젝트 템플릿을 제공합니다.

자세한 내용은 docs/GUIDE.md를 확인하세요.
