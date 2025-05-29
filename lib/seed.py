from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models import Base, Company, Dev, Freebie

# Configure your database URL here
DATABASE_URL = "sqlite:///freebies.db"

engine = create_engine(DATABASE_URL, echo=True)
Session = sessionmaker(bind=engine)
session = Session()

# Create all tables
Base.metadata.create_all(engine)

# Clear any existing data (optional)
session.query(Freebie).delete()
session.query(Dev).delete()
session.query(Company).delete()
session.commit()

# Create some companies
c1 = Company(name="Acme Corp", founding_year=1990)
c2 = Company(name="Globex Inc", founding_year=1985)
c3 = Company(name="Soylent Corp", founding_year=2000)

session.add_all([c1, c2, c3])
session.commit()

# Create some devs
d1 = Dev(name="Alice")
d2 = Dev(name="Bob")
d3 = Dev(name="Charlie")

session.add_all([d1, d2, d3])
session.commit()

# Give freebies using the company method
c1.give_freebie(d1, "T-Shirt", 10)
c1.give_freebie(d2, "Sticker Pack", 5)
c2.give_freebie(d1, "Coffee Mug", 15)
c3.give_freebie(d3, "Notebook", 20)

# Commit freebies
session.commit()

print("Seeding complete!")

session.close()