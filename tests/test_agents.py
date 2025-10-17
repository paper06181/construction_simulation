"""
에이전트 테스트
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agents.owner_agent import OwnerAgent
from agents.designer_agent import DesignerAgent
from agents.contractor_agent import ContractorAgent
from agents.supervisor_agent import SupervisorAgent
from agents.bank_agent import BankAgent
from models.project import Project

def test_agent_initialization():
    """에이전트 초기화 테스트"""
    print("\n=== 에이전트 초기화 테스트 ===")
    
    owner = OwnerAgent()
    designer = DesignerAgent()
    contractor = ContractorAgent()
    supervisor = SupervisorAgent()
    bank = BankAgent()
    
    assert owner.name == "건축주", "건축주 초기화 실패"
    assert designer.name == "설계사", "설계사 초기화 실패"
    assert contractor.name == "시공사", "시공사 초기화 실패"
    assert supervisor.name == "감리사", "감리사 초기화 실패"
    assert bank.name == "금융사", "금융사 초기화 실패"
    
    print("✓ 모든 에이전트 초기화 성공\n")

def test_agent_response():
    """에이전트 응답 테스트"""
    print("=== 에이전트 응답 테스트 ===")
    
    project = Project(bim_enabled=False)
    owner = OwnerAgent()
    
    issue = {
        'id': 'I-01',
        'name': '설비-구조 간섭 미발견',
        'category': '설계',
        'severity': 'S3'
    }
    
    response = owner.respond(issue, project, None)
    
    assert response is not None, "응답 생성 실패"
    assert len(response) > 0, "응답 내용이 비어있음"
    print(f"건축주 응답: {response}")
    
    print("✓ 에이전트 응답 테스트 통과\n")

def run_all_tests():
    """모든 테스트 실행"""
    print("\n" + "="*50)
    print("에이전트 테스트 시작")
    print("="*50)
    
    test_agent_initialization()
    test_agent_response()
    
    print("="*50)
    print("모든 테스트 통과!")
    print("="*50 + "\n")

if __name__ == '__main__':
    run_all_tests()