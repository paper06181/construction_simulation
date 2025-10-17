# -*- coding: utf-8 -*-
"""
간단한 설정 테스트
"""

print("\n" + "="*60)
print("BIM 시뮬레이션 - 빠른 테스트")
print("="*60 + "\n")

# 1. Import 테스트
print("1. 모듈 Import...")
try:
    from models.project import Project
    from models.bim_quality import BIMQuality
    from config.bim_quality_config import BIMQualityConfig
    from agents.owner_agent import OwnerAgent
    from agents.designer_agent import DesignerAgent
    print("[OK] 모든 모듈 import 성공\n")
except Exception as e:
    print(f"[ERROR] Import 실패: {e}\n")
    exit(1)

# 2. .env 파일 확인
print("2. 환경 설정...")
import os
if os.path.exists('.env'):
    print("[OK] .env 파일 존재")
    from dotenv import load_dotenv
    load_dotenv()

    api_key = os.getenv('OPENAI_API_KEY')
    if api_key and api_key != 'your_api_key_here':
        print(f"[OK] API 키 설정됨")
    else:
        print("[WARNING] API 키 미설정 - 템플릿 모드로 실행됨")
else:
    print("[WARNING] .env 파일 없음 - 템플릿 모드로 실행됨")
print()

# 3. 에이전트 생성 테스트
print("3. 에이전트 생성...")
try:
    agents = {
        'owner': OwnerAgent(use_llm=False),
        'designer': DesignerAgent(use_llm=False),
    }
    print("[OK] 에이전트 생성 성공\n")
except Exception as e:
    print(f"[ERROR] 에이전트 생성 실패: {e}\n")
    exit(1)

# 4. 프로젝트 생성 테스트
print("4. 프로젝트 생성...")
try:
    project = Project(bim_enabled=False)
    print(f"[OK] 프로젝트: {project.name}")
    print(f"[OK] 예산: {project.budget:,}원\n")
except Exception as e:
    print(f"[ERROR] 프로젝트 생성 실패: {e}\n")
    exit(1)

print("="*60)
print("[SUCCESS] 모든 기본 테스트 통과!")
print("="*60)
print("\n시뮬레이션 실행 명령:")
print("  python main.py --scenario compare\n")
