import pytest
from models import Company, Dev, Freebie, db, Base, engine

@pytest.fixture(scope='function', autouse=True)
def setup_and_teardown():
    # Setup: create all tables and start a new session
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    yield
    # Teardown: rollback any changes and close session
    db.rollback()

def test_create_freebie_invalid_data():
    company = Company(name='TestCo', founding_year=2010)
    dev = Dev(name='Tester')
    db.add_all([company, dev])
    db.commit()

    # item_name is None
    with pytest.raises(Exception):
        freebie = Freebie(item_name=None, value=10, dev=dev, company=company)
        db.add(freebie)
        db.commit()

    # value is negative
    with pytest.raises(Exception):
        freebie = Freebie(item_name='Badge', value=-5, dev=dev, company=company)
        db.add(freebie)
        db.commit()

def test_give_away_invalid_conditions():
    company = Company(name='TestCo', founding_year=2010)
    dev1 = Dev(name='Dev1')
    dev2 = Dev(name='Dev2')
    db.add_all([company, dev1, dev2])
    db.commit()

    freebie = Freebie(item_name='Sticker', value=5, dev=dev1, company=company)
    db.add(freebie)
    db.commit()

    # Attempt to give away freebie not owned by dev2
    result = dev2.give_away(dev1, freebie)
    assert result is False
    assert freebie.dev == dev1

def test_received_one_nonexistent_item():
    company = Company(name='TestCo', founding_year=2010)
    dev = Dev(name='Tester')
    db.add_all([company, dev])
    db.commit()

    assert dev.received_one('Nonexistent') is False

def test_oldest_company_empty_db():
    # Drop all tables to simulate empty db
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)

    assert Company.oldest_company() is None

def test_session_rollback():
    company = Company(name='TestCo', founding_year=2010)
    dev = Dev(name='Tester')
    db.add_all([company, dev])
    db.commit()

    freebie = Freebie(item_name='Badge', value=10, dev=dev, company=company)
    db.add(freebie)
    db.commit()

    # Force an error and rollback
    try:
        freebie.value = -10  # invalid value
        db.commit()
    except Exception:
        db.rollback()

    # Value should remain unchanged
    refreshed_freebie = db.query(Freebie).filter_by(id=freebie.id).one()
    assert refreshed_freebie.value == 10
