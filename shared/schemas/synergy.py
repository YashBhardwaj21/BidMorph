from pydantic import BaseModel
from typing import List

class CampaignInput(BaseModel):
    campaign_name: str
    product_category: str
    audience: str
    budget: float
    objective: str

class SynergyResponse(BaseModel):
    bid_price: float
    selected_creative: str
    predicted_ctr: float
    expected_roi: float
    confidence_score: float
    explanation: List[str]
