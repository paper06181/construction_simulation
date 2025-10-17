"""
금융 비용 계산
"""

from config.project_config import ProjectConfig

class FinancialCalculator:
    """금융 비용 계산기"""
    
    @staticmethod
    def calculate_financial_cost(project, delay_weeks):
        """지연에 따른 금융 비용 계산"""
        delay_days = delay_weeks * 7
        delay_months = delay_days / 30
        
        loan_amount = project.budget * ProjectConfig.PF_RATIO
        base_rate = ProjectConfig.BASE_INTEREST_RATE
        
        rate_increase_bp = FinancialCalculator.get_rate_increase(delay_months)
        rate_increase = rate_increase_bp / 10000
        
        additional_interest = loan_amount * rate_increase * (delay_days / 365)
        
        daily_indirect = project.budget * ProjectConfig.DAILY_INDIRECT_COST_RATIO
        additional_indirect = daily_indirect * delay_days
        
        total_financial_cost = additional_interest + additional_indirect
        
        new_rate = base_rate + rate_increase
        
        return {
            'interest_increase': additional_interest,
            'indirect_cost': additional_indirect,
            'total_financial_cost': total_financial_cost,
            'rate_increase_bp': rate_increase_bp,
            'new_interest_rate': new_rate,
            'delay_months': delay_months
        }
    
    @staticmethod
    def get_rate_increase(delay_months):
        """지연 개월수에 따른 금리 인상 (bp)"""
        delay_months_int = int(delay_months)
        
        if delay_months_int in ProjectConfig.DELAY_RATE_INCREASE:
            return ProjectConfig.DELAY_RATE_INCREASE[delay_months_int]
        
        if delay_months_int >= 7:
            return 100
        
        return 0
    
    @staticmethod
    def update_project_interest_rate(project, financial_result):
        """프로젝트 금리 업데이트"""
        if financial_result['rate_increase_bp'] > 0:
            project.current_interest_rate = financial_result['new_interest_rate']
            project.interest_rate_increases.append({
                'day': project.current_day,
                'delay_months': financial_result['delay_months'],
                'increase_bp': financial_result['rate_increase_bp'],
                'new_rate': financial_result['new_interest_rate']
            })