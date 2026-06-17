from pydantic import BaseModel
from typing import Optional

class OutcomeRequest(BaseModel):
    """
    Design Decision for Outcome Tracking:
    
    1. What is a click? 
       - An interaction where the user clicks on the ad creative. 
       - Indicated by `clicked = True`.
       
    2. What is a conversion?
       - A downstream event where the user purchases the product.
       - Captured indirectly through `revenue`. If `revenue > 0`, it was a conversion.
       
    3. How is ROI calculated?
       - ROI = (Total Revenue - Total Bid Spend) / Total Bid Spend
       - Note: Revenue can be None if not clicked, or 0.0 if clicked but not converted.
    """
    impression_id: str
    clicked: bool
    revenue: Optional[float] = None
