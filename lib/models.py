from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

Base = declarative_base()
engine = create_engine('sqlite:///freebies.db')
Session = sessionmaker(bind=engine)
db = Session()

class Freebie(Base):
    __tablename__ = 'freebies'

    id = Column(Integer, primary_key=True)
    item_name = Column(String)
    value = Column(Integer)

    dev_id = Column(Integer, ForeignKey('devs.id'))
    company_id = Column(Integer, ForeignKey('companies.id'))

    dev = relationship('Dev', backref=backref('freebies', cascade='all, delete-orphan'))
    company = relationship('Company', backref=backref('freebies', cascade='all, delete-orphan'))

    def __repr__(self):
        return f'<Freebie {self.item_name} value={self.value}>'

    def print_details(self):
        return f"{self.dev.name} owns a {self.item_name} from {self.company.name}"

class Company(Base):
    __tablename__ = 'companies'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    founding_year = Column(Integer)

    devs = association_proxy('freebies', 'dev',
        creator=lambda dev: Freebie(dev=dev))

    def __repr__(self):
        return f'<Company {self.name} founded={self.founding_year}>'

    def give_freebie(self, dev, item_name, value):
        freebie = Freebie(
            dev=dev,
            company=self,
            item_name=item_name,
            value=value
        )
        db.add(freebie)
        db.commit()
        return freebie

    @classmethod
    def oldest_company(cls):
        return db.query(cls).order_by(cls.founding_year).first()

class Dev(Base):
    __tablename__ = 'devs'

    id = Column(Integer, primary_key=True)
    name = Column(String)

    companies = association_proxy('freebies', 'company',
        creator=lambda company: Freebie(company=company))

    def __repr__(self):
        return f'<Dev {self.name}>'

    def received_one(self, item_name):
        return db.query(Freebie).filter(
            Freebie.dev_id == self.id,
            Freebie.item_name == item_name
        ).first() is not None

    def give_away(self, dev, freebie):
        if freebie.dev == self:
            freebie.dev = dev
            db.commit()
            return True
        return False

# Create all tables
Base.metadata.create_all(engine)