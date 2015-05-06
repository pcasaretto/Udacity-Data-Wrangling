# -*- coding: utf-8 -*-

from pymongo import MongoClient
from collections import defaultdict
import re
import pprint
import os

client = MongoClient(os.environ['BOXEN_MONGODB_URL'])

db = client.osm

street_type_re = re.compile(r'\S+', re.IGNORECASE)

expected = ["Rua", "Avenida", "Alameda", "Beco", "Estrada", "Rodovia", u'Praça', u'Servidão', "Travessa"]

mapping = { "Ave": "Avenue",
            "Rd.": "Road",
            "St.": "Street"
            }

# Look for street type that do not fall in the expected group
def audit_street_type(street_types, street_name):
    m = street_type_re.search(street_name)
    if m:
        street_type = m.group()
        if street_type not in expected:
            street_types[street_type].add(street_name)


def is_street_name(elem):
    return (elem.attrib['k'] == "addr:street")


def audit():
    # Query docs that have street information
    query = { "address.street": {"$exists": 1}}
    projection = { "_id": 0, "address.street": 1 }
    street_types = defaultdict(set)
    streets = db.udacity.find(query,projection)
    for doc in streets:
        street = doc["address"]["street"]
        audit_street_type(street_types, street)

    return street_types


st_types = audit()
pprint.pprint(dict(st_types))
