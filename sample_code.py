import os

def calculate_total(price: int, count: int) -> int:
    """총 가격 계산"""
    total_price = price * count
    if total_price > 10000:
        print("비쌈")
    return total_price