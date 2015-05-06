# -*- coding: utf-8 -*-

from pymongo import MongoClient
import re
import os

client = MongoClient(os.environ['BOXEN_MONGODB_URL'])

db = client.osm.udacity

street_type_re = re.compile(r'\S+', re.IGNORECASE)

mapping = {
    re.compile(r"^Av\b.*$"): u"Avenida",
    re.compile(r"^Avendia\b.*$"): u"Avenida",
    re.compile(r"^Serv\b.*$"): u"Servidão",
    re.compile(r"^SC 401\b.*$"): u"Rodovia SC 401",
    "Terceira Avenida": "Avenida Terceira",
    "Quarta Avenida": "Avenida Quarta",
    "Almirante Barroso": "Rua Almirante Barroso",
    u"Almirante Tamandaré": u"Rua Almirante Tamandaré",
    "Dom Jaime Camara": "Rua Dom Jaime Camara",
    u"Salomé Damazio Jacques": u"Rua Salomé Damazio Jacques",
    "Almirante Barroso": "Rua Almirante Barroso",
    "Santos Saraiva": "Rua Santos Saraiva",
    u"São Miguel": u"Rua São Miguel",
    "Escadaria da Rua Pedro Soares": "Rua Pedro Soares",

}

def update_names():
    regex_type = type(street_type_re)
    string_type = type("")
    for key, value in mapping.items():
        if type(key) == regex_type:
            # If the key is a regex, first search for it in the database
            for doc in db.find({"address.street": key}):
                # For each doc, update it according to the regex
                name = doc["address"]["street"]
                name = re.sub(key,value,name)
                doc["address"]["street"] = name
                db.save(doc)
        elif type(key) == string_type:
            # If the key is a string we can issue an update statement directly
            db.update(
                {
                    "address.street":key,
                },
                { "$set": {"address.street": value}}
            )

update_names()
