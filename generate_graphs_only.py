"""
결과 데이터로 그래프만 생성
"""

from reports.graph_visualizer import GraphVisualizer

# 시뮬레이션 결과 (방금 실행된 결과)
metrics_off = {
    'planned_duration': 360,
    'actual_duration': 1398.1,
    'delay_days': 1038.1,
    'delay_weeks': 148.3,
    'schedule_delay_rate': 2.883,
    'planned_budget': 2030000000,
    'actual_cost': 5560000000,
    'cost_increase': 3530000000,
    'budget_overrun_rate': 1.738,
    'direct_cost_increase': 1419000000,
    'financial_cost': 2110000000,
    'issues_count': 27,
    'detected_count': 0,
    'missed_count': 27,
    'detection_rate': 0.0,
    'rfi_count': 0,
    'rework_count': 0,
    'final_interest_rate': 0.057
}

metrics_on = {
    'planned_duration': 360,
    'actual_duration': 595.3,
    'delay_days': 235.3,
    'delay_weeks': 33.6,
    'schedule_delay_rate': 0.654,
    'planned_budget': 2030000000,
    'actual_cost': 2840000000,
    'cost_increase': 810000000,
    'budget_overrun_rate': 0.398,
    'direct_cost_increase': 330000000,
    'financial_cost': 478000000,
    'issues_count': 27,
    'detected_count': 20,
    'missed_count': 7,
    'detection_rate': 0.741,
    'rfi_count': 0,
    'rework_count': 0,
    'final_interest_rate': 0.057
}

print("\n" + "="*70)
print("그래프 생성 중...")
print("="*70)

viz = GraphVisualizer()
paths = viz.generate_all_graphs(metrics_off, metrics_on, bim_cost=50000000)

print("\n" + "="*70)
print("완료! 생성된 그래프:")
print("="*70)
for path in paths:
    print(f"  {path}")
print()
