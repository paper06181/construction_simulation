"""
에이전트 회의 조율
"""

from pathlib import Path

class MeetingCoordinator:
    """에이전트 회의 진행"""

    def __init__(self, agents, save_meetings=True, bim_status=""):
        """
        Args:
            agents: 에이전트 딕셔너리 {'owner': OwnerAgent, ...}
            save_meetings: 회의록 자동 저장 여부
            bim_status: "BIM_ON" 또는 "BIM_OFF"
        """
        self.agents = agents
        self.meeting_log = []
        self.conversation_context = []  # 대화 컨텍스트 공유용
        self.save_meetings = save_meetings
        self.bim_status = bim_status
        self.all_meetings_content = []  # 전체 회의록 내용 저장

        # 회의록 저장 폴더 생성
        if self.save_meetings:
            self.meetings_dir = Path("output/meetings")
            self.meetings_dir.mkdir(parents=True, exist_ok=True)
    
    def conduct_meeting(self, issue, project, impact_result=None):
        """회의 진행"""
        meeting_record = {
            'issue_id': issue['id'],
            'issue_name': issue['name'],
            'day': project.current_day,
            'phase': project.current_phase,
            'conversations': []
        }
        
        if impact_result is None:
            meeting_record['conversations'] = self._initial_discussion(issue, project)
        else:
            meeting_record['conversations'] = self._decision_meeting(issue, project, impact_result)
        
        self.meeting_log.append(meeting_record)

        # 회의록 저장
        if self.save_meetings:
            self._save_meeting_to_file(meeting_record, impact_result)

        return meeting_record
    
    def _initial_discussion(self, issue, project):
        """초기 논의 (문제 인식 단계)"""
        conversations = []

        # 대화 컨텍스트 초기화
        self.conversation_context = []

        # 시공사 → 설계사 → 감리사 → 건축주 → 금융사 순서
        contractor_msg = self.agents['contractor'].respond(issue, project, None)
        conversations.append(contractor_msg)
        self.conversation_context.append({"speaker": "시공사", "message": contractor_msg})

        designer_msg = self.agents['designer'].respond(issue, project, None)
        conversations.append(designer_msg)
        self.conversation_context.append({"speaker": "설계사", "message": designer_msg})

        supervisor_msg = self.agents['supervisor'].respond(issue, project, None)
        conversations.append(supervisor_msg)
        self.conversation_context.append({"speaker": "감리사", "message": supervisor_msg})

        owner_msg = self.agents['owner'].respond(issue, project, None)
        conversations.append(owner_msg)
        self.conversation_context.append({"speaker": "건축주", "message": owner_msg})

        bank_msg = self.agents['bank'].respond(issue, project, None)
        conversations.append(bank_msg)
        self.conversation_context.append({"speaker": "금융사", "message": bank_msg})

        return conversations
    
    def _decision_meeting(self, issue, project, impact_result):
        """의사결정 회의 (해결 방안 단계)"""
        conversations = []

        # 이전 회의 컨텍스트 유지 (초기 논의 내용)
        # 설계사 → 시공사 → 감리사 → 금융사 → 건축주 순서

        designer_msg = self.agents['designer'].respond(issue, project, impact_result)
        conversations.append(designer_msg)
        self.conversation_context.append({"speaker": "설계사", "message": designer_msg})

        contractor_msg = self.agents['contractor'].respond(issue, project, impact_result)
        conversations.append(contractor_msg)
        self.conversation_context.append({"speaker": "시공사", "message": contractor_msg})

        supervisor_msg = self.agents['supervisor'].respond(issue, project, impact_result)
        conversations.append(supervisor_msg)
        self.conversation_context.append({"speaker": "감리사", "message": supervisor_msg})

        bank_msg = self.agents['bank'].respond(issue, project, impact_result)
        conversations.append(bank_msg)
        self.conversation_context.append({"speaker": "금융사", "message": bank_msg})

        owner_msg = self.agents['owner'].respond(issue, project, impact_result)
        conversations.append(owner_msg)
        self.conversation_context.append({"speaker": "건축주", "message": owner_msg})

        return conversations
    
    def print_meeting(self, meeting_record):
        """회의록 출력"""
        print(f"\n{'='*60}")
        print(f"회의: {meeting_record['issue_name']} ({meeting_record['issue_id']})")
        print(f"일자: Day {meeting_record['day']} | 단계: {meeting_record['phase']}")
        print(f"{'='*60}")
        
        for conv in meeting_record['conversations']:
            print(conv)
        
        print(f"{'='*60}\n")
    
    def get_meeting_summary(self):
        """전체 회의 요약"""
        return f"총 회의 횟수: {len(self.meeting_log)}건"

    def get_conversation_context(self):
        """현재 대화 컨텍스트 반환"""
        return self.conversation_context

    def format_context_for_prompt(self, max_messages=5):
        """LLM 프롬프트용 컨텍스트 포맷"""
        if not self.conversation_context:
            return ""

        recent_context = self.conversation_context[-max_messages:]
        formatted = "\n\n## 이전 대화 내용\n"
        for ctx in recent_context:
            formatted += f"{ctx['message']}\n"

        return formatted

    def _save_meeting_to_file(self, meeting_record, impact_result):
        """회의록 내용을 메모리에 저장 (나중에 통합 파일로 저장)"""
        issue_id = meeting_record['issue_id']
        meeting_type = "초기 논의" if impact_result is None else "의사결정 회의"

        # 회의록 내용 작성
        content = []
        content.append("\n" + "="*80)
        content.append(f"[이슈 #{len(self.all_meetings_content)//2 + 1}] {meeting_record['issue_name']} ({meeting_record['issue_id']})")
        content.append(f"발생 시점: Day {meeting_record['day']} | 단계: {meeting_record['phase']}")
        content.append(f"회의 유형: {meeting_type}")
        content.append("="*80)

        if impact_result is not None:
            content.append("\n## 영향 분석 결과")
            content.append(f"  - 공기 지연: {impact_result['delay_weeks']:.2f}주 ({impact_result['delay_weeks']*7:.1f}일)")
            content.append(f"  - 비용 증가: {impact_result['cost_increase']:,.0f}원")
            content.append(f"  - 탐지 여부: {'예 (BIM으로 조기 탐지)' if impact_result['detected'] else '아니오 (시공 중 발견)'}")
            if impact_result['detected']:
                content.append(f"  - 탐지 단계: {impact_result['detection_phase']}")
                if impact_result.get('bim_effectiveness'):
                    content.append(f"  - BIM 효과성: {impact_result['bim_effectiveness']:.2f}")

            # 협상 결과 추가
            if impact_result.get('negotiation_summary'):
                content.append("\n## 협상 결과")
                content.append(f"  {impact_result['negotiation_summary']}")

        content.append("\n## 회의 내용")
        for conv in meeting_record['conversations']:
            content.append(conv)

        content.append("\n" + "-"*80)

        # 메모리에 저장
        self.all_meetings_content.append('\n'.join(content))

    def save_all_meetings_to_file(self, project_name=""):
        """시뮬레이션 종료 시 모든 회의록을 하나의 파일로 저장"""
        if not self.save_meetings or not self.all_meetings_content:
            return None

        from datetime import datetime
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"meetings_{self.bim_status}_{timestamp}.txt"
        filepath = self.meetings_dir / filename

        # 헤더 작성
        header = []
        header.append("="*80)
        header.append(f"회의록 통합 문서")
        header.append(f"프로젝트: {project_name}")
        header.append(f"BIM 적용: {self.bim_status}")
        header.append(f"생성 일시: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        header.append(f"총 회의 건수: {len(self.meeting_log)}건")
        header.append("="*80)

        # 전체 내용 결합
        full_content = '\n'.join(header) + '\n' + '\n'.join(self.all_meetings_content)

        # 푸터 작성
        footer = []
        footer.append("\n" + "="*80)
        footer.append("회의록 통합 문서 종료")
        footer.append(f"총 이슈 수: {len(self.meeting_log)//2}건")
        footer.append(f"총 회의 수: {len(self.meeting_log)}건 (초기 논의 + 의사결정)")
        footer.append("="*80)

        full_content += '\n'.join(footer)

        # 파일 저장
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(full_content)

        print(f"[회의록 저장] {filepath}")
        return filepath