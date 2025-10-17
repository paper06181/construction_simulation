"""
계산 함수 테스트
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.calculations import sigmoid, normalize_value, calculate_weighted_average

def test_sigmoid():
    """Sigmoid 함수 테스트"""
    print("\n=== Sigmoid 함수 테스트 ===")
    
    test_cases = [0.0, 0.3, 0.5, 0.7, 1.0]
    
    for x in test_cases:
        result = sigmoid(x, k=10, x0=0.5)
        print(f"sigmoid({x}) = {result:.4f}")
    
    assert 0 <= sigmoid(0.5) <= 1, "Sigmoid 결과가 0~1 범위를 벗어남"
    print("✓ Sigmoid 테스트 통과\n")

def test_normalize_value():
    """정규화 함수 테스트"""
    print("=== 정규화 함수 테스트 ===")
    
    result = normalize_value(5, 0, 10)
    print(f"normalize_value(5, 0, 10) = {result}")
    assert result == 0.5, "정규화 오류"
    
    result = normalize_value(0, 0, 10)
    print(f"normalize_value(0, 0, 10) = {result}")
    assert result == 0.0, "정규화 오류"
    
    result = normalize_value(10, 0, 10)
    print(f"normalize_value(10, 0, 10) = {result}")
    assert result == 1.0, "정규화 오류"
    
    print("✓ 정규화 테스트 통과\n")

def test_weighted_average():
    """가중 평균 테스트"""
    print("=== 가중 평균 테스트 ===")
    
    values = {'A': 0.8, 'B': 0.6, 'C': 0.9}
    weights = {'A': 0.3, 'B': 0.5, 'C': 0.2}
    
    result = calculate_weighted_average(values, weights)
    expected = 0.8 * 0.3 + 0.6 * 0.5 + 0.9 * 0.2
    
    print(f"가중 평균 = {result:.4f}")
    print(f"예상값 = {expected:.4f}")
    
    assert abs(result - expected) < 0.001, "가중 평균 계산 오류"
    print("✓ 가중 평균 테스트 통과\n")

def run_all_tests():
    """모든 테스트 실행"""
    print("\n" + "="*50)
    print("계산 함수 테스트 시작")
    print("="*50)
    
    test_sigmoid()
    test_normalize_value()
    test_weighted_average()
    
    print("="*50)
    print("모든 테스트 통과!")
    print("="*50 + "\n")

if __name__ == '__main__':
    run_all_tests()