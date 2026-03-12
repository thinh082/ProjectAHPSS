from pydantic import BaseModel, field_validator
from typing import List, Optional

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
