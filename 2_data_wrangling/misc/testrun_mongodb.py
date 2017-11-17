#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Your task is to sucessfully run the exercise to see how pymongo works
and how easy it is to start using it.
You don't actually have to change anything in this exercise,
but you can change the city name in the add_city function if you like.

Your code will be run against a MongoDB instance that we have provided.
If you want to run this code locally on your machine,
you have to install MongoDB (see Instructor comments for link to installation information)
and uncomment the get_db function.
"""

#from pymongo import MongoClient
# client = MongoClient("mongodb://mongodb0.example.net:27019")
#db = MongoClient()

import pprint 
valid_zipcodes = ["91901","91902","91903","91905","91906","91908","91909","91910","91911","91912","91913","91914","91915","91916","91917","91921","91931","91932","91933","91934","91935","91941","91942","91943","91944","91945","91946","91947","91948","91950","91951","91962","91963","91976","91977","91978","91979","91980","91987","92003","92004","92007","92008","92009","92010","92011","92013","92014","92018","92019","92020","92021","92022","92023","92024","92025","92026","92027","92028","92029","92030","92033","92036","92037","92038","92039","92040","92046","92049","92051","92052","92054","92055","92056","92058","92057","92059","92060","92061","92064","92065","92066","92067","92068","92069","92070","92071","92072","92074","92075","92078","92079","92081","92082","92083","92084","92085","92086","92088","92090","92091","92092","92093","92096","92101","92102","92103","92104","92105","92106","92107","92108","92109","92110","92111","92112","92113","92114","92115","92116","92117","92118","92119","92120","92121","92122","92123","92124","92126","92127","92128","92129","92130","92131","92132","92134","92135","92136","92137","92138","92139","92140","92142","92143","92145","92147","92149","92150","92152","92153","92154","92155","92158","92159","92160","92161","92162","92163","92164","92165","92166","92167","92168","92169","92170","92171","92172","92173","92174","92175","92176","92177","92178","92179","92182","92184","92186","92187","92190","92191","92192","92193","92194","92195","92196","92197","92198","92199"]

def add_city(db):
    # Changes to this function will be reflected in the output. 
    # All other functions are for local use only.
    # Try changing the name of the city to be inserted
    db.cities.insert({"name" : "Chicago"})
    
def get_city(db):
    return db.cities.find_one()

def get_client():
    from pymongo import MongoClient
    client = MongoClient('localhost:27017')
    return client

def get_db():
    # For local use
    from pymongo import MongoClient
    client = MongoClient('localhost:27017')
    # 'examples' here is the database name. It will be created if it does not exist.
    db = client.example
    return db

def drop_db(db):
    db.cities.drop()
    
def get_database_names(client):
    return client.database_names()
    
def get_collection_names(client, collection):
    return getattr(client, collection).collection_names()

def print_nonvalid_zipcodes():
    
    pipeline = [{"$match":{"address.postcode":{"$exists":1}}},
               {"$group":{"_id":"$address.postcode", "count":{"$sum":1}}},
               {"$sort":{"count":1}}]
               
    result = client.examples.map.aggregate(pipeline)
    
    for doc in result:
        zipcode_does_not_match = 0
        for zipcode in valid_zipcodes:
            if str(doc["_id"]) == str(zipcode):
                break
        else:
            zipcode_does_not_match = 1
        if zipcode_does_not_match:
            pprint.pprint(doc)

def print_biggest_religion():
        
    pipeline = [{"$match":{"amenity":{"$exists":1}, "amenity":"place_of_worship"}},
                {"$group":{"_id":"$religion", "count":{"$sum":1}}},
                {"$sort":{"count":-1}}, {"$limit":10}]
               
    result = client.examples.map.aggregate(pipeline)
    
    for doc in result:
        pprint.pprint(doc)

def print_top10_amenities():
        
    pipeline = [{"$match":{"amenity":{"$exists":1}}}, {"$group":{"_id":"$amenity", "count":{"$sum":1}}}, {"$sort":{"count":-1}}, {"$limit":10}]
               
    result = client.examples.map.aggregate(pipeline)
    
    for doc in result:
        pprint.pprint(doc)

def print_top10_cuisines():
        
    pipeline = [{"$match":{"amenity":{"$exists":1}, "amenity":"restaurant"}}, {"$group":{"_id":"$cuisine", "count":{"$sum":1}}},{"$sort":{"count":-1}}, {"$limit":10}]
               
    result = client.examples.map.aggregate(pipeline)
    
    for doc in result:
        pprint.pprint(doc)

def print_top10_contributing_users():
        
    pipeline = [{"$group":{"_id":"$created.user", "count":{"$sum":1}}}, {"$sort":{"count":-1}}, {"$limit":10}]
               
    result = client.examples.map.aggregate(pipeline)
    
    for doc in result:
        pprint.pprint(doc)

def print_num_unique_users():
    num_unique_users = len(client.examples.map.distinct("created.user"))
    print "Number of unique users = %d" % num_unique_users
    
def print_overview_data():
    print "Overview of data:"    
    
    num_documents = client.examples.map.find().count()
    print "Number of documents = %d" % num_documents
    
    num_nodes = client.examples.map.find({"type":"node"}).count()
    print "Number of nodes = %d" % num_nodes
    
    num_ways = client.examples.map.find({"type":"way"}).count()
    print "Number of unique ways = %d" % num_ways   
    
    num_unique_users = len(client.examples.map.distinct("created.user"))
    print "Number of unique users = %d" % num_unique_users    

def print_cities_grouped():
    
        print "Cities grouped:"    
    
        pipeline = [{"$match":{"address.city":{"$exists":1}}},
               {"$group":{"_id":"$address.city", "count":{"$sum":1}}},
               {"$sort":{"count":-1}}]
               
        result = client.examples.map.aggregate(pipeline)
        
        for doc in result:
            pprint.pprint(doc)

if __name__ == "__main__":
    # For local use
    db = get_db() # uncomment this line if you want to run this locally
    #add_city(db)
    #drop_db(db)
    client = get_client()
    print get_database_names(client)
    print get_collection_names(client, 'examples')
    print get_collection_names(client, 'local')
    #client.examples.map.drop()
    #print get_city(db)
    #pipeline = [{"$match":{"address.postcode":{"$exists":1}}},
    #           {"$group":{"_id":"$address.postcode", "count":{"$sum":1}}},
    #           {"$sort":{"count":1}}]
    
    #pipeline = [{"$match":{"amenity":{"$exists":1}}}, {"$group":{"_id":"$amenity", "count":{"$sum":1}}}, {"$sort":{"count":1}}, {"$limit":10}]
    #print len(client.examples.map.distinct("created.user"))
    #result = client.examples.map.aggregate(pipeline)
    #print_nonvalid_zipcodes()
    #print_biggest_religion()
    #print_top10_amenities()
    #print_top10_cuisines()
    #print_top10_contributing_users()
    #print_num_unique_users()
    #print_overview_data()
    print_cities_grouped()