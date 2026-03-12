from typing import List, Dict, Any
from .ahp_matrix import validate_pairwise_matrix
from .ahp_weight import calculate_priority_vector
from .ahp_consistency import calculate_lambda_max, calculate_consistency_index, calculate_consistency_ratio

def run_ahp(pairwise_matrix: List[List[float]]) -> Dict[str, Any]:
    """
    File orchestration - Điều phối toàn bộ quá trình tính AHP.
    Dùng để gọi toàn bộ pipeline AHP từ ma trận so sánh cặp đầu vào.
    
    Trả về Dictionary chứa trọng số, λmax, CI, CR, và độ nhất quán.
    """
    # 1. Kiểm tra tính hợp lệ của ma trận
    if not validate_pairwise_matrix(pairwise_matrix):
        raise ValueError("Ma trận so sánh cặp không hợp lệ. Phải là ma trận vuông, phần tử đường chéo bằng 1, và a[i][j] = 1 / a[j][i], a[i][j] > 0.")
        
    n = len(pairwise_matrix)
    
    # 2. Tính trọng số (priority vector)
    weights = calculate_priority_vector(pairwise_matrix)
    
    # Nếu chỉ có 1 hoặc 2 tiêu chí thì ma trận luôn hợp lệ và nhất quán
    if n <= 2:
        return {
            "weights": weights,
            "lambda_max": float(n),
            "CI": 0.0,
            "CR": 0.0,
            "is_consistent": True
        }
    
    # 3. Tính độ nhất quán
    lambda_max = calculate_lambda_max(pairwise_matrix, weights)
    ci = calculate_consistency_index(lambda_max, n)
    cr = calculate_consistency_ratio(ci, n)
    
    # Kiểm tra tỷ số nhất quán CR < 0.1
    is_consistent = cr < 0.1
    
    return {
        "weights": weights,
        "lambda_max": lambda_max,
        "CI": ci,
        "CR": cr,
        "is_consistent": is_consistent
    }
