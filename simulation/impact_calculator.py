"""
이슈 영향도 계산 (핵심 로직)
"""

import random
from models.bim_quality import BIMQuality
from models.financial import FinancialCalculator
from simulation.negotiation_system import NegotiationSystem

class ImpactCalculator:
    """이슈 영향도 계산기"""

    def __init__(self):
        """협상 시스템 초기화"""
        self.negotiation_system = NegotiationSystem()

    def calculate_impact(self, issue, project):
        """이슈의 최종 영향 계산"""
        if not project.bim_enabled:
            return self._calculate_traditional_impact(
                issue, project
            )
        else:
            return self._calculate_bim_impact(
                issue, project
            )

    def _calculate_traditional_impact(self, issue, project):
        """전통 방식 영향 계산 (협상 시스템 사용)"""
        # 협상을 통해 최종 지연/비용 결정
        negotiation_result = self.negotiation_system.negotiate(
            issue, project, detected=False
        )

        actual_delay = negotiation_result['delay_weeks']
        actual_cost = negotiation_result['cost_increase']

        # 추가 불확실성 (전통 방식은 예측이 어려움)
        uncertainty_multiplier = random.uniform(1.0, 1.15)
        actual_delay *= uncertainty_multiplier
        actual_cost *= uncertainty_multiplier

        financial_cost = FinancialCalculator.calculate_financial_cost(
            project, actual_delay
        )

        if financial_cost['rate_increase_bp'] > 0:
            FinancialCalculator.update_project_interest_rate(project, financial_cost)

        return {
            'issue_id': issue['id'],
            'issue_name': issue['name'],
            'delay_weeks': actual_delay,
            'cost_increase': actual_cost,
            'detected': False,
            'detection_phase': None,
            'bim_effectiveness': 0.0,
            'detection_probability': 0.0,
            'financial_cost': financial_cost,
            'negotiation_summary': negotiation_result['negotiation_summary']
        }

    def _calculate_bim_impact(self, issue, project):
        """BIM 적용 시 영향 계산 (협상 시스템 사용)"""
        bim_effectiveness = BIMQuality.calculate_effectiveness(
            issue['id'],
            project.bim_quality
        )

        detection_prob = BIMQuality.calculate_detection_probability(
            issue,
            bim_effectiveness
        )

        detected = random.random() < detection_prob

        if not detected:
            # 미탐지 시: 협상으로 결정하되 불확실성 추가
            negotiation_result = self.negotiation_system.negotiate(
                issue, project, detected=False
            )

            actual_delay = negotiation_result['delay_weeks']
            actual_cost = negotiation_result['cost_increase']

            # BIM 있어도 미탐지면 약간의 불확실성
            uncertainty_multiplier = random.uniform(1.05, 1.15)
            actual_delay *= uncertainty_multiplier
            actual_cost *= uncertainty_multiplier

            financial_cost = FinancialCalculator.calculate_financial_cost(
                project, actual_delay
            )

            if financial_cost['rate_increase_bp'] > 0:
                FinancialCalculator.update_project_interest_rate(project, financial_cost)

            return {
                'issue_id': issue['id'],
                'issue_name': issue['name'],
                'delay_weeks': actual_delay,
                'cost_increase': actual_cost,
                'detected': False,
                'detection_phase': None,
                'bim_effectiveness': bim_effectiveness,
                'detection_probability': detection_prob,
                'financial_cost': financial_cost,
                'negotiation_summary': negotiation_result['negotiation_summary']
            }

        # 조기 탐지 성공: 협상 + BIM 절감 효과
        detection_phase = issue['bim_effect']['detection_phase']

        # 1단계: 협상으로 기본 값 결정 (BIM 탐지 효과 반영)
        negotiation_result = self.negotiation_system.negotiate(
            issue, project, detected=True
        )

        negotiated_delay = negotiation_result['delay_weeks']
        negotiated_cost = negotiation_result['cost_increase']

        # 2단계: BIM 조기 탐지 추가 절감 효과
        reduction_by_phase = {
            '설계': {'delay': 0.70, 'cost': 0.80},      # 설계 단계 탐지 → 70% 추가 절감
            '발주': {'delay': 0.50, 'cost': 0.60},      # 발주 단계 탐지 → 50% 추가 절감
            '시공초기': {'delay': 0.30, 'cost': 0.40},  # 시공초기 → 30% 추가 절감
            '시공중기': {'delay': 0.15, 'cost': 0.20},  # 시공중기 → 15% 추가 절감
            '시공후기': {'delay': 0.05, 'cost': 0.10}   # 시공후기 → 5% 추가 절감
        }

        reduction = reduction_by_phase.get(
            detection_phase,
            {'delay': 0.3, 'cost': 0.4}
        )

        # BIM 품질 보너스
        quality_bonus = bim_effectiveness * 0.15

        # 최종 절감률
        final_delay_reduction = min(0.95, reduction['delay'] + quality_bonus)
        final_cost_reduction = min(0.95, reduction['cost'] + quality_bonus)

        # 협상된 값에서 추가 절감
        actual_delay = negotiated_delay * (1.0 - final_delay_reduction)
        actual_cost = negotiated_cost * (1.0 - final_cost_reduction)

        financial_cost = FinancialCalculator.calculate_financial_cost(
            project, actual_delay
        )

        if financial_cost['rate_increase_bp'] > 0:
            FinancialCalculator.update_project_interest_rate(project, financial_cost)

        return {
            'issue_id': issue['id'],
            'issue_name': issue['name'],
            'delay_weeks': actual_delay,
            'cost_increase': actual_cost,
            'detected': True,
            'detection_phase': detection_phase,
            'bim_effectiveness': bim_effectiveness,
            'detection_probability': detection_prob,
            'financial_cost': financial_cost,
            'negotiation_summary': negotiation_result['negotiation_summary'],
            'savings': {
                'delay_avoided': negotiated_delay - actual_delay,
                'cost_avoided': negotiated_cost - actual_cost
            }
        }
