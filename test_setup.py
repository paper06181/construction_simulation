"""
설치 및 설정 테스트 스크립트
"""

import sys
import os

def test_imports():
    """필수 모듈 import 테스트"""
    print("=" * 60)
    print("1. 모듈 Import 테스트")
    print("=" * 60)

    try:
        from models.project import Project
        print("[OK] models.project")
    except Exception as e:
        print(f"✗ models.project: {e}")
        return False

    try:
        from models.bim_quality import BIMQuality
        print("✓ models.bim_quality")
    except Exception as e:
        print(f"✗ models.bim_quality: {e}")
        return False

    try:
        from config.bim_quality_config import BIMQualityConfig
        print("✓ config.bim_quality_config")
    except Exception as e:
        print(f"✗ config.bim_quality_config: {e}")
        return False

    try:
        from agents.owner_agent import OwnerAgent
        print("✓ agents.owner_agent")
    except Exception as e:
        print(f"✗ agents.owner_agent: {e}")
        return False

    try:
        from agents.designer_agent import DesignerAgent
        print("✓ agents.designer_agent")
    except Exception as e:
        print(f"✗ agents.designer_agent: {e}")
        return False

    try:
        from simulation.simulation_engine import SimulationEngine
        print("✓ simulation.simulation_engine")
    except Exception as e:
        print(f"✗ simulation.simulation_engine: {e}")
        return False

    print("\n모든 모듈 import 성공!\n")
    return True


def test_llm_setup():
    """LLM 설정 테스트"""
    print("=" * 60)
    print("2. LLM 설정 테스트")
    print("=" * 60)

    # .env 파일 확인
    if os.path.exists('.env'):
        print("✓ .env 파일 존재")
    else:
        print("✗ .env 파일 없음")
        print("  → .env.example을 복사하여 .env 파일을 생성하세요")
        print("  → cp .env.example .env")
        return False

    # 환경 변수 확인
    from dotenv import load_dotenv
    load_dotenv()

    api_key = os.getenv('OPENAI_API_KEY')
    if api_key and api_key != 'your_api_key_here':
        print(f"✓ OPENAI_API_KEY 설정됨 (sk-...{api_key[-4:]})")
    else:
        print("✗ OPENAI_API_KEY 미설정")
        print("  → .env 파일에 실제 API 키를 입력하세요")
        return False

    model = os.getenv('OPENAI_MODEL', 'gpt-4o-mini')
    print(f"✓ OPENAI_MODEL: {model}")

    print("\nLLM 설정 완료!\n")
    return True


def test_agent_creation():
    """에이전트 생성 테스트"""
    print("=" * 60)
    print("3. 에이전트 생성 테스트")
    print("=" * 60)

    try:
        from agents.owner_agent import OwnerAgent
        from agents.designer_agent import DesignerAgent
        from agents.contractor_agent import ContractorAgent
        from agents.supervisor_agent import SupervisorAgent
        from agents.bank_agent import BankAgent

        # LLM 없이 테스트 (빠름)
        agents = {
            'owner': OwnerAgent(use_llm=False),
            'designer': DesignerAgent(use_llm=False),
            'contractor': ContractorAgent(use_llm=False),
            'supervisor': SupervisorAgent(use_llm=False),
            'bank': BankAgent(use_llm=False)
        }

        print("✓ 건축주 에이전트")
        print("✓ 설계사 에이전트")
        print("✓ 시공사 에이전트")
        print("✓ 감리사 에이전트")
        print("✓ 금융사 에이전트")

        print("\n모든 에이전트 생성 성공!\n")
        return True

    except Exception as e:
        print(f"✗ 에이전트 생성 실패: {e}")
        return False


def test_llm_agent():
    """LLM 에이전트 테스트"""
    print("=" * 60)
    print("4. LLM 에이전트 테스트 (선택)")
    print("=" * 60)

    if not os.path.exists('.env'):
        print("⊘ .env 파일 없음 - 테스트 건너뜀")
        return True

    from dotenv import load_dotenv
    load_dotenv()

    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key or api_key == 'your_api_key_here':
        print("⊘ API 키 미설정 - 테스트 건너뜀")
        return True

    try:
        from agents.owner_agent import OwnerAgent
        from models.project import Project

        print("LLM 에이전트 생성 중...")
        owner = OwnerAgent(use_llm=True)

        if not owner.use_llm:
            print("✗ LLM 초기화 실패")
            return False

        print("✓ LLM 에이전트 생성 성공")

        # 간단한 응답 테스트
        print("\n간단한 응답 테스트 (이슈 정보 생성)...")
        project = Project(bim_enabled=False)
        test_issue = {
            'id': 'TEST-01',
            'name': '테스트 이슈',
            'category': '설계',
            'severity': 'S2',
            'description': '테스트를 위한 가상 이슈입니다.'
        }

        response = owner._initial_response(test_issue, project)
        print(f"\n건축주 응답:\n{response}\n")

        if response and response.startswith('[건축주]'):
            print("✓ LLM 응답 생성 성공\n")
            return True
        else:
            print("⚠ LLM 응답 형식 확인 필요\n")
            return True

    except Exception as e:
        print(f"✗ LLM 테스트 실패: {e}\n")
        import traceback
        traceback.print_exc()
        return False


def main():
    """메인 테스트 함수"""
    print("\n")
    print("=" * 60)
    print("  BIM 건설 시뮬레이션 - 설정 테스트")
    print("=" * 60)
    print("\n")

    results = []

    # 1. Import 테스트
    results.append(("모듈 Import", test_imports()))

    # 2. LLM 설정 테스트
    results.append(("LLM 설정", test_llm_setup()))

    # 3. 에이전트 생성 테스트
    results.append(("에이전트 생성", test_agent_creation()))

    # 4. LLM 에이전트 테스트
    results.append(("LLM 에이전트", test_llm_agent()))

    # 결과 출력
    print("=" * 60)
    print("테스트 결과 요약")
    print("=" * 60)

    all_passed = True
    for test_name, result in results:
        status = "✓ 통과" if result else "✗ 실패"
        print(f"{test_name:20s} : {status}")
        if not result:
            all_passed = False

    print("=" * 60)

    if all_passed:
        print("\n[SUCCESS] 모든 테스트 통과!")
        print("\n다음 명령으로 시뮬레이션을 실행하세요:")
        print("  python main.py --scenario compare\n")
        return 0
    else:
        print("\n[WARNING] 일부 테스트 실패")
        print("위 오류 메시지를 확인하고 수정해주세요.\n")
        return 1


if __name__ == '__main__':
    exit_code = main()
    sys.exit(exit_code)
