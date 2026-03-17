from pydantic import BaseModel, Field, field_validator
from typing import List, Optional, Dict, Any, Dict, Any

# ─────────────────────────────────────────────
# Step 1: Tính tổng cột
# ─────────────────────────────────────────────

class MatrixInput(BaseModel):
    """Input chứa ma trận so sánh cặp AHP."""
    matrix: List[List[float]]

    @field_validator("matrix")
    @classmethod
    def matrix_must_not_be_empty(cls, v):
        # Kiểm tra ma trận không rỗng
        if not v or not v[0]:
            raise ValueError("Ma trận không được rỗng.")
        return v


class ColumnSumResponse(BaseModel):
    """Output trả về tổng của từng cột trong ma trận."""
    column_sums: List[float]


# ─────────────────────────────────────────────
# Step 2: Chuẩn hóa ma trận
# ─────────────────────────────────────────────

class NormalizeInput(BaseModel):
    """Input chứa ma trận gốc và tổng cột để chuẩn hóa."""
    matrix: List[List[float]]
    column_sums: List[float]


class NormalizeResponse(BaseModel):
    """Output trả về ma trận đã được chuẩn hóa."""
    normalized_matrix: List[List[float]]


# ─────────────────────────────────────────────
# Step 3: Tính vector trọng số (Priority Vector)
# ─────────────────────────────────────────────

class WeightsInput(BaseModel):
    """Input chứa ma trận đã chuẩn hóa để tính trọng số."""
    normalized_matrix: List[List[float]]


class WeightsResponse(BaseModel):
    """Output trả về vector trọng số (priority vector)."""
    weights: List[float]


# ─────────────────────────────────────────────
# Step 4: Kiểm tra Consistency
# ─────────────────────────────────────────────

class ConsistencyInput(BaseModel):
    """Input chứa ma trận gốc và vector trọng số để kiểm tra độ nhất quán."""
    matrix: List[List[float]]
    weights: List[float]


class ConsistencyResponse(BaseModel):
    """Output trả về kết quả kiểm tra độ nhất quán: λmax, CI, CR."""
    lambda_max: float
    CI: float
    CR: float
    is_consistent: bool


# ─────────────────────────────────────────────
# Step 5: Xếp hạng phương án (Ranking)
# ─────────────────────────────────────────────

class RankInput(BaseModel):
    """
    Input để xếp hạng phương án.
    - criteria_weights: Vector trọng số các tiêu chí
    - alternative_scores: Ma trận điểm của từng phương án theo từng tiêu chí
    - names: Tên của từng phương án (tùy chọn)
    """
    criteria_weights: List[float]
    alternative_scores: List[List[float]]
    names: Optional[List[str]] = None


class RankItem(BaseModel):
    """Kết quả điểm của một phương án."""
    name: str
    score: float


class RankResponse(BaseModel):
    """Output trả về danh sách phương án đã xếp hạng theo thứ tự giảm dần."""
    ranking: List[RankItem]

class CriteriaRankInput(BaseModel):
    """
    Input de xep hang theo tung tieu chi.
    - alternative_scores: Ma tran diem cua tung phuong an theo tung tieu chi
    - names: Ten phuong an (tuy chon)
    - criteria_names: Ten tieu chi (tuy chon)
    - top_k: So luong phuong an cao nhat can lay cho moi tieu chi
    """
    alternative_scores: List[List[float]]
    names: Optional[List[str]] = None
    criteria_names: Optional[List[str]] = None
    top_k: int = Field(default=3, ge=1)


class CriteriaRankItem(BaseModel):
    rank: int
    name: str
    score: float


class CriteriaRankGroup(BaseModel):
    criterion: str
    top_alternatives: List[CriteriaRankItem]


class CriteriaRankResponse(BaseModel):
    rankings_by_criteria: List[CriteriaRankGroup]

# ─────────────────────────────────────────────
# Đánh giá phương án theo tiêu chí (Tích hợp DB)
# ─────────────────────────────────────────────

class CriteriaEvaluationRequest(BaseModel):
    """Input request cho tính năng đánh giá các phương án từ CSDL trực tiếp"""
    weights: List[float] = Field(..., description="Danh sách 5 trọng số của 5 tiêu chí. Tổng phải bằng 1.0")
    filters: Optional[Dict[str, Any]] = Field(default=None, description="Bộ lọc tùy chọn (VD: mau_dien_thoai, limit...)")

    @field_validator("weights")
    @classmethod
    def validate_weights(cls, v):
        if len(v) != 5:
            raise ValueError("Phải cung cấp chính xác 5 trọng số.")
        # Do sai số số thực, kiểm tra tổng xấp xỉ 1.0
        if abs(sum(v) - 1.0) > 1e-4:
            raise ValueError("Tổng các trọng số phải bằng 1.0.")
        return v

class LocationHeader(BaseModel):
    id: int
    name: str

class CriteriaTabResponse(BaseModel):
    criteria_id: str
    criteria_name: str
    raw_column: str
    locations_header: List[LocationHeader]
    matrix_rows: List[List[str]]
    local_weights: List[float]
    cr: float

class CriteriaEvaluationResponse(BaseModel):
    success: bool
    total_locations: int
    tabs: List[CriteriaTabResponse]
