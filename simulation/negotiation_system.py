"""
회의 기반 협상 시스템
에이전트들이 이슈 카드 범위 내에서 최종 지연/비용 결정
"""

class NegotiationSystem:
    """에이전트 협상 시스템"""

    def __init__(self):
        # 에이전트별 선호도 (0.0~1.0)
        # 0.0 = 최소값 선호, 1.0 = 최대값 선호
        self.agent_preferences = {
            'owner': 0.25,       # 건축주: 빡빡하게 (25% 위치)
            'contractor': 0.75,  # 시공사: 여유롭게 (75% 위치)
            'supervisor': 0.50,  # 감리사: 중립적 (50% 위치)
            'designer': 0.40,    # 설계사: 약간 빡빡 (40% 위치)
            'bank': 0.60        # 금융사: 약간 여유 (60% 위치)
        }

        # 에이전트별 영향력/가중치
        self.agent_weights = {
            'owner': 0.40,       # 건축주: 40% (최종 의사결정권자)
            'contractor': 0.25,  # 시공사: 25%
            'supervisor': 0.20,  # 감리사: 20%
            'designer': 0.10,    # 설계사: 10%
            'bank': 0.05        # 금융사: 5%
        }

    def negotiate(self, issue, project, detected=False):
        """
        협상을 통해 최종 지연/비용 결정

        Args:
            issue: 이슈 정보 (범위 포함)
            project: 프로젝트 정보 (건물 특성 반영)
            detected: BIM으로 조기 탐지 여부

        Returns:
            {
                'delay_weeks': float,
                'cost_increase': float,
                'negotiation_summary': str
            }
        """
        delay_min = issue['delay_weeks_min']
        delay_max = issue['delay_weeks_max']
        cost_min = issue['cost_increase_min']
        cost_max = issue['cost_increase_max']

        # 프로젝트 특성에 따른 선호도/가중치 조정
        adjusted_prefs, adjusted_weights = self._adjust_by_project_type(
            project, detected
        )

        # 최종 위치 계산 (가중 평균)
        final_position = sum(
            adjusted_prefs[agent] * adjusted_weights[agent]
            for agent in adjusted_prefs
        )

        # 범위 내에서 값 결정
        agreed_delay = delay_min + (delay_max - delay_min) * final_position
        agreed_cost = cost_min + (cost_max - cost_min) * final_position

        # 협상 요약
        summary = self._generate_summary(
            issue, project, detected,
            agreed_delay, agreed_cost,
            final_position
        )

        return {
            'delay_weeks': agreed_delay,
            'cost_increase': agreed_cost,
            'negotiation_summary': summary,
            'final_position': final_position  # 0.0~1.0
        }

    def _adjust_by_project_type(self, project, detected):
        """
        프로젝트 특성에 따라 선호도/가중치 조정

        건물 종류, 규모, 예산, BIM 탐지 여부 고려
        """
        prefs = self.agent_preferences.copy()
        weights = self.agent_weights.copy()

        # BIM 조기 탐지 시: 건축주가 더 강하게 압박
        if detected and project.bim_enabled:
            prefs['owner'] = 0.20   # 더 빡빡하게
            weights['owner'] = 0.45  # 영향력 증가 (40% → 45%)
            weights['contractor'] = 0.22  # 시공사 영향력 감소

        # 프로젝트 규모에 따른 조정
        if project.budget > 5_000_000_000:  # 50억 이상 대형
            # 대형 프로젝트: 공기 준수 중요
            prefs['owner'] = prefs['owner'] - 0.05  # 더 빡빡
            prefs['bank'] = prefs['bank'] - 0.05    # 금융사도 민감
        elif project.budget < 2_000_000_000:  # 20억 미만 소형
            # 소형 프로젝트: 유연하게 대응 가능
            prefs['owner'] = prefs['owner'] + 0.05  # 약간 여유
            prefs['contractor'] = prefs['contractor'] - 0.05

        # 프로젝트 이름으로 건물 유형 추정
        project_name = project.name.lower()

        if '아파트' in project_name or 'apartment' in project_name:
            # 아파트: 공기 지연 매우 민감 (분양 일정)
            prefs['owner'] = max(0.15, prefs['owner'] - 0.10)
            weights['owner'] = 0.50  # 건축주 영향력 최대

        elif '오피스' in project_name or 'office' in project_name:
            # 오피스: 품질 중요
            prefs['supervisor'] = prefs['supervisor'] + 0.10
            weights['supervisor'] = 0.25  # 감리사 영향력 증가

        elif '주택' in project_name or 'house' in project_name:
            # 단독주택: 건축주가 직접 관여
            weights['owner'] = 0.55  # 건축주 영향력 극대화
            prefs['owner'] = 0.30    # 하지만 어느정도 수용

        elif '근린생활' in project_name or 'commercial' in project_name:
            # 근생: 비용 절감 중요
            prefs['owner'] = 0.20    # 비용 최소화
            prefs['bank'] = 0.50     # 금융사도 비용 중요시

        # 현재 프로젝트 상황 반영
        if project.current_day > project.planned_duration * 0.8:
            # 공사 막바지 (80% 이상 진행)
            # → 추가 지연 회피, 비용 투입해서라도 빨리 마무리
            prefs['owner'] = max(0.10, prefs['owner'] - 0.15)
            prefs['contractor'] = max(0.40, prefs['contractor'] - 0.20)

        return prefs, weights

    def _generate_summary(self, issue, project, detected, delay, cost, position):
        """협상 결과 요약 생성 (상세 버전)"""

        # 프로젝트 특성 반영된 선호도/가중치
        prefs, weights = self._adjust_by_project_type(project, detected)

        # 위치에 따른 설명
        if position < 0.35:
            outcome = "강하게 압박하여 최소 수준으로 합의"
        elif position < 0.50:
            outcome = "건축주 주도로 빡빡하게 합의"
        elif position < 0.65:
            outcome = "중립적 수준에서 합의"
        elif position < 0.80:
            outcome = "시공사에 여유를 주는 선에서 합의"
        else:
            outcome = "시공사 요구를 대부분 수용하여 합의"

        # BIM 탐지 효과
        detection_note = ""
        if detected and project.bim_enabled:
            detection_note = " (BIM 조기 탐지로 건축주 협상력 증가)"

        # 상세 협상 과정
        summary_lines = []
        summary_lines.append(f"[협상 과정]")
        summary_lines.append(f"  건축주 입장: {prefs['owner']*100:.0f}% 위치 선호 ({'빡빡' if prefs['owner'] < 0.5 else '여유'}), 영향력 {weights['owner']*100:.0f}%")
        summary_lines.append(f"  시공사 입장: {prefs['contractor']*100:.0f}% 위치 선호 (여유롭게), 영향력 {weights['contractor']*100:.0f}%")
        summary_lines.append(f"  감리사 입장: {prefs['supervisor']*100:.0f}% 위치 선호 (중립), 영향력 {weights['supervisor']*100:.0f}%")
        summary_lines.append(f"  설계사 입장: {prefs['designer']*100:.0f}% 위치 선호, 영향력 {weights['designer']*100:.0f}%")
        summary_lines.append(f"  금융사 입장: {prefs['bank']*100:.0f}% 위치 선호, 영향력 {weights['bank']*100:.0f}%")
        summary_lines.append("")
        summary_lines.append(f"[협상 결과] {outcome}{detection_note}")
        summary_lines.append(f"  최종 협상 위치: {position*100:.0f}% (0%=최소, 100%=최대)")
        summary_lines.append(f"  합의 지연: {delay:.1f}주 (범위: {issue['delay_weeks_min']}~{issue['delay_weeks_max']}주)")
        summary_lines.append(f"  합의 비용: {cost*100:.1f}% (범위: {issue['cost_increase_min']*100:.1f}~{issue['cost_increase_max']*100:.1f}%)")

        return '\n'.join(summary_lines)

    def get_agent_stance(self, agent_name, issue, project):
        """
        특정 에이전트의 입장 설명
        (향후 LLM 프롬프트에 사용)
        """
        prefs, weights = self._adjust_by_project_type(project, False)

        pref = prefs[agent_name]
        weight = weights[agent_name]

        if agent_name == 'owner':
            if pref < 0.3:
                stance = "지연/비용 최소화 강력 요구"
            else:
                stance = "지연/비용 절감 요구"
        elif agent_name == 'contractor':
            if pref > 0.7:
                stance = "충분한 여유 필요"
            else:
                stance = "적정 수준 요청"
        elif agent_name == 'supervisor':
            stance = "품질 확보 관점에서 의견"
        elif agent_name == 'designer':
            stance = "설계 품질 유지 필요"
        else:  # bank
            stance = "금융 리스크 관리 관점"

        return {
            'stance': stance,
            'influence': weight,
            'preference_position': pref
        }
