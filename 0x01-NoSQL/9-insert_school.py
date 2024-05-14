#!/usr/bin/env python3
"""
Module for inserting a new document in a collection based on kwargs.
"""


def insert_school(mongo_collection, **kwargs):
    """
    Inserts a new document in a collection based on kwargs.

    Args:
        mongo_collection (pymongo.collection.Collection): The MongoDB collection.
        **kwargs: Arbitrary keyword arguments for the new document.

    Returns:
        ObjectId: The _id of the newly inserted document.
    """
    result = mongo_collection.insert_one(kwargs)
    return result.inserted_id


if __name__ == "__main__":
    from pymongo import MongoClient
    from 8-all import list_all

    client = MongoClient('mongodb://127.0.0.1:27017')
    school_collection = client.my_db.school
    new_school_id = insert_school(school_collection, name="UCSF", address="505 Parnassus Ave")
    print("New school created: {}".format(new_school_id))

    schools = list_all(school_collection)
    for school in schools:
        print("[{}] {} {}".format(school.get('_id'), school.get('name'), school.get('address', "")))
