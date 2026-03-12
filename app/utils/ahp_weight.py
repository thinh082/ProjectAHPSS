from typing import List
from .ahp_matrix import normalize_matrix

def calculate_priority_vector(matrix: List[List[float]]) -> List[float]:
    """
    Tính vector trọng số (priority vector) tiêu chí từ ma trận so sánh cặp.
    - Bước 1: Chuẩn hóa ma trận (chia mỗi phần tử cho tổng cột tương ứng).
    - Bước 2: Tính trung bình cộng của mỗi dòng trên ma trận đã chuẩn hóa.
    """
    if not matrix:
        return []
        
    normalized_matrix = normalize_matrix(matrix)
    n = len(normalized_matrix)
    weights = []
    
    # Tính trung bình cộng cho từng dòng
    for i in range(n):
        row_avg = sum(normalized_matrix[i]) / n
        weights.append(row_avg)
        
    return weights
