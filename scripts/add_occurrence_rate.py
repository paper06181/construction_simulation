"""
이슈별 발생 확률 추가 스크립트
실무 기반 발생 빈도 설정
"""

import json
from pathlib import Path

# 이슈별 발생 확률 매핑 (실무 기반)
# 값 범위: 0.0 ~ 1.0 (일별 발생 확률)
OCCURRENCE_RATES = {
    # 설계 이슈 (흔함 - 중간)
    "I-01": 0.015,  # 설비-구조 간섭 (1.5% / 일) - 흔함
    "I-02": 0.012,  # 도면 불일치 (1.2% / 일) - 흔함
    "I-03": 0.010,  # 물량 산출 오류 (1.0% / 일) - 중간
    "I-04": 0.008,  # 설계 변경 이력 (0.8% / 일) - 중간
    "I-05": 0.010,  # 도면 정보 불일치 (1.0% / 일) - 중간

    # 시공 이슈 (매우 흔함 - 중간)
    "I-06": 0.020,  # RFI 폭증 (2.0% / 일) - 매우 흔함
    "I-07": 0.005,  # 철골 제작 오류 (0.5% / 일) - 드묾
    "I-08": 0.015,  # 현장 착오 시공 (1.5% / 일) - 흔함
    "I-09": 0.008,  # 배관 간섭 (0.8% / 일) - 중간
    "I-10": 0.006,  # 양중 계획 부재 (0.6% / 일) - 중간
    "I-11": 0.003,  # 우기 장마 (0.3% / 일) - 드묾 (계절)
    "I-12": 0.004,  # 층간 오차 (0.4% / 일) - 드묾
    "I-13": 0.012,  # 자재 수량 오류 (1.2% / 일) - 흔함
    "I-14": 0.008,  # 인력 수급 차질 (0.8% / 일) - 중간
    "I-15": 0.002,  # 지하 매설물 (0.2% / 일) - 매우 드묾
    "I-16": 0.003,  # 콘크리트 양생 불량 (0.3% / 일) - 드묾 (계절)
    "I-17": 0.005,  # 타워크레인 고장 (0.5% / 일) - 드묾

    # 발주 이슈 (드묾)
    "I-18": 0.004,  # 발주자 설계 변경 (0.4% / 일) - 드묾
    "I-19": 0.003,  # 계약 금액 오류 (0.3% / 일) - 드묾
    "I-20": 0.006,  # 인허가 보완 (0.6% / 일) - 중간
    "I-21": 0.002,  # 하도급 부도 (0.2% / 일) - 매우 드묾

    # 자재 이슈 (중간)
    "I-22": 0.005,  # 수입 자재 지연 (0.5% / 일) - 드묾
    "I-23": 0.004,  # 철근 가격 급등 (0.4% / 일) - 드묾
    "I-24": 0.006,  # 맞춤 제작 지연 (0.6% / 일) - 중간
    "I-25": 0.008,  # 자재 품질 불량 (0.8% / 일) - 중간

    # 감리 이슈 (중간)
    "I-26": 0.010,  # 감리 지적 (1.0% / 일) - 중간
    "I-27": 0.012,  # 준공 검사 불합격 (1.2% / 일) - 중간
}

def calculate_daily_probability(issue_id, severity, category):
    """
    일별 발생 확률 계산

    매핑에 없으면 카테고리와 심각도로 추정
    """
    if issue_id in OCCURRENCE_RATES:
        return OCCURRENCE_RATES[issue_id]

    # 기본값 설정 (카테고리별)
    base_rates = {
        '설계': 0.010,      # 1.0% / 일
        '시공': 0.012,      # 1.2% / 일
        '발주': 0.004,      # 0.4% / 일
        '자재': 0.006,      # 0.6% / 일
        '감리': 0.010,      # 1.0% / 일
    }

    base_rate = base_rates.get(category, 0.008)

    # 심각도 배율
    severity_multiplier = {
        'S3': 0.8,   # 심각한 문제는 덜 자주
        'S2': 1.0,   # 보통
        'S1': 1.2,   # 작은 문제는 더 자주
    }

    return base_rate * severity_multiplier.get(severity, 1.0)

def add_occurrence_rates():
    """이슈 카드에 발생 확률 추가"""

    issue_file = Path("data/issue_cards.json")

    # 파일 읽기
    with open(issue_file, 'r', encoding='utf-8') as f:
        issues = json.load(f)

    print(f"총 {len(issues)}개 이슈에 발생 확률 추가 중...\n")

    # 통계
    stats = {
        '매우 흔함 (>1.5%)': [],
        '흔함 (1.0-1.5%)': [],
        '중간 (0.5-1.0%)': [],
        '드묾 (0.2-0.5%)': [],
        '매우 드묾 (<0.2%)': []
    }

    # 각 이슈에 occurrence_rate 추가
    for issue in issues:
        issue_id = issue['id']
        severity = issue['severity']
        category = issue['category']

        # 일별 발생 확률 계산
        daily_rate = calculate_daily_probability(issue_id, severity, category)

        # 저장
        issue['occurrence_rate'] = daily_rate

        # 통계 분류
        rate_pct = daily_rate * 100
        if rate_pct >= 1.5:
            stats['매우 흔함 (>1.5%)'].append((issue_id, issue['name'], rate_pct))
        elif rate_pct >= 1.0:
            stats['흔함 (1.0-1.5%)'].append((issue_id, issue['name'], rate_pct))
        elif rate_pct >= 0.5:
            stats['중간 (0.5-1.0%)'].append((issue_id, issue['name'], rate_pct))
        elif rate_pct >= 0.2:
            stats['드묾 (0.2-0.5%)'].append((issue_id, issue['name'], rate_pct))
        else:
            stats['매우 드묾 (<0.2%)'].append((issue_id, issue['name'], rate_pct))

        print(f"  {issue_id} {issue['name']:<35s} → {rate_pct:.2f}% / 일")

    # 파일 저장
    with open(issue_file, 'w', encoding='utf-8') as f:
        json.dump(issues, f, ensure_ascii=False, indent=2)

    print(f"\n업데이트 완료: {issue_file}")

    # 통계 출력
    print("\n=== 발생 빈도 통계 ===")
    for category, items in stats.items():
        if items:
            print(f"\n{category}: {len(items)}개")
            for issue_id, name, rate in items:
                print(f"  {issue_id}: {name} ({rate:.2f}%)")

if __name__ == "__main__":
    add_occurrence_rates()
