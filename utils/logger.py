"""
시뮬레이션 로깅
"""

import json
from datetime import datetime

class SimulationLogger:
    """시뮬레이션 로거"""
    
    def __init__(self, output_dir='output'):
        """
        Args:
            output_dir: 출력 디렉토리
        """
        self.output_dir = output_dir
        self.logs = []
    
    def log_event(self, event_type, data):
        """이벤트 로깅"""
        log_entry = {
            'timestamp': datetime.now().isoformat(),
            'event_type': event_type,
            'data': data
        }
        self.logs.append(log_entry)
    
    def save_logs(self, filename=None):
        """로그 파일 저장"""
        if filename is None:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f'simulation_log_{timestamp}.json'
        
        filepath = f"{self.output_dir}/{filename}"
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(self.logs, f, ensure_ascii=False, indent=2)
        
        print(f"로그 저장됨: {filepath}")
    
    def print_summary(self):
        """로그 요약 출력"""
        event_counts = {}
        for log in self.logs:
            event_type = log['event_type']
            event_counts[event_type] = event_counts.get(event_type, 0) + 1
        
        print(f"\n{'='*60}")
        print("로그 요약")
        print(f"{'='*60}")
        print(f"총 이벤트: {len(self.logs)}건")
        for event_type, count in event_counts.items():
            print(f"  {event_type}: {count}건")
        print(f"{'='*60}\n")