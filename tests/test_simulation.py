"""
시뮬레이션 통합 테스트
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models.project import Project
from models.bim_quality import BIMQuality
from config.bim_quality_config import BIMQualityConfig
from agents.owner_agent import OwnerAgent
from agents.designer_agent import DesignerAgent
from agents.contractor_agent import ContractorAgent
from agents.supervisor_agent import SupervisorAgent
from agents.bank_agent import BankAgent
from simulation.issue_manager import IssueManager
from simulation.impact_calculator import ImpactCalculator

def test_project_initialization():
    """프로젝트 초기화 테스트"""
    print("\n=== 프로젝트 초기화 테스트 ===")
    
    project_off = Project(bim_enabled=False)
    assert project_off.bim_enabled == False, "BIM OFF 설정 오류"
    print("✓ BIM OFF 프로젝트 초기화 성공")
    
    project_on = Project(bim_enabled=True, bim_quality=BIMQualityConfig.BIM_GOOD)
    assert project_on.bim_enabled == True, "BIM ON 설정 오류"
    print("✓ BIM ON 프로젝트 초기화 성공\n")

def test_bim_quality_calculation():
    """BIM 품질 계산 테스트"""
    print("=== BIM 품질 계산 테스트 ===")
    
    bim_quality = BIMQualityConfig.BIM_GOOD
    
    normalized = BIMQuality.normalize_metrics(bim_quality)
    print(f"정규화된 지표: {normalized}")
    
    effectiveness = BIMQuality.calculate_effectiveness('I-01', bim_quality)
    print(f"I-01 이슈 효과성: {effectiveness:.4f}")
    
    assert 0 <= effectiveness <= 1, "효과성이 0~1 범위를 벗어남"
    
    quality_score = BIMQuality.get_quality_score(bim_quality)
    print(f"전체 품질 점수: {quality_score:.4f}")
    
    quality_level = BIMQuality.get_quality_level(bim_quality)
    print(f"품질 등급: {quality_level}")
    
    print("✓ BIM 품질 계산 테스트 통과\n")

def test_issue_manager():
    """이슈 관리자 테스트"""
    print("=== 이슈 관리자 테스트 ===")
    
    issue_manager = IssueManager()
    
    total_issues = len(issue_manager.all_issues)
    print(f"전체 이슈 수: {total_issues}건")
    
    assert total_issues == 27, "이슈 카드 수가 27개가 아님"
    
    issue = issue_manager.get_issue_by_id('I-01')
    assert issue is not None, "I-01 이슈를 찾을 수 없음"
    print(f"I-01 이슈: {issue['name']}")
    
    design_issues = issue_manager.get_issues_by_category('설계')
    print(f"설계 단계 이슈: {len(design_issues)}건")
    
    print("✓ 이슈 관리자 테스트 통과\n")

def test_impact_calculation():
    """영향도 계산 테스트"""
    print("=== 영향도 계산 테스트 ===")
    
    project_off = Project(bim_enabled=False)
    project_on = Project(bim_enabled=True, bim_quality=BIMQualityConfig.BIM_GOOD)
    
    issue_manager = IssueManager()
    issue = issue_manager.get_issue_by_id('I-01')
    
    impact_off = ImpactCalculator.calculate_impact(issue, project_off)
    print(f"BIM OFF 영향:")
    print(f"  지연: {impact_off['delay_weeks']:.2f}주")
    print(f"  비용: {impact_off['cost_increase']*100:.2f}%")
    print(f"  탐지: {impact_off['detected']}")
    
    impact_on = ImpactCalculator.calculate_impact(issue, project_on)
    print(f"\nBIM ON 영향:")
    print(f"  지연: {impact_on['delay_weeks']:.2f}주")
    print(f"  비용: {impact_on['cost_increase']*100:.2f}%")
    print(f"  탐지: {impact_on['detected']}")
    print(f"  효과성: {impact_on['bim_effectiveness']:.4f}")
    
    assert impact_on['delay_weeks'] <= impact_off['delay_weeks'], "BIM ON 지연이 더 큼"
    assert impact_on['cost_increase'] <= impact_off['cost_increase'], "BIM ON 비용이 더 큼"
    
    print("\n✓ 영향도 계산 테스트 통과\n")

def run_all_tests():
    """모든 테스트 실행"""
    print("\n" + "="*50)
    print("시뮬레이션 통합 테스트 시작")
    print("="*50)
    
    test_project_initialization()
    test_bim_quality_calculation()
    test_issue_manager()
    test_impact_calculation()
    
    print("="*50)
    print("모든 테스트 통과!")
    print("="*50 + "\n")

if __name__ == '__main__':
    run_all_tests()