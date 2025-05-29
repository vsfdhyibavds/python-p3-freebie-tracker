from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Company(Base):
    __tablename__ = 'companies'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    founding_year = Column(Integer)

    freebies = relationship('Freebie', backref='company')

    @property
    def devs(self):
        # Return unique Dev instances associated with this company's freebies
        return list({freebie.dev for freebie in self.freebies})

    def give_freebie(self, dev, item_name, value):
        new_freebie = Freebie(item_name=item_name, value=value, dev=dev, company=self)
        self.freebies.append(new_freebie)
        return new_freebie

    @classmethod
    def oldest_company(cls, session):
        # Return the company with the smallest founding_year
        return session.query(cls).order_by(cls.founding_year).first()

class Dev(Base):
    __tablename__ = 'devs'

    id = Column(Integer, primary_key=True)
    name = Column(String)

    freebies = relationship('Freebie', backref='dev')

    @property
    def companies(self):
        # Return unique Company instances associated with this dev's freebies
        return list({freebie.company for freebie in self.freebies})

    def received_one(self, item_name):
        return any(freebie.item_name == item_name for freebie in self.freebies)

    def give_away(self, dev, freebie):
        # Change the freebie's dev to the given dev only if this dev owns it
        if freebie in self.freebies:
            freebie.dev = dev
            return True
        return False

class Freebie(Base):
    __tablename__ = 'freebies'

    id = Column(Integer, primary_key=True)
    item_name = Column(String)
    value = Column(Integer)

    dev_id = Column(Integer, ForeignKey('devs.id'))
    company_id = Column(Integer, ForeignKey('companies.id'))

    def print_details(self):
        return f"{self.dev.name} owns a {self.item_name} from {self.company.name}"