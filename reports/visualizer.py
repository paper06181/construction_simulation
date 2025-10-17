"""
텍스트 기반 시각화
"""

class TextVisualizer:
    """텍스트 기반 차트 생성기"""
    
    @staticmethod
    def create_bar_chart(data, title="", max_width=50):
        """
        텍스트 막대 그래프
        
        Args:
            data: {'label': value} 형태의 딕셔너리
            title: 제목
            max_width: 최대 막대 길이
        """
        if not data:
            return ""
        
        max_value = max(data.values()) if data else 1
        
        chart = f"\n{title}\n"
        chart += "=" * (max_width + 20) + "\n"
        
        for label, value in data.items():
            bar_length = int((value / max_value) * max_width) if max_value > 0 else 0
            bar = "█" * bar_length
            chart += f"{label:15} | {bar} {value:.2f}\n"
        
        chart += "=" * (max_width + 20) + "\n"
        
        return chart
    
    @staticmethod
    def create_comparison_chart(data_off, data_on, title="", max_width=40):
        """
        비교 막대 그래프
        
        Args:
            data_off: BIM OFF 데이터
            data_on: BIM ON 데이터
            title: 제목
            max_width: 최대 막대 길이
        """
        chart = f"\n{title}\n"
        chart += "=" * (max_width * 2 + 30) + "\n"
        
        all_labels = set(list(data_off.keys()) + list(data_on.keys()))
        max_value = max(list(data_off.values()) + list(data_on.values())) if all_labels else 1
        
        for label in sorted(all_labels):
            value_off = data_off.get(label, 0)
            value_on = data_on.get(label, 0)
            
            bar_off_length = int((value_off / max_value) * max_width) if max_value > 0 else 0
            bar_on_length = int((value_on / max_value) * max_width) if max_value > 0 else 0
            
            bar_off = "█" * bar_off_length
            bar_on = "█" * bar_on_length
            
            chart += f"{label:12}\n"
            chart += f"  OFF | {bar_off} {value_off:.2f}\n"
            chart += f"  ON  | {bar_on} {value_on:.2f}\n"
            chart += "\n"
        
        chart += "=" * (max_width * 2 + 30) + "\n"
        
        return chart
    
    @staticmethod
    def create_table(headers, rows, title=""):
        """
        텍스트 테이블
        
        Args:
            headers: 헤더 리스트
            rows: 행 데이터 리스트 (각 행은 리스트)
            title: 제목
        """
        if not headers or not rows:
            return ""
        
        col_widths = [max(len(str(h)), max(len(str(row[i])) for row in rows)) + 2 
                      for i, h in enumerate(headers)]
        
        table = f"\n{title}\n" if title else "\n"
        table += "=" * (sum(col_widths) + len(headers) + 1) + "\n"
        
        header_row = "|".join(str(h).center(col_widths[i]) for i, h in enumerate(headers))
        table += f"{header_row}\n"
        table += "=" * (sum(col_widths) + len(headers) + 1) + "\n"
        
        for row in rows:
            row_str = "|".join(str(cell).center(col_widths[i]) for i, cell in enumerate(row))
            table += f"{row_str}\n"
        
        table += "=" * (sum(col_widths) + len(headers) + 1) + "\n"
        
        return table