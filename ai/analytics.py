from fastapi import APIRouter
from sklearn.linear_model import LinearRegression
import numpy as np

router = APIRouter()

@router.get("/ai-analytics", tags=["ai"])
def ai_analytics():
    # Example: Predict file upload trends (dummy data)
    x = np.arange(10).reshape(-1, 1)
    y = np.array([2, 3, 5, 7, 11, 13, 17, 19, 23, 29])
    model = LinearRegression().fit(x, y)
    future_x = np.arange(10, 15).reshape(-1, 1)
    predictions = model.predict(future_x)
    return {"future": predictions.tolist()}
