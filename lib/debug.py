from models import session, Company, Dev, Freebie
from seed import *

# Test relationships
print("Company devs:", company1.devs)
print("Dev companies:", dev1.companies)

# Test methods
print("\\nFreebie details:", freebie1.print_details())
print("Oldest company:", Company.oldest_company().name)
print("Dev received mug:", dev1.received_one("Mug"))
print("Dev received hat:", dev1.received_one("Hat"))

# Test give_away
print("\\nBefore give_away:", freebie1.dev.name)
dev1.give_away(dev2, freebie1)
print("After give_away:", freebie1.dev.name)
