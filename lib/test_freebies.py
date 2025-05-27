from models import Company, Dev, Freebie, db

if __name__ == '__main__':
    # Create some test data
    company1 = Company(name='TechCorp', founding_year=2000)
    company2 = Company(name='DevSoft', founding_year=1995)
    dev1 = Dev(name='Alice')
    dev2 = Dev(name='Bob')

    db.add_all([company1, company2, dev1, dev2])
    db.commit()

    # Test relationships
    freebie1 = Freebie(item_name='T-shirt', value=20, dev=dev1, company=company1)
    db.add(freebie1)
    db.commit()

    # Test methods
    assert freebie1.print_details() == "Alice owns a T-shirt from TechCorp"
    assert dev1.companies == [company1]
    assert company1.devs == [dev1]

    # Test give_freebie
    company1.give_freebie(dev2, 'Sticker', 5)
    assert len(dev2.freebies) == 1

    # Test oldest_company
    assert Company.oldest_company().name == "DevSoft"

    # Test received_one
    assert dev1.received_one('T-shirt') is True
    assert dev1.received_one('Mug') is False

    # Test give_away
    dev1.give_away(dev2, freebie1)
    assert freebie1.dev.name == "Bob"
