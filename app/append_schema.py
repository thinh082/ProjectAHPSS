import os

content = '''
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
'''

schema_path = r'd:\\Project\\ProjectAHPSS\\app\\schemas\\ahp_schema.py'
with open(schema_path, 'a', encoding='utf-8') as f:
    f.write(content)

print(f"Successfully appended schema to {schema_path}")
