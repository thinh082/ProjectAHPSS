import os

content = '''
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
    m = re.search(r"\\d+(\\.\\d+)?", str(val))
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
'''

# Note: this appends to ahp_service.py
with open(r'd:\Project\ProjectAHPSS\app\services\ahp_service.py', 'a', encoding='utf-8') as f:
    f.write(content)
print("done")
