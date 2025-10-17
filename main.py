"""
BIM 시뮬레이션 메인 실행 파일
"""

import sys
import argparse
from pathlib import Path
from datetime import datetime
from models.project import Project
from models.bim_quality import BIMQuality
from config.bim_quality_config import BIMQualityConfig
from config.project_templates import ProjectTemplates
from agents.owner_agent import OwnerAgent
from agents.designer_agent import DesignerAgent
from agents.contractor_agent import ContractorAgent
from agents.supervisor_agent import SupervisorAgent
from agents.bank_agent import BankAgent
from simulation.simulation_engine import SimulationEngine
from reports.report_generator import ReportGenerator
from reports.visualizer import TextVisualizer
from reports.graph_visualizer import GraphVisualizer
from utils.validation import ResultValidator

def create_agents():
    """에이전트 생성"""
    return {
        'owner': OwnerAgent(),
        'designer': DesignerAgent(),
        'contractor': ContractorAgent(),
        'supervisor': SupervisorAgent(),
        'bank': BankAgent()
    }

def save_simulation_results(metrics_off, metrics_on, template_name=None):
    """시뮬레이션 결과를 파일로 저장"""
    # 저장 디렉토리 생성
    results_dir = Path("output/results")
    results_dir.mkdir(parents=True, exist_ok=True)

    # 타임스탬프 생성
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    template_suffix = f"_{template_name}" if template_name else ""
    filename = f"comparison_result_{timestamp}{template_suffix}.txt"
    filepath = results_dir / filename

    # 상세 비교 리포트 생성
    content = []
    content.append("╔" + "="*78 + "╗")
    content.append("║" + " "*20 + "BIM 시뮬레이션 비교 결과 리포트" + " "*24 + "║")
    content.append("╚" + "="*78 + "╝")
    content.append("")
    content.append(f"생성 일시: {datetime.now().strftime('%Y년 %m월 %d일 %H:%M:%S')}")
    if template_name:
        content.append(f"프로젝트 템플릿: {template_name}")
    content.append("")

    # ========== 핵심 요약 ==========
    delay_reduction = metrics_off['delay_days'] - metrics_on['delay_days']
    cost_reduction = metrics_off['actual_cost'] - metrics_on['actual_cost']
    detection_improvement = metrics_on['detection_rate'] - metrics_off['detection_rate']

    content.append("┌" + "─"*78 + "┐")
    content.append("│" + " "*28 + "핵심 개선 효과 요약" + " "*30 + "│")
    content.append("├" + "─"*78 + "┤")
    content.append(f"│  1. 공사 기간 단축: {delay_reduction:>3}일 ({delay_reduction/7:>5.1f}주)" + " "*(80-len(f"│  1. 공사 기간 단축: {delay_reduction:>3}일 ({delay_reduction/7:>5.1f}주)")) + "│")
    content.append(f"│  2. 비용 절감: {cost_reduction:>15,}원 ({cost_reduction/100000000:>6.2f}억원)" + " "*(80-len(f"│  2. 비용 절감: {cost_reduction:>15,}원 ({cost_reduction/100000000:>6.2f}억원)")) + "│")
    content.append(f"│  3. 이슈 탐지율 향상: {detection_improvement*100:>5.1f}%p" + " "*(80-len(f"│  3. 이슈 탐지율 향상: {detection_improvement*100:>5.1f}%p")) + "│")

    if metrics_on['actual_cost'] > 0:
        roi = (cost_reduction / metrics_off['actual_cost']) * 100
        content.append(f"│  4. ROI (투자 대비 절감률): {roi:>5.1f}%" + " "*(80-len(f"│  4. ROI (투자 대비 절감률): {roi:>5.1f}%")) + "│")

    content.append("└" + "─"*78 + "┘")
    content.append("")

    # ========== 상세 비교표 ==========
    content.append("┌" + "─"*78 + "┐")
    content.append("│" + " "*30 + "상세 비교표" + " "*36 + "│")
    content.append("├" + "─"*38 + "┬" + "─"*19 + "┬" + "─"*19 + "┤")
    content.append("│ 항목" + " "*34 + "│ BIM OFF (전통)" + " "*4 + "│ BIM ON (적용)" + " "*5 + "│")
    content.append("├" + "─"*38 + "┼" + "─"*19 + "┼" + "─"*19 + "┤")

    # 공사 기간
    content.append(f"│ 총 공사 기간 (일)" + " "*21 + f"│ {metrics_off['actual_duration']:>17.0f} │ {metrics_on['actual_duration']:>17.0f} │")
    content.append(f"│ 계획 대비 지연 (일)" + " "*19 + f"│ {metrics_off['delay_days']:>17.0f} │ {metrics_on['delay_days']:>17.0f} │")
    content.append(f"│ 지연율 (%)" + " "*28 + f"│ {metrics_off['schedule_delay_rate']*100:>16.1f}% │ {metrics_on['schedule_delay_rate']*100:>16.1f}% │")
    content.append("├" + "─"*38 + "┼" + "─"*19 + "┼" + "─"*19 + "┤")

    # 비용
    content.append(f"│ 최종 비용 (원)" + " "*23 + f"│ {metrics_off['actual_cost']:>17,} │ {metrics_on['actual_cost']:>17,} │")
    content.append(f"│ 계획 예산 (원)" + " "*23 + f"│ {metrics_off['planned_budget']:>17,} │ {metrics_on['planned_budget']:>17,} │")
    content.append(f"│ 예산 초과액 (원)" + " "*21 + f"│ {metrics_off['cost_increase']:>17,} │ {metrics_on['cost_increase']:>17,} │")
    content.append(f"│ 예산 초과율 (%)" + " "*23 + f"│ {metrics_off['budget_overrun_rate']*100:>16.1f}% │ {metrics_on['budget_overrun_rate']*100:>16.1f}% │")
    content.append("├" + "─"*38 + "┼" + "─"*19 + "┼" + "─"*19 + "┤")

    # 이슈
    content.append(f"│ 발생 이슈 (건)" + " "*23 + f"│ {metrics_off['issues_count']:>17} │ {metrics_on['issues_count']:>17} │")
    content.append(f"│ 조기 탐지 이슈 (건)" + " "*18 + f"│ {metrics_off['detected_count']:>17} │ {metrics_on['detected_count']:>17} │")
    content.append(f"│ 미탐지 이슈 (건)" + " "*20 + f"│ {metrics_off['missed_count']:>17} │ {metrics_on['missed_count']:>17} │")
    content.append(f"│ 탐지율 (%)" + " "*28 + f"│ {metrics_off['detection_rate']*100:>16.1f}% │ {metrics_on['detection_rate']*100:>16.1f}% │")
    content.append("└" + "─"*38 + "┴" + "─"*19 + "┴" + "─"*19 + "┘")
    content.append("")

    # ========== 결론 및 권고사항 ==========
    content.append("┌" + "─"*78 + "┐")
    content.append("│" + " "*28 + "결론 및 권고사항" + " "*33 + "│")
    content.append("├" + "─"*78 + "┤")

    if delay_reduction > 0:
        content.append("│ ✓ BIM 적용으로 공사 기간이 단축되어 일정 준수에 유리합니다." + " "*26 + "│")

    if cost_reduction > 0:
        cost_reduction_rate = (cost_reduction / metrics_off['actual_cost']) * 100
        content.append(f"│ ✓ 총 비용이 {cost_reduction_rate:.1f}% 절감되어 예산 효율성이 크게 향상되었습니다." + " "*(80-len(f"│ ✓ 총 비용이 {cost_reduction_rate:.1f}% 절감되어 예산 효율성이 크게 향상되었습니다.")) + "│")

    if detection_improvement > 0.2:
        content.append("│ ✓ 이슈 조기 탐지율이 크게 향상되어 품질 관리가 강화되었습니다." + " "*22 + "│")

    content.append("│" + " "*78 + "│")
    content.append("│ [권고] BIM 적용을 통해 시공 품질 및 효율성이 입증되었습니다." + " "*25 + "│")
    content.append("└" + "─"*78 + "┘")
    content.append("")

    # ========== 파일 위치 정보 ==========
    content.append("="*80)
    content.append("출력 파일 위치")
    content.append("="*80)
    content.append(f"  - 비교 결과: {filepath}")
    content.append(f"  - 시뮬레이션 로그: output/logs/")
    content.append(f"  - 회의록: output/meetings/")
    content.append(f"  - 그래프: output/ (delay_comparison.png 등)")
    content.append("="*80)

    # 파일 저장
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write('\n'.join(content))

    print(f"\n[결과 저장] {filepath}")
    return filepath

