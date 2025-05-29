import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Company, Dev, Freebie, Base

engine = create_engine('sqlite:///freebies.db')
Session = sessionmaker(bind=engine)
session = Session()

@pytest.fixture(scope='function', autouse=True)
def setup_and_teardown():
    # Setup: create all tables and start a new session
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    yield
    # Teardown: rollback any changes and close session
    session.rollback()

def test_create_freebie_invalid_data():
    company = Company(name='TestCo', founding_year=2010)
    dev = Dev(name='Tester')
    session.add_all([company, dev])
    session.commit()

    # item_name is None
    with pytest.raises(Exception):
        freebie = Freebie(item_name=None, value=10, dev=dev, company=company)
        session.add(freebie)
        session.commit()

    # value is negative
    with pytest.raises(Exception):
        freebie = Freebie(item_name='Badge', value=-5, dev=dev, company=company)
        session.add(freebie)
        session.commit()

def test_give_away_invalid_conditions():
    company = Company(name='TestCo', founding_year=2010)
    dev1 = Dev(name='Dev1')
    dev2 = Dev(name='Dev2')
    session.add_all([company, dev1, dev2])
    session.commit()

    freebie = Freebie(item_name='Sticker', value=5, dev=dev1, company=company)
    session.add(freebie)
    session.commit()

    # Attempt to give away freebie not owned by dev2
    result = dev2.give_away(dev1, freebie)
    assert result is False
    assert freebie.dev == dev1

def test_received_one_nonexistent_item():
    company = Company(name='TestCo', founding_year=2010)
    dev = Dev(name='Tester')
    session.add_all([company, dev])
    session.commit()

    assert dev.received_one('Nonexistent') is False

def test_oldest_company_empty_db():
    # Drop all tables to simulate empty db
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)

    assert Company.oldest_company(session) is None

def test_session_rollback():
    company = Company(name='TestCo', founding_year=2010)
    dev = Dev(name='Tester')
    session.add_all([company, dev])
    session.commit()

    freebie = Freebie(item_name='Badge', value=10, dev=dev, company=company)
    session.add(freebie)
    session.commit()

    # Force an error and rollback
    try:
        freebie.value = -10  # invalid value
        session.commit()
    except Exception:
        session.rollback()

    # Value should remain unchanged
    refreshed_freebie = session.query(Freebie).filter_by(id=freebie.id).one()
    assert refreshed_freebie.value == 10
