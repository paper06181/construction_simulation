"""
수학적 계산 함수
"""

import math

def sigmoid(x, k=10, x0=0.5):
    """
    Sigmoid 함수
    
    Args:
        x: 입력값 (0~1)
        k: 기울기 (클수록 가파름)
        x0: 변곡점
    
    Returns:
        sigmoid 값 (0~1)
    """
    try:
        return 1 / (1 + math.exp(-k * (x - x0)))
    except OverflowError:
        return 0.0 if x < x0 else 1.0

def normalize_value(value, min_val, max_val):
    """
    값을 0~1 범위로 정규화
    
    Args:
        value: 정규화할 값
        min_val: 최소값
        max_val: 최대값
    
    Returns:
        정규화된 값 (0~1)
    """
    if max_val == min_val:
        return 0.5
    
    normalized = (value - min_val) / (max_val - min_val)
    return max(0, min(1, normalized))

def calculate_weighted_average(values, weights):
    """
    가중 평균 계산
    
    Args:
        values: 값 딕셔너리 {'key': value}
        weights: 가중치 딕셔너리 {'key': weight}
    
    Returns:
        가중 평균
    """
    if not values or not weights:
        return 0.0
    
    total = sum(values.get(k, 0) * weights.get(k, 0) for k in weights)
    weight_sum = sum(weights.values())
    
    return total / weight_sum if weight_sum > 0 else 0.0

def calculate_percentage_change(original, new):
    """
    변화율 계산
    
    Args:
        original: 원래 값
        new: 새로운 값
    
    Returns:
        변화율 (%)
    """
    if original == 0:
        return 0.0
    
    return ((new - original) / original) * 100