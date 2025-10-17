"""
빠른 데모 실행 (LLM 비활성화)
"""

from models.project import Project
from agents.owner_agent import OwnerAgent
from agents.designer_agent import DesignerAgent
from agents.contractor_agent import ContractorAgent
from agents.supervisor_agent import SupervisorAgent
from agents.bank_agent import BankAgent
from simulation.simulation_engine import SimulationEngine
from reports.report_generator import ReportGenerator
from reports.graph_visualizer import GraphVisualizer

print("\n" + "="*70)
print("BIM 시뮬레이션 빠른 데모 (LLM 비활성화)")
print("="*70 + "\n")

# 에이전트 생성 (LLM 비활성화)
print("에이전트 생성 중...")
agents = {
    'owner': OwnerAgent(use_llm=False),
    'designer': DesignerAgent(use_llm=False),
    'contractor': ContractorAgent(use_llm=False),
    'supervisor': SupervisorAgent(use_llm=False),
    'bank': BankAgent(use_llm=False)
}
print("✓ 5개 에이전트 생성 완료\n")

# BIM OFF 시나리오
print("="*70)
print("1단계: BIM OFF 시나리오 실행")
print("="*70)
project_off = Project(bim_enabled=False)
engine_off = SimulationEngine(project_off, agents)
metrics_off = engine_off.run(verbose=False)
print("✓ BIM OFF 시뮬레이션 완료\n")

# BIM ON 시나리오
print("="*70)
print("2단계: BIM ON 시나리오 실행")
print("="*70)
from config.bim_quality_config import BIMQualityConfig
project_on = Project(bim_enabled=True, bim_quality=BIMQualityConfig.BIM_GOOD)
engine_on = SimulationEngine(project_on, agents)
metrics_on = engine_on.run(verbose=False)
print("✓ BIM ON 시뮬레이션 완료\n")

# 결과 비교
print("="*70)
print("3단계: 결과 비교")
print("="*70)
report = ReportGenerator.generate_comparison_report(metrics_off, metrics_on)
print(report)

# 그래프 생성
print("\n" + "="*70)
print("4단계: 그래프 생성")
print("="*70)
try:
    viz = GraphVisualizer()
    paths = viz.generate_all_graphs(metrics_off, metrics_on)
    print(f"\n생성된 그래프 파일:")
    for path in paths:
        print(f"  - {path}")
except Exception as e:
    print(f"그래프 생성 중 오류: {e}")

print("\n" + "="*70)
print("데모 완료!")
print("="*70)
print("\n💡 LLM을 활성화하려면 다음 명령을 사용하세요:")
print("   python main.py --scenario compare")