def run_bim_off_scenario(verbose=True, template=None, random_seed=None):
    """BIM OFF 시나리오 실행"""
    print("\n" + "="*70)
    print("BIM OFF (전통 방식) 시나리오")
    print("="*70 + "\n")

    if template:
        ProjectTemplates.print_template_info(template)

    project = Project(bim_enabled=False, template=template)
    agents = create_agents()

    engine = SimulationEngine(project, agents, random_seed=random_seed)
    metrics = engine.run(verbose=verbose)

    return project, metrics

def run_bim_on_scenario(bim_quality_level='good', verbose=True, template=None, custom_quality=None, random_seed=None):
    """BIM ON 시나리오 실행"""
    print("\n" + "="*70)

    if custom_quality:
        print(f"BIM ON 시나리오 (품질: CUSTOM)")
    else:
        print(f"BIM ON 시나리오 (품질: {bim_quality_level.upper()})")
    print("="*70 + "\n")

    if template:
        ProjectTemplates.print_template_info(template)

    # Custom 품질 또는 프리셋 품질 선택
    if custom_quality:
        bim_quality = custom_quality
    else:
        quality_map = {
            'excellent': BIMQualityConfig.BIM_EXCELLENT,
            'good': BIMQualityConfig.BIM_GOOD,
            'average': BIMQualityConfig.BIM_AVERAGE,
            'poor': BIMQualityConfig.BIM_POOR
        }
        bim_quality = quality_map.get(bim_quality_level, BIMQualityConfig.BIM_GOOD)

    project = Project(bim_enabled=True, bim_quality=bim_quality, template=template)
    agents = create_agents()

    print(f"BIM 품질 설정:")
    print(f"  경고밀도(WD): {bim_quality['warning_density']}")
    print(f"  충돌밀도(CD): {bim_quality['clash_density']}")
    print(f"  속성채움률(AF): {bim_quality['attribute_fill']*100:.0f}%")
    print(f"  Phase연결률(PL): {bim_quality['phase_link']*100:.0f}%")

    quality_score = BIMQuality.get_quality_score(bim_quality)
    quality_level_text = BIMQuality.get_quality_level(bim_quality)
    print(f"  품질 점수: {quality_score:.2f} ({quality_level_text})\n")

    engine = SimulationEngine(project, agents, random_seed=random_seed)
    metrics = engine.run(verbose=verbose)

    return project, metrics

