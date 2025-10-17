"""
공종 간 의존성 정의 (실무 기반 CPM)
"""

# 공종 간 의존성 그래프
# Key: 공종, Value: 선행 공종 리스트
WORK_DEPENDENCIES = {
    '설계': [],                    # 설계는 선행 없음 (최초)
    '토목': ['설계'],               # 토목은 설계 후
    '구조': ['토목', '설계'],       # 구조는 토목, 설계 후
    '설비': ['구조'],               # 설비는 구조 완료 후
    '전기': ['구조'],               # 전기는 구조 완료 후 (설비와 병렬 가능)
    '마감': ['설비', '전기'],       # 마감은 설비와 전기 완료 후
    '시공관리': [],                 # 시공관리는 독립적
    '계약': [],                     # 계약은 독립적
    '자재': [],                     # 자재는 독립적 (병렬 가능)
}

# 공종별 기본 Float 값 (일 단위)
# Float = 해당 공종이 지연될 수 있는 여유 시간
# Float = 0 이면 크리티컬 패스
DEFAULT_FLOAT_DAYS = {
    '설계': 0,          # 설계는 크리티컬
    '토목': 0,          # 토목은 크리티컬
    '구조': 0,          # 구조는 크리티컬
    '설비': 7,          # 설비는 1주 여유
    '전기': 7,          # 전기는 1주 여유
    '마감': 14,         # 마감은 2주 여유
    '시공관리': 7,      # 시공관리는 1주 여유
    '계약': 0,          # 계약은 크리티컬
    '자재': 14,         # 자재는 2주 여유 (선주문 가능)
}

# 공종별 병렬 처리 가능 여부
# 같은 그룹 내에서는 병렬 처리 가능
PARALLEL_GROUPS = [
    ['설비', '전기'],        # 설비와 전기는 병렬 처리 가능
    ['자재'],                # 자재는 언제든지 병렬 처리 가능
    ['시공관리'],            # 시공관리는 언제든지 병렬 처리 가능
]

def can_run_in_parallel(work_type1, work_type2):
    """
    두 공종이 병렬 처리 가능한지 확인
    """
    for group in PARALLEL_GROUPS:
        if work_type1 in group and work_type2 in group:
            return True
    return False

def get_dependencies(work_type):
    """특정 공종의 선행 공종 리스트 반환"""
    return WORK_DEPENDENCIES.get(work_type, [])

def get_float_days(work_type):
    """특정 공종의 Float 값 반환"""
    return DEFAULT_FLOAT_DAYS.get(work_type, 7)

def is_critical_path(work_type):
    """크리티컬 패스 공종인지 확인"""
    return get_float_days(work_type) == 0
