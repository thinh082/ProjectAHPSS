from typing import List

# Bảng Random Index (RI) chuẩn của phương pháp Saaty
RI_TABLE = {
    1: 0.0,
    2: 0.0,
    3: 0.58,
    4: 0.90,
    5: 1.12,
    6: 1.24,
    7: 1.32,
    8: 1.41,
    9: 1.45,
    10: 1.49
}

def calculate_lambda_max(matrix: List[List[float]], weights: List[float]) -> float:
    """
    Tính giá trị riêng lớn nhất (λmax / lambda max).
    Công thức: Trung bình của các tỷ số ((A.W)_i / W_i) trong đó (A.W) là ma trận nhân với vector trọng số.
    """
    if not matrix or not weights:
        return 0.0
        
    n = len(matrix)
    lambda_max = 0.0
    
    for i in range(n):
        # Tính phần tử thứ i của vector A.W
        aw_i = sum(matrix[i][j] * weights[j] for j in range(n))
        
        if weights[i] == 0:
            raise ValueError("Lỗi chia cho 0: Trọng số bằng 0.")
            
        lambda_max += aw_i / weights[i]
        
    return lambda_max / n

def calculate_consistency_index(lambda_max: float, n: int) -> float:
    """
    Tính chỉ số nhất quán (Consistency Index - CI).
    Công thức: CI = (λmax - n) / (n - 1)
    """
    if n <= 1:
        return 0.0
    return (lambda_max - n) / (n - 1)

def calculate_consistency_ratio(ci: float, n: int) -> float:
    """
    Tính tỷ số nhất quán (Consistency Ratio - CR).
    Công thức: CR = CI / RI
    Nếu CR < 0.1 thì ma trận được coi là nhất quán và hợp lệ.
    """
    ri = RI_TABLE.get(n, 1.49) # Nếu n > 10, tạm dùng mức 1.49 của n=10
    
    if ri == 0.0:
        return 0.0 # Với n = 1, 2 thì CR luôn bằng 0
        
    return ci / ri
