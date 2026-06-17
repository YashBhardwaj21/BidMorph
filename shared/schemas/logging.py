from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class ImpressionLog(BaseModel):
    impression_id: str
    user_id: str
    product_id: str
    bid_price: float
    ctr_score: float
    synergy_score: float
    bid_model_version: str
    creative_model_version: str
    timestamp: datetime

class OutcomeLog(BaseModel):
    impression_id: str         # Foreign key → ImpressionLog
    clicked: bool
    revenue: Optional[float] = None
    timestamp: datetime