def run_comparison(bim_quality_level='good', verbose=True, template=None, custom_quality=None):
    """BIM ON/OFF 비교 실행"""
    print("\n" + "#"*70)
    print("BIM 적용 효과 비교 시뮬레이션")
    print("#"*70 + "\n")

    # 동일한 이슈 발생을 위한 시드 고정
    COMPARISON_SEED = 42

    print("1단계: BIM OFF 시나리오 실행")
    project_off, metrics_off = run_bim_off_scenario(verbose=verbose, template=template, random_seed=COMPARISON_SEED)

    print("\n2단계: BIM ON 시나리오 실행")
    print("[알림] 동일한 조건에서 BIM 효과만 비교하기 위해 이슈 발생 패턴을 BIM OFF와 동일하게 설정합니다.\n")
    project_on, metrics_on = run_bim_on_scenario(bim_quality_level, verbose=verbose, template=template, custom_quality=custom_quality, random_seed=COMPARISON_SEED)
    
    print("\n3단계: 결과 비교 및 검증")
    print("="*70)
    
    report = ReportGenerator.generate_comparison_report(metrics_off, metrics_on)
    print(report)
    
    validator = ResultValidator()
    
    print("\n[BIM OFF 검증]")
    validation_off = validator.validate_results(metrics_off, 'traditional')
    validator.print_validation_report(validation_off)
    
    print("\n[BIM ON 검증]")
    validation_on = validator.validate_results(metrics_on, 'bim')
    validator.print_validation_report(validation_on)

    # 텍스트 차트는 verbose 모드에서만 출력 (인코딩 이슈 방지)
    if verbose:
        try:
            visualizer = TextVisualizer()

            delay_chart = visualizer.create_comparison_chart(
                {'지연(주)': metrics_off['delay_weeks']},
                {'지연(주)': metrics_on['delay_weeks']},
                title="공사 지연 비교"
            )
            print(delay_chart)

            cost_chart = visualizer.create_comparison_chart(
                {'예산초과율(%)': metrics_off['budget_overrun_rate']*100},
                {'예산초과율(%)': metrics_on['budget_overrun_rate']*100},
                title="예산 초과 비교"
            )
            print(cost_chart)
        except UnicodeEncodeError:
            print("[알림] 텍스트 차트 출력 생략 (인코딩 문제). 그래프는 파일로 저장됩니다.")

    # 그래프 생성
    print("\n4단계: 그래프 생성")
    graph_viz = GraphVisualizer()
    graph_viz.generate_all_graphs(metrics_off, metrics_on)

    # 결과 저장
    print("\n5단계: 결과 저장")
    save_simulation_results(metrics_off, metrics_on, template_name=template)

    return metrics_off, metrics_on

