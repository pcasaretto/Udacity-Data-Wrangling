// Update documents that do not start with the proper area code
db.udacity.update({"$and": [{"address.postcode": {"$exists": true}}, {"address.postcode": {"$not": /^8[89]/ } } ] }, {"$set": {"address.postcode": "88063-000"}})

// Update area codes that are not in correct format
db.udacity.find({"$and": [{"address.postcode": {"$exists": true}}, {"address.postcode": /\d\d\d\d\d\d\d\d/ }]}).forEach(function(doc) {
  doc.address.postcode = doc.address.postcode.replace(/\d\d\d$/g, function(match) {
    return "-" + match;
  });
  db.udacity.save(doc)
});
