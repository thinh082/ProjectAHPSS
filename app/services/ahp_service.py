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


def step_rank_by_criteria(
    alternative_scores: List[List[float]],
    names: List[str],
    criteria_names: List[str],
    top_k: int = 3
) -> List[Dict]:
    """
    Xep hang phuong an theo tung tieu chi, moi tieu chi lay top_k phuong an.
    """
    if not alternative_scores:
        return []

    criteria_count = len(alternative_scores[0])
    for i, scores in enumerate(alternative_scores):
        if len(scores) != criteria_count:
            raise HTTPException(
                status_code=400,
                detail=f"Phuong an #{i+1} co so tieu chi ({len(scores)}) khong dong nhat voi cac phuong an khac ({criteria_count})."
            )

    if len(criteria_names) != criteria_count:
        raise HTTPException(
            status_code=400,
            detail=f"So ten tieu chi ({len(criteria_names)}) khong khop voi so tieu chi ({criteria_count})."
        )

    if len(names) != len(alternative_scores):
        raise HTTPException(
            status_code=400,
            detail=f"So ten phuong an ({len(names)}) khong khop voi so phuong an ({len(alternative_scores)})."
        )

    limit = min(top_k, len(alternative_scores))
    result = []
    for crit_idx, crit_name in enumerate(criteria_names):
        scored = [
            {"name": names[alt_idx], "score": round(scores[crit_idx], 4)}
            for alt_idx, scores in enumerate(alternative_scores)
        ]
        scored.sort(key=lambda x: x["score"], reverse=True)

        top_alternatives = [
            {"rank": rank + 1, "name": item["name"], "score": item["score"]}
            for rank, item in enumerate(scored[:limit])
        ]
        result.append({"criterion": crit_name, "top_alternatives": top_alternatives})

    return result

import re
from typing import Any
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models import SamsungPhone
from app.schemas.ahp_schema import (
    CriteriaEvaluationRequest, CriteriaEvaluationResponse, 
    CriteriaTabResponse, LocationHeader
)

def parse_numeric(val: Any, default: float = 5.0) -> float:
    if val is None: return default
    if isinstance(val, (int, float)): return float(val)
    m = re.search(r"\d+(\.\d+)?", str(val))
    if m:
        return float(m.group())
    return default

def get_ahp_scale(ratio: float) -> int:
    """Quy đổi chênh lệch tỷ lệ sang thang đo Saaty"""
    if ratio < 1:
        ratio = 1 / ratio
    if ratio < 1.1: return 1
    if ratio < 1.3: return 3
    if ratio < 1.5: return 5
    if ratio < 2.0: return 7
    return 9

async def evaluate_criteria(session: AsyncSession, request: CriteriaEvaluationRequest) -> CriteriaEvaluationResponse:
    # 1. Base Query
    query = select(SamsungPhone)
    
    if request.filters:
        if "mau_dien_thoai" in request.filters:
            search_term = request.filters["mau_dien_thoai"]
            query = query.filter(SamsungPhone.mau_dien_thoai.ilike(f"%{search_term}%"))
    
    result = await session.execute(query)
    all_phones = result.scalars().all()
    
    limit = request.filters.get("limit", 1000) if request.filters else 1000
    phones = all_phones[:limit]
    
    n = len(phones)
    
    criteria_def = [
        {"id": "C1", "name": "Giá cả", "col": "gia_usd", "lower_is_better": True},
        {"id": "C2", "name": "Hiệu năng", "col": "hieu_nang", "lower_is_better": False},
        {"id": "C3", "name": "Pin", "col": "dung_luong_pin", "lower_is_better": False},
        {"id": "C4", "name": "Lưu trữ", "col": "dung_luong_luu_tru", "lower_is_better": False},
        {"id": "C5", "name": "Camera", "col": "chat_luong_camera", "lower_is_better": False},
        {"id": "C6", "name": "Thiết kế", "col": "thiet_ke", "lower_is_better": False},
    ]
    
    tabs = []
    headers = [LocationHeader(id=p.id, name=p.mau_dien_thoai or f"Phone {p.id}") for p in phones]
    
    for crit in criteria_def:
        col_name = crit["col"]
        lower_is_better = crit["lower_is_better"]
        
        matrix = [[1.0] * n for _ in range(n)]
        matrix_str = [["1"] * n for _ in range(n)]
        
        vals = [parse_numeric(getattr(p, col_name, 0)) for p in phones]
        
        for i in range(n):
            for j in range(n):
                if i == j:
                    matrix[i][j] = 1.0
                    matrix_str[i][j] = "1"
                elif i < j:
                    vi = vals[i]
                    vj = vals[j]
                    
                    if vi == 0: vi = 0.1
                    if vj == 0: vj = 0.1
                    
                    if lower_is_better:
                        ratio = vj / vi
                    else:
                        ratio = vi / vj
                        
                    scale = get_ahp_scale(ratio)
                    
                    if ratio >= 1:
                        matrix[i][j] = float(scale)
                        matrix[j][i] = 1.0 / scale
                        matrix_str[i][j] = str(scale)
                        matrix_str[j][i] = f"1/{scale}"
                    else:
                        scale = get_ahp_scale(1/ratio)
                        matrix[i][j] = 1.0 / scale
                        matrix[j][i] = float(scale)
                        matrix_str[i][j] = f"1/{scale}"
                        matrix_str[j][i] = str(scale)
        
        local_weights = []
        cr = 0.0
        if n > 0:
            local_weights = calculate_priority_vector(matrix)
            if n > 2:
                lambda_max = calculate_lambda_max(matrix, local_weights)
                ci = calculate_consistency_index(lambda_max, n)
                cr = round(calculate_consistency_ratio(ci, n), 4)

        tabs.append(CriteriaTabResponse(
            criteria_id=crit["id"],
            criteria_name=crit["name"],
            raw_column=col_name,
            locations_header=headers,
            matrix_rows=matrix_str,
            local_weights=[round(w, 4) for w in local_weights],
            cr=cr
        ))
        
    return CriteriaEvaluationResponse(
        success=True,
        total_locations=n,
        tabs=tabs
    )