def main():
    """메인 함수"""
    parser = argparse.ArgumentParser(description='BIM 건설 시뮬레이션')
    parser.add_argument(
        '--scenario',
        choices=['off', 'on', 'compare'],
        default='compare',
        help='실행할 시나리오 (off: BIM OFF, on: BIM ON, compare: 비교)'
    )
    parser.add_argument(
        '--quality',
        choices=['excellent', 'good', 'average', 'poor', 'custom'],
        default='good',
        help='BIM 품질 수준 (excellent/good/average/poor/custom)'
    )
    parser.add_argument(
        '--wd',
        type=float,
        help='경고밀도 (Warning Density, 0.0 이상, 낮을수록 좋음)'
    )
    parser.add_argument(
        '--cd',
        type=float,
        help='충돌밀도 (Clash Density, 0.0 이상, 낮을수록 좋음)'
    )
    parser.add_argument(
        '--af',
        type=float,
        help='속성채움률 (Attribute Fill, 0.0~1.0)'
    )
    parser.add_argument(
        '--pl',
        type=float,
        help='Phase연결률 (Phase Link, 0.0~1.0)'
    )
    parser.add_argument(
        '--template',
        choices=['cheongdam', 'officetel', 'apartment', 'commercial', 'office', 'house'],
        default=None,
        help='프로젝트 템플릿 선택'
    )
    parser.add_argument(
        '--list-templates',
        action='store_true',
        help='사용 가능한 템플릿 목록 표시'
    )
    parser.add_argument(
        '--verbose',
        action='store_true',
        default=True,
        help='상세 출력 여부'
    )
    parser.add_argument(
        '--quiet',
        action='store_true',
        help='요약만 출력'
    )

    args = parser.parse_args()

    # 템플릿 목록 표시
    if args.list_templates:
        print("\n사용 가능한 프로젝트 템플릿:")
        print("="*70)
        for key, desc in ProjectTemplates.list_templates().items():
            print(f"  {key:12s}: {desc}")
        print("="*70)
        print("\n사용법: python main.py --template [템플릿명]\n")
        return

    verbose = args.verbose and not args.quiet

    # Custom BIM 품질 설정 처리
    custom_quality = None
    if args.quality == 'custom' or any([args.wd, args.cd, args.af, args.pl]):
        # custom 옵션 또는 개별 값이 하나라도 입력되면
        if not all([args.wd is not None, args.cd is not None, args.af is not None, args.pl is not None]):
            print("\n[오류] --quality custom 사용 시 --wd, --cd, --af, --pl 모두 입력해야 합니다.")
            print("\n예시:")
            print("  python main.py --quality custom --wd 0.5 --cd 0.2 --af 0.95 --pl 0.90")
            print("\n또는 프리셋 사용:")
            print("  python main.py --quality good")
            return

        # 값 범위 검증
        for name, value in [('AF', args.af), ('PL', args.pl)]:
            if not (0.0 <= value <= 1.0):
                print(f"\n[오류] {name} 값은 0.0~1.0 범위여야 합니다. 입력값: {value}")
                return

        # WD, CD는 0 이상이기만 하면 됨 (상한 없음)
        for name, value in [('WD', args.wd), ('CD', args.cd)]:
            if value < 0.0:
                print(f"\n[오류] {name} 값은 0.0 이상이어야 합니다. 입력값: {value}")
                return

        custom_quality = {
            'warning_density': args.wd,
            'clash_density': args.cd,
            'attribute_fill': args.af,
            'phase_link': args.pl
        }
        print(f"\n[알림] 사용자 정의 BIM 품질로 시뮬레이션 실행")
        print(f"  WD: {args.wd}, CD: {args.cd}, AF: {args.af}, PL: {args.pl}")

    if args.scenario == 'off':
        project, metrics = run_bim_off_scenario(verbose=verbose, template=args.template)

        if args.quiet:
            report = ReportGenerator.generate_single_report(metrics, "BIM OFF")
            print(report)

    elif args.scenario == 'on':
        project, metrics = run_bim_on_scenario(args.quality, verbose=verbose, template=args.template, custom_quality=custom_quality)

        if args.quiet:
            report = ReportGenerator.generate_single_report(metrics, f"BIM ON ({args.quality.upper()})")
            print(report)

    elif args.scenario == 'compare':
        metrics_off, metrics_on = run_comparison(args.quality, verbose=verbose, template=args.template, custom_quality=custom_quality)

    print("\n시뮬레이션 완료!")

if __name__ == '__main__':
    main()