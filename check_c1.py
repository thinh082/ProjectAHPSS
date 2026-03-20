"""
Script kiểm tra C1 matrix có đúng không sau khi hardcode.
"""
import asyncio
from app.database import SessionLocal
from app.schemas.ahp_schema import CriteriaEvaluationRequest
from app.services.ahp_service import evaluate_criteria

async def check_c1():
    request_data = {
        "weights": [0.2, 0.15, 0.15, 0.15, 0.15, 0.2],
        "filters": {"limit": 10}
    }
    req = CriteriaEvaluationRequest(**request_data)
    async with SessionLocal() as session:
        result = await evaluate_criteria(session, req)

    c1 = result.tabs[0]
    print(f"Criteria: {c1.criteria_id} - {c1.criteria_name}")
    print(f"Total phones: {len(c1.locations_header)}")
    print("Matrix row 0 (S24 Ultra):", c1.matrix_rows[0])
    print("Matrix row 3 (Z Fold5):", c1.matrix_rows[3])
    print("local_weights:", c1.local_weights)
    print("CR:", c1.cr)

if __name__ == "__main__":
    asyncio.run(check_c1())
