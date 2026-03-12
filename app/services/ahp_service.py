from typing import List, Dict
from fastapi import HTTPException

from app.utils.ahp_matrix import validate_pairwise_matrix, sum_columns, normalize_matrix
from app.utils.ahp_weight import calculate_priority_vector
from app.utils.ahp_consistency import calculate_lambda_max, calculate_consistency_index, calculate_consistency_ratio

# ─────────────────────────────────────────────
# Step 1: Validate + Tính tổng cột
# ─────────────────────────────────────────────

def step_column_sum(matrix: List[List[float]]) -> List[float]:
    """
    Kiểm tra tính hợp lệ của ma trận so sánh cặp và tính tổng từng cột.
    Ném lỗi HTTP 400 nếu ma trận không hợp lệ.
    """
    # Kiểm tra ma trận không rỗng và là ma trận vuông
    n = len(matrix)
    for row in matrix:
        if len(row) != n:
            raise HTTPException(status_code=400, detail="Ma trận phải là ma trận vuông (n x n).")
        for val in row:
            if val <= 0:
                raise HTTPException(status_code=400, detail="Tất cả giá trị trong ma trận phải lớn hơn 0.")

    return sum_columns(matrix)


# ─────────────────────────────────────────────
# Step 2: Chuẩn hóa ma trận
# ─────────────────────────────────────────────

def step_normalize(matrix: List[List[float]], column_sums: List[float]) -> List[List[float]]:
    """
    Chuẩn hóa ma trận bằng cách chia mỗi phần tử cho tổng cột tương ứng.
    Ném lỗi HTTP 400 nếu tổng cột bằng 0.
    """
    for s in column_sums:
        if s == 0:
            raise HTTPException(status_code=400, detail="Tổng cột không được bằng 0 (lỗi chia cho 0).")

    n = len(matrix)
    normalized = [[0.0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            normalized[i][j] = matrix[i][j] / column_sums[j]

    return normalized


# ─────────────────────────────────────────────
# Step 3: Tính vector trọng số (Priority Vector)
# ─────────────────────────────────────────────

def step_weights(normalized_matrix: List[List[float]]) -> List[float]:
    """
    Tính vector trọng số bằng cách lấy trung bình từng hàng của ma trận chuẩn hóa.
    """
    n = len(normalized_matrix)
    weights = [sum(row) / n for row in normalized_matrix]
    return weights


# ─────────────────────────────────────────────
# Step 4: Kiểm tra Consistency
# ─────────────────────────────────────────────

def step_consistency(matrix: List[List[float]], weights: List[float]) -> Dict:
    """
    Tính λmax, CI, CR và kiểm tra tính nhất quán của ma trận.
    Trả về dict chứa lambda_max, CI, CR, is_consistent.
    """
    n = len(matrix)
    lambda_max = calculate_lambda_max(matrix, weights)
    ci = calculate_consistency_index(lambda_max, n)
    cr = calculate_consistency_ratio(ci, n)
    is_consistent = cr < 0.1

    return {
        "lambda_max": lambda_max,
        "CI": ci,
        "CR": cr,
        "is_consistent": is_consistent
    }


# ─────────────────────────────────────────────
# Step 5: Xếp hạng phương án
# ─────────────────────────────────────────────

def step_rank(
    criteria_weights: List[float],
    alternative_scores: List[List[float]],
    names: List[str]
) -> List[Dict]:
    """
    Tổng hợp điểm và xếp hạng các phương án theo điểm AHP giảm dần.
    """
    results = []
    for i, scores in enumerate(alternative_scores):
        if len(scores) != len(criteria_weights):
            raise HTTPException(
                status_code=400,
                detail=f"Phương án #{i+1} có số tiêu chí ({len(scores)}) không khớp với số trọng số ({len(criteria_weights)})."
            )
        # Tính tổng điểm có trọng số
        total = sum(w * s for w, s in zip(criteria_weights, scores))
        results.append({"name": names[i], "score": round(total, 4)})

    # Sắp xếp giảm dần theo điểm
    results.sort(key=lambda x: x["score"], reverse=True)
    return results
