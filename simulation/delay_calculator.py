"""
실무 기반 CPM 지연 계산기
Multiple overlapping issues를 Critical Path Method로 처리
"""

from collections import defaultdict
from config.work_dependencies import WORK_DEPENDENCIES, get_float_days, can_run_in_parallel

class DelayCalculator:
    """CPM 기반 다중 이슈 지연 계산기"""

    def __init__(self):
        self.active_issues = []  # 현재 처리 중인 이슈들

    def add_issue(self, issue_data):
        """
        이슈 추가

        Args:
            issue_data: {
                'issue_id': 'I-01',
                'work_type': '구조',
                'delay_weeks': 4.5,
                'float_days': 0,
                'detected': True
            }
        """
        self.active_issues.append(issue_data)

    def calculate_total_delay(self):
        """
        여러 이슈의 총 지연 계산 (CPM 방식)

        Returns:
            float: 총 지연 (주 단위)
        """
        if not self.active_issues:
            return 0.0

        # 1단계: 공종별 그룹핑 및 합산
        work_type_delays = self._group_by_work_type()

        # 2단계: Float 적용하여 실제 영향 계산
        effective_delays = self._apply_float(work_type_delays)

        # 3단계: 크리티컬 패스 계산
        total_delay = self._calculate_critical_path(effective_delays)

        # 4단계: 동시 이슈 관리 오버헤드 추가
        total_delay = self._apply_concurrency_overhead(total_delay)

        return total_delay

    def _group_by_work_type(self):
        """공종별로 이슈 그룹핑 및 지연 합산"""
        work_type_delays = defaultdict(float)

        for issue in self.active_issues:
            work_type = issue['work_type']
            delay = issue['delay_weeks']
            work_type_delays[work_type] += delay

        return dict(work_type_delays)

    def _apply_float(self, work_type_delays):
        """
        Float 적용: 여유시간 범위 내 지연은 흡수

        Float (여유시간) = 해당 공종이 프로젝트 전체에 영향 없이 지연될 수 있는 시간
        Float = 0 이면 크리티컬 패스 (지연 시 프로젝트 전체 지연)
        Float > 0 이면 그 범위 내에서 지연 흡수 가능
        """
        effective_delays = {}

        for work_type, delay_weeks in work_type_delays.items():
            float_days = get_float_days(work_type)
            float_weeks = float_days / 7.0

            # Float 범위 내에서 흡수
            absorbed = min(delay_weeks, float_weeks)
            actual_impact = delay_weeks - absorbed

            # 음수 방지
            effective_delays[work_type] = max(0, actual_impact)

        return effective_delays

    def _calculate_critical_path(self, effective_delays):
        """
        크리티컬 패스 계산 (동적 계획법)

        각 공종까지의 최장 경로를 계산
        """
        memo = {}

        def get_path_length(work_type):
            """해당 공종까지의 최장 경로 길이 (재귀 + 메모이제이션)"""
            if work_type in memo:
                return memo[work_type]

            # 선행 공종들
            deps = WORK_DEPENDENCIES.get(work_type, [])

            if not deps:
                # 선행 없음: 현재 공종의 지연만
                result = effective_delays.get(work_type, 0)
            else:
                # 선행 공종들 중 최대값 + 현재 공종 지연
                max_dep_delay = max(
                    get_path_length(dep)
                    for dep in deps
                    if dep in effective_delays or has_dependencies_with_delay(dep)
                )
                result = max_dep_delay + effective_delays.get(work_type, 0)

            memo[work_type] = result
            return result

        def has_dependencies_with_delay(work_type):
            """해당 공종 또는 선행 공종에 지연이 있는지 확인"""
            if work_type in effective_delays and effective_delays[work_type] > 0:
                return True
            deps = WORK_DEPENDENCIES.get(work_type, [])
            return any(has_dependencies_with_delay(dep) for dep in deps)

        # 모든 공종의 경로 중 최대값이 총 지연
        if not effective_delays:
            return 0.0

        total_delay = max(
            get_path_length(work_type)
            for work_type in effective_delays.keys()
        )

        return total_delay

    def _apply_concurrency_overhead(self, base_delay):
        """
        동시 다발 이슈 발생 시 관리 오버헤드 적용

        5개 이상 이슈가 동시에 진행되면:
        - 현장 혼란도 증가
        - 의사결정 지연
        - 리소스 분산으로 인한 비효율

        → 5개 초과시 1개당 5% 추가
        """
        issue_count = len(self.active_issues)

        if issue_count <= 5:
            return base_delay

        # 5개 초과시 1개당 5% 오버헤드
        overhead_multiplier = 1.0 + (issue_count - 5) * 0.05

        return base_delay * overhead_multiplier

    def get_summary(self):
        """계산 요약 정보 반환"""
        work_type_delays = self._group_by_work_type()
        effective_delays = self._apply_float(work_type_delays)

        summary = {
            'total_issues': len(self.active_issues),
            'work_types': len(work_type_delays),
            'raw_delays': work_type_delays,
            'effective_delays': effective_delays,
            'total_delay': self.calculate_total_delay()
        }

        return summary

    def clear(self):
        """이슈 리스트 초기화"""
        self.active_issues = []
