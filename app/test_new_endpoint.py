import asyncio
import json
from app.database import SessionLocal
from app.schemas.ahp_schema import CriteriaEvaluationRequest
from app.services.ahp_service import evaluate_criteria

async def test_endpoint():
    request_data = {
        "weights": [0.2977, 0.0886, 0.158, 0.2977, 0.158],
        "filters": {
            "mau_dien_thoai": "Galaxy S24",
            "limit": 5
        }
    }
    print("----- INPUT REQUEST -----")
    print(json.dumps(request_data, indent=2, ensure_ascii=False))
    
    req = CriteriaEvaluationRequest(**request_data)
    
    async with SessionLocal() as session:
        result = await evaluate_criteria(session, req)
        
    print("\n----- OUTPUT RESPONSE -----")
    print(result.model_dump_json(indent=2))

if __name__ == "__main__":
    asyncio.run(test_endpoint())
