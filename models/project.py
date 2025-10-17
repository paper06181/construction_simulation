"""
프로젝트 모델
"""

from config.project_config import ProjectConfig
from config.project_templates import ProjectTemplates
from simulation.delay_calculator import DelayCalculator

class Project:
    """건설 프로젝트 모델"""

    def __init__(self, bim_enabled=False, bim_quality=None, template=None):
        # 템플릿이 지정된 경우 템플릿 사용
        if template:
            project_data = ProjectTemplates.get_template(template)
            self.name = project_data['name']
            self.location = project_data['location']
            self.gfa = project_data['gfa']
            self.budget = project_data['budget']
            self.planned_duration = project_data['duration']
            self.building_type = project_data['building_type']
            self.pf_ratio = project_data['pf_ratio']
            self.base_interest_rate = project_data['base_interest_rate']
            self.phase_durations = project_data['phase_durations']
        else:
            # 기본 설정 (ProjectConfig)
            self.name = ProjectConfig.PROJECT_NAME
            self.location = ProjectConfig.LOCATION
            self.gfa = ProjectConfig.GFA
            self.budget = ProjectConfig.TOTAL_BUDGET
            self.planned_duration = ProjectConfig.TOTAL_DURATION
            self.building_type = ProjectConfig.USE
            self.pf_ratio = ProjectConfig.PF_RATIO
            self.base_interest_rate = ProjectConfig.BASE_INTEREST_RATE
            self.phase_durations = ProjectConfig.PHASE_DURATIONS
        
        self.bim_enabled = bim_enabled
        self.bim_quality = bim_quality if bim_quality else {
            'warning_density': 0.0,
            'clash_density': 0.0,
            'attribute_fill': 0.0,
            'phase_link': 0.0
        }
        
        self.current_day = 0
        self.current_phase = '설계'
        self.actual_duration = 0
        self.actual_cost = self.budget
        
        self.total_delay_weeks = 0.0
        self.total_cost_increase = 0.0
        self.total_financial_cost = 0.0
        
        self.issues_occurred = []
        self.issues_detected = []
        self.issues_missed = []
        
        self.rfi_count = 0
        self.rework_count = 0
        
        self.current_interest_rate = self.base_interest_rate
        self.interest_rate_increases = []
        
        self.phase_history = []
        
    def advance_day(self):
        """하루 진행"""
        self.current_day += 1
        new_phase = ProjectConfig.get_phase_by_day(self.current_day)
        
        if new_phase != self.current_phase:
            self.phase_history.append({
                'phase': self.current_phase,
                'end_day': self.current_day - 1
            })
            self.current_phase = new_phase
    
    def apply_impact(self, impact_result):
        """이슈 영향 적용"""
        self.total_delay_weeks += impact_result['delay_weeks']
        self.total_cost_increase += impact_result['cost_increase']
        
        if impact_result.get('financial_cost'):
            self.total_financial_cost += impact_result['financial_cost']['total_financial_cost']
        
        if impact_result['detected']:
            self.issues_detected.append(impact_result['issue_id'])
        else:
            self.issues_missed.append(impact_result['issue_id'])
        
        self.issues_occurred.append(impact_result)
    
    def calculate_final_metrics(self):
        """최종 지표 계산"""
        delay_days = self.total_delay_weeks * 7
        self.actual_duration = self.planned_duration + delay_days
        
        direct_cost_increase = self.budget * self.total_cost_increase
        self.actual_cost = self.budget + direct_cost_increase + self.total_financial_cost
        
        schedule_delay_rate = delay_days / self.planned_duration
        budget_overrun_rate = (self.actual_cost - self.budget) / self.budget
        
        return {
            'planned_duration': self.planned_duration,
            'actual_duration': self.actual_duration,
            'delay_days': delay_days,
            'delay_weeks': self.total_delay_weeks,
            'schedule_delay_rate': schedule_delay_rate,
            'planned_budget': self.budget,
            'actual_cost': self.actual_cost,
            'cost_increase': self.actual_cost - self.budget,
            'budget_overrun_rate': budget_overrun_rate,
            'direct_cost_increase': direct_cost_increase,
            'financial_cost': self.total_financial_cost,
            'issues_count': len(self.issues_occurred),
            'detected_count': len(self.issues_detected),
            'missed_count': len(self.issues_missed),
            'detection_rate': len(self.issues_detected) / len(self.issues_occurred) if self.issues_occurred else 0,
            'rfi_count': self.rfi_count,
            'rework_count': self.rework_count,
            'final_interest_rate': self.current_interest_rate
        }
    
    def get_summary(self):
        """프로젝트 요약"""
        metrics = self.calculate_final_metrics()
        
        return f"""
========================================
프로젝트: {self.name}
BIM 적용: {'ON' if self.bim_enabled else 'OFF'}
========================================

[기간]
계획: {self.planned_duration}일
실제: {metrics['actual_duration']:.1f}일
지연: {metrics['delay_days']:.1f}일 ({metrics['delay_weeks']:.1f}주)
지연률: {metrics['schedule_delay_rate']*100:.1f}%

[비용]
계획: {self.budget:,.0f}원
실제: {metrics['actual_cost']:,.0f}원
초과: {metrics['cost_increase']:,.0f}원
초과율: {metrics['budget_overrun_rate']*100:.1f}%
- 직접비용: {metrics['direct_cost_increase']:,.0f}원
- 금융비용: {metrics['financial_cost']:,.0f}원

[이슈]
발생: {metrics['issues_count']}건
탐지: {metrics['detected_count']}건
미탐지: {metrics['missed_count']}건
탐지율: {metrics['detection_rate']*100:.1f}%

[기타]
RFI: {self.rfi_count}건
재시공: {self.rework_count}건
최종금리: {metrics['final_interest_rate']*100:.2f}%
========================================
"""