#!/usr/bin/env python3
"""
Module for listing all documents in a collection.
"""


def list_all(mongo_collection):
    """
    Lists all documents in a collection.

    Args:
        mongo_collection (pymongo.collection.Collection): The MongoDB collection.

    Returns:
        list: A list of all documents in the collection.
    """
    return list(mongo_collection.find())


if __name__ == "__main__":
    from pymongo import MongoClient

    client = MongoClient('mongodb://127.0.0.1:27017')
    school_collection = client.my_db.school
    schools = list_all(school_collection)
    print(f"Total documents found: {len(schools)}")
    for school in schools:
        print("[{}] {}".format(school.get('_id'), school.get('name')))
