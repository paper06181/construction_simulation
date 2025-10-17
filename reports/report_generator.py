"""
결과 보고서 생성
"""

class ReportGenerator:
    """보고서 생성기"""
    
    @staticmethod
    def generate_comparison_report(metrics_off, metrics_on):
        """BIM ON/OFF 비교 보고서"""
        report = f"""
{'='*80}
BIM 적용 효과 비교 보고서
{'='*80}

1. 공사 기간
{'─'*80}
구분              | 계획(일)  | 실제(일)  | 지연(일)  | 지연률
{'─'*80}
BIM OFF          | {metrics_off['planned_duration']:7.0f}   | {metrics_off['actual_duration']:7.1f}   | {metrics_off['delay_days']:7.1f}   | {metrics_off['schedule_delay_rate']*100:5.1f}%
BIM ON           | {metrics_on['planned_duration']:7.0f}   | {metrics_on['actual_duration']:7.1f}   | {metrics_on['delay_days']:7.1f}   | {metrics_on['schedule_delay_rate']*100:5.1f}%
{'─'*80}
개선 효과        | -        | {metrics_off['actual_duration']-metrics_on['actual_duration']:7.1f}일 단축 | {metrics_off['delay_days']-metrics_on['delay_days']:7.1f}일 감소 | {(metrics_off['schedule_delay_rate']-metrics_on['schedule_delay_rate'])*100:5.1f}%p

2. 공사 비용
{'─'*80}
구분              | 계획(억원) | 실제(억원) | 초과(억원) | 초과율
{'─'*80}
BIM OFF          | {metrics_off['planned_budget']/100000000:7.1f}    | {metrics_off['actual_cost']/100000000:7.1f}    | {metrics_off['cost_increase']/100000000:7.1f}    | {metrics_off['budget_overrun_rate']*100:5.1f}%
BIM ON           | {metrics_on['planned_budget']/100000000:7.1f}    | {metrics_on['actual_cost']/100000000:7.1f}    | {metrics_on['cost_increase']/100000000:7.1f}    | {metrics_on['budget_overrun_rate']*100:5.1f}%
{'─'*80}
절감 효과        | -         | -         | {(metrics_off['cost_increase']-metrics_on['cost_increase'])/100000000:7.1f}억원 | {(metrics_off['budget_overrun_rate']-metrics_on['budget_overrun_rate'])*100:5.1f}%p

3. 비용 세부 내역
{'─'*80}
구분              | 직접비용(억원) | 금융비용(억원) | 합계(억원)
{'─'*80}
BIM OFF          | {metrics_off['direct_cost_increase']/100000000:11.2f}      | {metrics_off['financial_cost']/100000000:11.2f}      | {metrics_off['cost_increase']/100000000:8.2f}
BIM ON           | {metrics_on['direct_cost_increase']/100000000:11.2f}      | {metrics_on['financial_cost']/100000000:11.2f}      | {metrics_on['cost_increase']/100000000:8.2f}
{'─'*80}
절감             | {(metrics_off['direct_cost_increase']-metrics_on['direct_cost_increase'])/100000000:11.2f}      | {(metrics_off['financial_cost']-metrics_on['financial_cost'])/100000000:11.2f}      | {(metrics_off['cost_increase']-metrics_on['cost_increase'])/100000000:8.2f}

4. 이슈 관리
{'─'*80}
구분              | 발생(건) | 탐지(건) | 미탐지(건) | 탐지율
{'─'*80}
BIM OFF          | {metrics_off['issues_count']:6}   | {metrics_off['detected_count']:6}   | {metrics_off['missed_count']:8}   | {metrics_off['detection_rate']*100:5.1f}%
BIM ON           | {metrics_on['issues_count']:6}   | {metrics_on['detected_count']:6}   | {metrics_on['missed_count']:8}   | {metrics_on['detection_rate']*100:5.1f}%
{'─'*80}
개선             | {metrics_off['issues_count']-metrics_on['issues_count']:6}   | +{metrics_on['detected_count']-metrics_off['detected_count']:5}   | {metrics_off['missed_count']-metrics_on['missed_count']:8}   | +{(metrics_on['detection_rate']-metrics_off['detection_rate'])*100:5.1f}%p

5. 금융 지표
{'─'*80}
구분              | 최종 금리
{'─'*80}
BIM OFF          | {metrics_off['final_interest_rate']*100:6.2f}%
BIM ON           | {metrics_on['final_interest_rate']*100:6.2f}%
{'─'*80}
차이             | {(metrics_off['final_interest_rate']-metrics_on['final_interest_rate'])*10000:6.0f}bp

{'='*80}
핵심 요약
{'='*80}
BIM 적용을 통한 개선 효과:
- 공사 기간: {metrics_off['delay_days']-metrics_on['delay_days']:.1f}일 단축 ({(1-metrics_on['schedule_delay_rate']/metrics_off['schedule_delay_rate'])*100 if metrics_off['schedule_delay_rate'] > 0 else 0:.1f}% 개선)
- 공사 비용: {(metrics_off['cost_increase']-metrics_on['cost_increase'])/100000000:.2f}억원 절감 ({(1-metrics_on['budget_overrun_rate']/metrics_off['budget_overrun_rate'])*100 if metrics_off['budget_overrun_rate'] > 0 else 0:.1f}% 개선)
- 이슈 탐지율: {(metrics_on['detection_rate']-metrics_off['detection_rate'])*100:.1f}%p 향상
- 금리 인상 억제: {(metrics_off['final_interest_rate']-metrics_on['final_interest_rate'])*10000:.0f}bp 절감
{'='*80}
"""
        return report
    
    @staticmethod
    def generate_single_report(metrics, scenario_name):
        """단일 시나리오 보고서"""
        report = f"""
{'='*70}
{scenario_name} 시나리오 결과 보고서
{'='*70}

1. 프로젝트 개요
  - 프로젝트명: 청담동 근린생활시설 신축공사
  - 계획 예산: {metrics['planned_budget']/100000000:.1f}억원
  - 계획 공기: {metrics['planned_duration']}일

2. 최종 결과
  - 실제 공기: {metrics['actual_duration']:.0f}일
  - 지연: {metrics['delay_days']:.0f}일 ({metrics['delay_weeks']:.1f}주)
  - 지연률: {metrics['schedule_delay_rate']*100:.1f}%
  
  - 실제 비용: {metrics['actual_cost']/100000000:.2f}억원
  - 초과: {metrics['cost_increase']/100000000:.2f}억원
  - 초과율: {metrics['budget_overrun_rate']*100:.1f}%

3. 비용 세부
  - 직접 비용 증가: {metrics['direct_cost_increase']/100000000:.2f}억원
  - 금융 비용: {metrics['financial_cost']/100000000:.2f}억원

4. 이슈 통계
  - 발생: {metrics['issues_count']}건
  - 탐지: {metrics['detected_count']}건
  - 미탐지: {metrics['missed_count']}건
  - 탐지율: {metrics['detection_rate']*100:.1f}%

5. 금융
  - 최종 금리: {metrics['final_interest_rate']*100:.2f}%

{'='*70}
"""
        return report