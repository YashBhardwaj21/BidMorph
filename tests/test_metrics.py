from pipelines.evaluation.metrics import ctr_lift, roi, bid_efficiency, synergy_score_distribution

class MockOutcome:
    def __init__(self, clicked, revenue):
        self.clicked = clicked
        self.revenue = revenue

class MockImpression:
    def __init__(self, bid_price, synergy_score, outcomes):
        self.bid_price = bid_price
        self.synergy_score = synergy_score
        self.outcomes = outcomes

def test_ctr_lift():
    # BidMorph: 2 clicks out of 4 impressions = 50% CTR
    bm_imps = [
        MockImpression(1.0, 0.8, [MockOutcome(True, 0.0)]),
        MockImpression(1.0, 0.8, [MockOutcome(True, 10.0)]),
        MockImpression(1.0, 0.8, [MockOutcome(False, None)]),
        MockImpression(1.0, 0.8, [MockOutcome(False, None)])
    ]
    
    # Baseline: 1 click out of 4 impressions = 25% CTR
    base_imps = [
        MockImpression(1.0, 0.4, [MockOutcome(True, 0.0)]),
        MockImpression(1.0, 0.4, [MockOutcome(False, None)]),
        MockImpression(1.0, 0.4, [MockOutcome(False, None)]),
        MockImpression(1.0, 0.4, [MockOutcome(False, None)])
    ]
    
    lift = ctr_lift(bm_imps, base_imps)
    assert lift == 1.0  # (0.5 - 0.25) / 0.25 = 1.0 (100% lift)

def test_roi_and_efficiency():
    imps = [
        MockImpression(bid_price=2.0, synergy_score=0.9, outcomes=[MockOutcome(True, 10.0)]),
        MockImpression(bid_price=3.0, synergy_score=0.9, outcomes=[MockOutcome(True, 5.0)]),
        MockImpression(bid_price=5.0, synergy_score=0.9, outcomes=[MockOutcome(False, None)])
    ]
    
    # Total Spend = 10.0
    # Total Revenue = 15.0
    # ROI = (15 - 10) / 10 = 0.5
    # Efficiency = 15 / 10 = 1.5
    assert roi(imps) == 0.5
    assert bid_efficiency(imps) == 1.5

def test_synergy_distribution():
    imps = [
        MockImpression(1.0, 0.2, []),
        MockImpression(1.0, 0.4, []),
        MockImpression(1.0, 0.4, []),
        MockImpression(1.0, 0.6, [])
    ]
    dist = synergy_score_distribution(imps)
    assert dist["mean"] == 0.4
    assert dist["median"] == 0.4
    # Variance = ((0.2-0.4)^2 + 0 + 0 + (0.6-0.4)^2) / 4 = 0.02
    assert round(dist["stddev"], 4) == 0.1414
