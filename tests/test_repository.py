import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime

from storage.models import Base
from storage.repository import create_impression, get_impression, create_outcome, get_outcomes_for_impression
from shared.schemas.logging import ImpressionLog
from shared.schemas.outcome import OutcomeRequest

# Setup in-memory SQLite DB for testing
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture()
def db():
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)

def test_create_and_get_impression(db):
    log = ImpressionLog(
        impression_id="imp-001",
        user_id="user-123",
        product_id="prod-abc",
        bid_price=1.50,
        ctr_score=0.05,
        synergy_score=0.8,
        bid_model_version="oil-v1",
        creative_model_version="caig-v1",
        timestamp=datetime.utcnow()
    )
    impression = create_impression(db, log)
    assert impression.impression_id == "imp-001"
    assert impression.bid_price == 1.50

    fetched = get_impression(db, "imp-001")
    assert fetched is not None
    assert fetched.user_id == "user-123"

def test_idempotency_duplicate_impression(db):
    log = ImpressionLog(
        impression_id="imp-002",
        user_id="user-123",
        product_id="prod-abc",
        bid_price=1.50,
        ctr_score=0.05,
        synergy_score=0.8,
        bid_model_version="oil-v1",
        creative_model_version="caig-v1",
        timestamp=datetime.utcnow()
    )
    # First insert
    imp1 = create_impression(db, log)
    # Second insert should return the same object without crashing
    imp2 = create_impression(db, log)
    assert imp1.impression_id == imp2.impression_id

def test_create_outcome(db):
    # Setup parent impression first
    log = ImpressionLog(
        impression_id="imp-003",
        user_id="user-123",
        product_id="prod-abc",
        bid_price=1.50,
        ctr_score=0.05,
        synergy_score=0.8,
        bid_model_version="oil-v1",
        creative_model_version="caig-v1",
        timestamp=datetime.utcnow()
    )
    create_impression(db, log)

    req = OutcomeRequest(impression_id="imp-003", clicked=True, revenue=10.0)
    outcome = create_outcome(db, req)
    
    assert outcome is not None
    assert outcome.clicked is True
    assert outcome.revenue == 10.0
    
    outcomes = get_outcomes_for_impression(db, "imp-003")
    assert len(outcomes) == 1
    assert outcomes[0].id == outcome.id

def test_create_outcome_fails_without_impression(db):
    # Try to create outcome for missing impression
    req = OutcomeRequest(impression_id="missing-imp", clicked=True, revenue=None)
    outcome = create_outcome(db, req)
    assert outcome is None
