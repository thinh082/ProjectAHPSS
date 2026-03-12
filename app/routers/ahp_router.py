from fastapi import APIRouter
from app.schemas.ahp_schema import (
    MatrixInput, ColumnSumResponse,
    NormalizeInput, NormalizeResponse,
    WeightsInput, WeightsResponse,
    ConsistencyInput, ConsistencyResponse,
    RankInput, RankResponse, RankItem
)
from app.services.ahp_service import (
    step_column_sum,
    step_normalize,
    step_weights,
    step_consistency,
    step_rank
)

# Tạo router với prefix /ahp và tag AHP để gom nhóm trên Swagger
router = APIRouter(prefix="/ahp", tags=["AHP Steps"])


# ─────────────────────────────────────────────
# Endpoint 1: Tính tổng cột + Validate
# ─────────────────────────────────────────────

@router.post("/step/column-sum", response_model=ColumnSumResponse)
def api_column_sum(body: MatrixInput):
    """
    **Bước 1:** Validate ma trận so sánh cặp và tính tổng từng cột.
    """
    col_sums = step_column_sum(body.matrix)
    return ColumnSumResponse(column_sums=col_sums)


# ─────────────────────────────────────────────
# Endpoint 2: Chuẩn hóa ma trận
# ─────────────────────────────────────────────

@router.post("/step/normalize", response_model=NormalizeResponse)
def api_normalize(body: NormalizeInput):
    """
    **Bước 2:** Chuẩn hóa ma trận AHP bằng cách chia mỗi phần tử cho tổng cột.
    """
    normalized = step_normalize(body.matrix, body.column_sums)
    return NormalizeResponse(normalized_matrix=normalized)


# ─────────────────────────────────────────────
# Endpoint 3: Tính vector trọng số
# ─────────────────────────────────────────────

@router.post("/step/weights", response_model=WeightsResponse)
def api_weights(body: WeightsInput):
    """
    **Bước 3:** Tính vector trọng số (priority vector) từ ma trận đã chuẩn hóa.
    """
    weights = step_weights(body.normalized_matrix)
    return WeightsResponse(weights=weights)


# ─────────────────────────────────────────────
# Endpoint 4: Kiểm tra Consistency (CR, CI, λmax)
# ─────────────────────────────────────────────

@router.post("/step/consistency", response_model=ConsistencyResponse)
def api_consistency(body: ConsistencyInput):
    """
    **Bước 4:** Kiểm tra tính nhất quán của ma trận (λmax, CI, CR).
    Nếu CR < 0.1 thì ma trận nhất quán, ngược lại cần nhập lại.
    """
    result = step_consistency(body.matrix, body.weights)
    return ConsistencyResponse(**result)


# ─────────────────────────────────────────────
# Endpoint 5: Xếp hạng phương án
# ─────────────────────────────────────────────

@router.post("/rank", response_model=RankResponse)
def api_rank(body: RankInput):
    """
    **Bước 5:** Xếp hạng các phương án dựa trên vector trọng số và điểm đánh giá.
    Kết quả được sắp xếp theo điểm giảm dần.
    """
    # Tự động tạo tên phương án nếu không có
    n = len(body.alternative_scores)
    names = body.names if body.names and len(body.names) == n else [f"Phương án {i+1}" for i in range(n)]

    ranking_data = step_rank(body.criteria_weights, body.alternative_scores, names)
    ranking = [RankItem(**item) for item in ranking_data]
    return RankResponse(ranking=ranking)
