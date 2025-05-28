from models import Company, Dev, Freebie, session

# Clear existing data
session.query(Freebie).delete()
session.query(Company).delete()
session.query(Dev).delete()
session.commit()

# Create companies
company1 = Company(name="TechCorp", founding_year=2000)
company2 = Company(name="DevSoft", founding_year=1995)
company3 = Company(name="CodeMasters", founding_year=2010)

# Create devs
dev1 = Dev(name="Alice")
dev2 = Dev(name="Bob")
dev3 = Dev(name="Charlie")

# Add and commit
session.add_all([company1, company2, company3, dev1, dev2, dev3])
session.commit()

# Create freebies
freebie1 = Freebie(item_name="T-shirt", value=15, dev=dev1, company=company1)
freebie2 = Freebie(item_name="Stickers", value=5, dev=dev2, company=company1)
freebie3 = Freebie(item_name="Mug", value=10, dev=dev1, company=company2)
freebie4 = Freebie(item_name="Laptop", value=1000, dev=dev3, company=company3)

session.add_all([freebie1, freebie2, freebie3, freebie4])
session.commit()
