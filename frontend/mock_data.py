import random
from typing import Dict, List
from shared.schemas.synergy import CampaignInput, SynergyResponse

def generate_campaign() -> CampaignInput:
    categories = ["Enterprise SaaS", "E-commerce", "Fintech"]
    return CampaignInput(
        campaign_name=f"Q3 Launch {random.choice(categories)}",
        product_category=random.choice(categories),
        audience="C-Level Tech Executives",
        budget=round(random.uniform(5000, 20000), 2),
        objective=random.choice(["Conversions", "Awareness"])
    )

def generate_bid(input_data: CampaignInput) -> float:
    base = 1.50 if input_data.objective == "Awareness" else 2.50
    return round(base + random.uniform(-0.5, 1.5), 2)

def generate_creative(category: str) -> Dict[str, str]:
    creatives = {
        "Enterprise SaaS": {
            "image_url": "https://via.placeholder.com/600x300.png?text=Cloud+Architecture",
            "copy": "Scale Your Enterprise Architecture Without the Overhead. Reduce server costs by 40%."
        },
        "E-commerce": {
            "image_url": "https://via.placeholder.com/600x300.png?text=Retail+Promo",
            "copy": "Exclusive Holiday Discounts Inside. Shop the latest trends before they sell out."
        },
        "Fintech": {
            "image_url": "https://via.placeholder.com/600x300.png?text=Secure+Banking",
            "copy": "Bank Securely From Anywhere. Next-generation encryption for your peace of mind."
        }
    }
    return creatives.get(category, creatives["Enterprise SaaS"])

def generate_metrics(bid_price: float) -> SynergyResponse:
    return SynergyResponse(
        bid_price=bid_price,
        selected_creative="Creative A",
        predicted_ctr=round(random.uniform(4.0, 12.0), 2),
        expected_roi=round(random.uniform(10.0, 35.0), 1),
        confidence_score=round(random.uniform(0.85, 0.99), 2),
        explanation=[
            "Creative predicted highest CTR for this audience segment.",
            "Audience match score = 91%",
            "Historical conversion trend is positive for this time of day."
        ]
    )

def generate_leaderboard_mock() -> List[Dict]:
    """Generates mock data for the Creative Intelligence leaderboard."""
    return [
        {
            "Creative Name": f"Creative {chr(65+i)}",
            "Category": random.choice(["Enterprise SaaS", "E-commerce", "Fintech"]),
            "CTR": f"{random.uniform(2.0, 9.0):.1f}%",
            "Conv Rate": f"{random.uniform(0.5, 4.0):.1f}%",
            "Score": round(random.uniform(60, 98), 1)
        }
        for i in range(10)
    ]
