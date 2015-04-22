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

# UPDATE THIS VARIABLE
mapping = { "Ave": "Avenue",
            "Rd.": "Road",
            "St.": "Street"
            }


def audit_street_type(street_types, street_name):
    m = street_type_re.search(street_name)
    if m:
        street_type = m.group()
        if street_type not in expected:
            street_types[street_type].add(street_name)


def is_street_name(elem):
    return (elem.attrib['k'] == "addr:street")


def audit():
    query = { "address.street": {"$exists": 1}}
    projection = { "_id": 0, "address.street": 1 }
    street_types = defaultdict(set)
    streets = db.udacity.find(query,projection)
    for doc in streets:
        street = doc["address"]["street"]
        audit_street_type(street_types, street)

    return street_types


def update_name(name, mapping):

    for key in mapping.keys():
        regex = re.compile(r"\b" + re.escape(key) + r"$")
        name = re.sub(regex,mapping[key],name)

    return name


st_types = audit()
pprint.pprint(dict(st_types))

    # for st_type, ways in st_types.iteritems():
    #     for name in ways:
    #         better_name = update_name(name, mapping)
    #         print name, "=>", better_name
    #         if name == "West Lexington St.":
    #             assert better_name == "West Lexington Street"
    #         if name == "Baldwin Rd.":
    #             assert better_name == "Baldwin Road"

