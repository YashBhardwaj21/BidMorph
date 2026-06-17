from typing import List, Any

# We use typing.Any for the list objects so this can accept either 
# SQLAlchemy ORM objects or Mock objects during tests, as long as 
# they have the correct attributes (outcomes, bid_price, synergy_score).

def ctr_lift(bidmorph_impressions: List[Any], baseline_impressions: List[Any]) -> float:
    """Calculates CTR Lift = (BidMorph CTR - Baseline CTR) / Baseline CTR"""
    def calc_ctr(imps: List[Any]) -> float:
        if not imps:
            return 0.0
        clicks = sum(1 for imp in imps for out in imp.outcomes if out.clicked)
        return clicks / len(imps)

    bm_ctr = calc_ctr(bidmorph_impressions)
    base_ctr = calc_ctr(baseline_impressions)
    
    if base_ctr == 0:
        return 0.0
    return (bm_ctr - base_ctr) / base_ctr

def roi(impressions: List[Any]) -> float:
    """Calculates ROI = (Total Revenue - Total Bid Spend) / Total Bid Spend"""
    total_spend = sum(imp.bid_price for imp in impressions)
    total_revenue = sum((out.revenue or 0.0) for imp in impressions for out in imp.outcomes)
    
    if total_spend == 0:
        return 0.0
    return (total_revenue - total_spend) / total_spend

def bid_efficiency(impressions: List[Any]) -> float:
    """Calculates Revenue per dollar spent = Total Revenue / Total Bid Spend"""
    total_spend = sum(imp.bid_price for imp in impressions)
    total_revenue = sum((out.revenue or 0.0) for imp in impressions for out in imp.outcomes)
    
    if total_spend == 0:
        return 0.0
    return total_revenue / total_spend

def synergy_score_distribution(impressions: List[Any]) -> dict:
    """Calculates Mean, Median, and StdDev of synergy scores"""
    if not impressions:
        return {"mean": 0.0, "median": 0.0, "stddev": 0.0}
        
    scores = sorted([imp.synergy_score for imp in impressions])
    n = len(scores)
    mean = sum(scores) / n
    median = scores[n // 2] if n % 2 != 0 else (scores[n // 2 - 1] + scores[n // 2]) / 2.0
    variance = sum((x - mean) ** 2 for x in scores) / n
    stddev = variance ** 0.5
    
    return {
        "mean": mean,
        "median": median,
        "stddev": stddev
    }
