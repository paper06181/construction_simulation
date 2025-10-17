"""
이슈 카드에 CPM 관련 필드 추가 스크립트
work_type (공종)과 float_days (여유시간) 추가
"""

import json
from pathlib import Path

# 이슈명 → 공종 매핑 (실무 기반)
WORK_TYPE_MAPPING = {
    # 구조 공종 (크리티컬 패스)
    "I-01": ("구조", 0),  # 설비-구조 간섭 → 구조 재작업
    "I-02": ("구조", 0),  # 기둥 위치 불일치 → 구조
    "I-07": ("구조", 0),  # 철골 제작 오류 → 구조
    "I-12": ("구조", 0),  # 층간 높이 오차 → 구조
    "I-15": ("토목", 0),  # 지하 매설물 → 토목 (크리티컬)
    "I-16": ("구조", 0),  # 콘크리트 양생 불량 → 구조

    # 설비 공종
    "I-09": ("설비", 7),   # 배관 간섭 → 설비 (1주 여유)
    "I-21": ("설비", 0),   # 설비 하도급사 부도 → 크리티컬

    # 전기 공종
    "I-20": ("전기", 7),   # 소방 설비 → 전기/설비 (1주 여유)

    # 마감 공종
    "I-05": ("마감", 14),  # 천장 높이 불일치 → 마감 (2주 여유)
    "I-08": ("마감", 7),   # 벽체 착오 시공 → 마감 (1주 여유)
    "I-13": ("마감", 14),  # 타일 수량 부족 → 마감 (2주 여유)
    "I-25": ("마감", 14),  # 타일 품질 불량 → 마감 (2주 여유)
    "I-26": ("마감", 7),   # 방수 재시공 → 마감 (1주 여유)
    "I-27": ("마감", 14),  # 준공 검사 → 마감 (2주 여유)

    # 자재 (독립적, 여유 있음)
    "I-22": ("자재", 14),  # 수입 자재 지연 (2주 여유)
    "I-23": ("자재", 0),   # 철근 가격 급등 (지연 없음)
    "I-24": ("자재", 7),   # 맞춤 제작 지연 (1주 여유)

    # 설계 (초기 단계, 크리티컬)
    "I-03": ("설계", 0),   # 물량 산출 오류
    "I-04": ("설계", 0),   # 설계 변경 이력
    "I-06": ("설계", 0),   # RFI 폭증

    # 발주/계약 (크리티컬)
    "I-18": ("계약", 0),   # 설계 변경
    "I-19": ("계약", 0),   # 계약 금액 오류

    # 기타 시공 (일반)
    "I-10": ("시공관리", 7),   # 양중 계획 (1주 여유)
    "I-11": ("토목", 0),       # 우기 장마 → 토목 크리티컬
    "I-14": ("시공관리", 0),   # 인력 수급 → 크리티컬
    "I-17": ("시공관리", 7),   # 타워크레인 고장 (1주 여유)
}

def determine_work_type_and_float(issue):
    """
    이슈의 특성에 따라 공종과 Float 결정
    """
    issue_id = issue['id']

    # 미리 정의된 매핑이 있으면 사용
    if issue_id in WORK_TYPE_MAPPING:
        return WORK_TYPE_MAPPING[issue_id]

    # 없으면 category와 description으로 추론
    category = issue['category']
    description = issue['description']
    severity = issue['severity']

    # 카테고리별 기본 매핑
    if category == "설계":
        # 설계 이슈는 보통 크리티컬
        return ("설계", 0)

    elif category == "시공":
        # description으로 세분화
        if "철골" in description or "철근" in description or "콘크리트" in description:
            return ("구조", 0)  # 구조 관련은 크리티컬
        elif "설비" in description or "배관" in description or "HVAC" in description:
            return ("설비", 7)   # 설비는 1주 여유
        elif "전기" in description or "소방" in description:
            return ("전기", 7)
        elif "마감" in description or "타일" in description or "도장" in description:
            return ("마감", 14)  # 마감은 2주 여유
        elif "토공" in description or "터파기" in description:
            return ("토목", 0)
        else:
            return ("시공관리", 7)  # 기타 시공은 1주 여유

    elif category == "발주":
        return ("계약", 0)  # 발주 이슈는 크리티컬

    elif category == "자재":
        # 심각도로 판단
        if severity == "S3":
            return ("자재", 7)   # 심각한 자재 문제는 1주 여유
        else:
            return ("자재", 14)  # 일반 자재는 2주 여유

    elif category == "감리":
        return ("마감", 7)  # 감리 지적은 마감 단계

    else:
        # 기본값
        return ("시공관리", 7)

def add_cpm_fields():
    """이슈 카드에 CPM 필드 추가"""

    issue_file = Path("data/issue_cards.json")

    # 파일 읽기
    with open(issue_file, 'r', encoding='utf-8') as f:
        issues = json.load(f)

    print(f"총 {len(issues)}개 이슈 처리 중...")

    # 각 이슈에 work_type과 float_days 추가
    for issue in issues:
        work_type, float_days = determine_work_type_and_float(issue)

        issue['work_type'] = work_type
        issue['float_days'] = float_days

        print(f"  {issue['id']} {issue['name']:<30s} → {work_type:10s} (Float: {float_days}일)")

    # 파일 저장
    with open(issue_file, 'w', encoding='utf-8') as f:
        json.dump(issues, f, ensure_ascii=False, indent=2)

    print(f"\n✓ {issue_file} 업데이트 완료!")

    # 통계 출력
    work_types = {}
    for issue in issues:
        wt = issue['work_type']
        work_types[wt] = work_types.get(wt, 0) + 1

    print("\n=== 공종별 이슈 개수 ===")
    for wt, count in sorted(work_types.items()):
        print(f"  {wt:10s}: {count}개")

if __name__ == "__main__":
    add_cpm_fields()
