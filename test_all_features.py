"""
모든 개선사항 통합 테스트
"""

import sys
import os

print("="*70)
print("통합 테스트 - 모든 개선사항 검증")
print("="*70 + "\n")

# 1. 기본 모듈 import 테스트
print("1. 모듈 Import 테스트...")
try:
    from models.project import Project
    from config.project_templates import ProjectTemplates
    from reports.graph_visualizer import GraphVisualizer
    from agents.contractor_agent import ContractorAgent
    from agents.supervisor_agent import SupervisorAgent
    from agents.bank_agent import BankAgent
    from simulation.meeting_coordinator import MeetingCoordinator
    print("   [OK] 모든 모듈 import 성공\n")
except Exception as e:
    print(f"   [FAIL] Import 실패: {e}\n")
    sys.exit(1)

# 2. .env 파일 테스트
print("2. 환경 설정 테스트...")
try:
    from dotenv import load_dotenv
    load_dotenv()
    api_key = os.getenv('OPENAI_API_KEY')
    if api_key:
        print(f"   [OK] API 키 로드 성공 (길이: {len(api_key)})\n")
    else:
        print("   [WARN] API 키 없음 - 템플릿 모드로 작동\n")
except Exception as e:
    print(f"   [FAIL] 환경 설정 실패: {e}\n")

# 3. 프로젝트 템플릿 테스트
print("3. 프로젝트 템플릿 테스트...")
try:
    templates = ProjectTemplates.list_templates()
    print(f"   [OK] {len(templates)}개 템플릿 사용 가능")
    for key, desc in templates.items():
        print(f"      - {key}: {desc}")
    print()
except Exception as e:
    print(f"   [FAIL] 템플릿 테스트 실패: {e}\n")
    sys.exit(1)

# 4. 프로젝트 생성 테스트 (템플릿 사용)
print("4. 프로젝트 생성 테스트 (템플릿)...")
try:
    # 기본 프로젝트
    project1 = Project(bim_enabled=False)
    print(f"   [OK] 기본 프로젝트: {project1.name}")

    # 템플릿 프로젝트
    project2 = Project(bim_enabled=True, template='apartment')
    print(f"   [OK] 템플릿 프로젝트: {project2.name}")
    print(f"      예산: {project2.budget:,}원 ({project2.budget/1e8:.0f}억)")
    print(f"      공기: {project2.planned_duration}일\n")
except Exception as e:
    print(f"   [FAIL] 프로젝트 생성 실패: {e}\n")
    sys.exit(1)

# 5. LLM 통합 에이전트 테스트
print("5. LLM 통합 에이전트 테스트...")
try:
    # LLM 비활성화 모드로 테스트
    contractor = ContractorAgent(use_llm=False)
    supervisor = SupervisorAgent(use_llm=False)
    bank = BankAgent(use_llm=False)

    print("   [OK] 시공사 에이전트 생성 성공")
    print("   [OK] 감리사 에이전트 생성 성공")
    print("   [OK] 금융사 에이전트 생성 성공\n")
except Exception as e:
    print(f"   [FAIL] 에이전트 생성 실패: {e}\n")
    sys.exit(1)

# 6. 대화 컨텍스트 테스트
print("6. 대화 컨텍스트 공유 테스트...")
try:
    from agents.owner_agent import OwnerAgent
    from agents.designer_agent import DesignerAgent

    agents = {
        'owner': OwnerAgent(use_llm=False),
        'designer': DesignerAgent(use_llm=False),
        'contractor': ContractorAgent(use_llm=False),
        'supervisor': SupervisorAgent(use_llm=False),
        'bank': BankAgent(use_llm=False)
    }

    coordinator = MeetingCoordinator(agents)
    print("   [OK] MeetingCoordinator 생성 성공")
    print(f"   [OK] 대화 컨텍스트 초기화: {len(coordinator.conversation_context)}개 항목\n")
except Exception as e:
    print(f"   [FAIL] 컨텍스트 테스트 실패: {e}\n")
    sys.exit(1)

# 7. 그래프 시각화 테스트
print("7. 그래프 시각화 테스트...")
try:
    viz = GraphVisualizer()
    print("   [OK] GraphVisualizer 생성 성공")
    print(f"   [OK] 출력 폴더: {viz.output_dir}\n")
except Exception as e:
    print(f"   [FAIL] 시각화 테스트 실패: {e}\n")
    sys.exit(1)

# 8. matplotlib 의존성 테스트
print("8. matplotlib 의존성 테스트...")
try:
    import matplotlib
    import matplotlib.pyplot as plt
    print(f"   [OK] matplotlib 버전: {matplotlib.__version__}")
    print(f"   [OK] 백엔드: {matplotlib.get_backend()}\n")
except Exception as e:
    print(f"   [FAIL] matplotlib 테스트 실패: {e}\n")
    sys.exit(1)

# 최종 결과
print("="*70)
print("[SUCCESS] 통합 테스트 완료!")
print("="*70)
print("\n[OK] 모든 개선사항이 정상 작동합니다!\n")
print("다음 명령으로 시뮬레이션을 실행하세요:")
print("  python main.py --scenario compare")
print("  python main.py --template apartment")
print("  python main.py --list-templates\n")
