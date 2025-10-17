"""
프로젝트 기본 설정
"""

class ProjectConfig:
    """청담동 근린생활시설 프로젝트 설정"""
    
    # 프로젝트 기본 정보
    PROJECT_NAME = "청담동 근린생활시설 신축공사"
    LOCATION = "서울특별시 강남구 청담동 2-2"
    USE = "근린생활시설"
    
    # 규모
    GFA = 883.5  # 연면적 (㎡)
    GFA_PYEONG = 267.23  # 평
    
    # 예산
    TOTAL_BUDGET = 2_030_000_000  # 20.3억 원
    
    # 공기
    TOTAL_DURATION = 360  # 일 (12개월)
    
    # 단계별 기간 (일)
    PHASE_DURATIONS = {
        '설계': 90,      # Day 1-90
        '입찰': 20,      # Day 91-110
        '시공': 300,     # Day 111-410
        '준공': 20       # Day 411-430
    }
    
    # 금융 정보
    PF_RATIO = 0.7  # PF 대출 비율 (70%)
    BASE_INTEREST_RATE = 0.055  # 기본 연 5.5%
    
    # 간접비
    DAILY_INDIRECT_COST_RATIO = 0.001  # 일 0.1%
    
    # 지연별 금리 인상 (basis point)
    DELAY_RATE_INCREASE = {
        0: 0,      # 1개월 이하
        1: 0,      # 1개월 이하
        2: 20,     # 1~3개월
        3: 20,     # 1~3개월
        4: 50,     # 3~6개월
        5: 50,     # 3~6개월
        6: 50,     # 3~6개월
        7: 100,    # 6개월 초과
    }
    
    @classmethod
    def get_phase_start_end(cls, phase_name):
        """단계별 시작/종료 일자 반환"""
        phases = list(cls.PHASE_DURATIONS.keys())
        
        if phase_name not in phases:
            return None, None
        
        start_day = 1
        for phase in phases:
            if phase == phase_name:
                end_day = start_day + cls.PHASE_DURATIONS[phase] - 1
                return start_day, end_day
            start_day += cls.PHASE_DURATIONS[phase]
        
        return None, None
    
    @classmethod
    def get_phase_by_day(cls, day):
        """현재 일자에 해당하는 단계 반환"""
        current_day = 1
        
        for phase, duration in cls.PHASE_DURATIONS.items():
            if current_day <= day <= current_day + duration - 1:
                return phase
            current_day += duration
        
        return '준공'  # 기본값