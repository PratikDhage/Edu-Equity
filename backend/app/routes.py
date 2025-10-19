from fastapi import APIRouter, Depends
from .services import get_clusters, predict_enrollment

router = APIRouter()

@router.get("/clusters")
async def clusters(state_code: str = None):
    return get_clusters(state_code)

@router.post("/predict")
async def predict(features: dict):
    return predict_enrollment(features)
