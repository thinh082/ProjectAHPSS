import os

filepath = r'd:\\Project\\ProjectAHPSS\\app\\routers\\ahp_router.py'

with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

# Replace imports
old_imports = """
from app.schemas.ahp_schema import (
    MatrixInput, ColumnSumResponse,
    NormalizeInput, NormalizeResponse,
    WeightsInput, WeightsResponse,
    ConsistencyInput, ConsistencyResponse,
    RankInput, RankResponse, RankItem,
    CriteriaRankInput, CriteriaRankResponse, CriteriaRankGroup, CriteriaRankItem
)
from app.services.ahp_service import (
    step_column_sum,
    step_normalize,
    step_weights,
    step_consistency,
    step_rank,
    step_rank_by_criteria
)
"""

new_imports = """
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.schemas.ahp_schema import (
    MatrixInput, ColumnSumResponse,
    NormalizeInput, NormalizeResponse,
    WeightsInput, WeightsResponse,
    ConsistencyInput, ConsistencyResponse,
    RankInput, RankResponse, RankItem,
    CriteriaRankInput, CriteriaRankResponse, CriteriaRankGroup, CriteriaRankItem,
    CriteriaEvaluationRequest, CriteriaEvaluationResponse
)
from app.services.ahp_service import (
    step_column_sum,
    step_normalize,
    step_weights,
    step_consistency,
    step_rank,
    step_rank_by_criteria,
    evaluate_criteria
)
"""

content = content.replace(old_imports.strip(), new_imports.strip())

# Add endpoint before rank
old_endpoint = """
# ─────────────────────────────────────────────
# Endpoint 5: Xếp hạng phương án
# ─────────────────────────────────────────────
"""

new_endpoint = """
# ─────────────────────────────────────────────
# Endpoint 4.5: Đánh giá phương án theo tiêu chí
# ─────────────────────────────────────────────

@router.post("/criteria-evaluation", response_model=CriteriaEvaluationResponse)
async def api_criteria_evaluation(
    body: CriteriaEvaluationRequest,
    session: AsyncSession = Depends(get_db)
):
    \"\"\"
    Đánh giá các phương án từ cơ sở dữ liệu dựa trên tiêu chí và tạo ma trận.
    \"\"\"
    return await evaluate_criteria(session, body)


# ─────────────────────────────────────────────
# Endpoint 5: Xếp hạng phương án
# ─────────────────────────────────────────────
"""

content = content.replace(old_endpoint.strip(), new_endpoint.strip())

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)

print("Router updated")
