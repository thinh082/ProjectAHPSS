import asyncio
from app.database import SessionLocal
from app.schemas.ahp_schema import CriteriaEvaluationRequest
from app.services.ahp_service import evaluate_criteria

async def test_endpoint():
    request_data = {
        "weights": [0.2314, 0.1915, 0.1938, 0.1183, 0.1396, 0.1254],
        "filters": {
            "mau_dien_thoai": "Galaxy S24",
            "limit": 5
        }
    }
    
    req = CriteriaEvaluationRequest(**request_data)
    async with SessionLocal() as session:
        result = await evaluate_criteria(session, req)
        
    print(f"Success. Total tabs: {len(result.tabs)}")

if __name__ == "__main__":
    asyncio.run(test_endpoint())
