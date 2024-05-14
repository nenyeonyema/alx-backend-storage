#!/usr/bin/env python3
"""
Module for updating all topics of a school document based on the name.
"""


def update_topics(mongo_collection, name, topics):
    """
    Changes all topics of a school document based on the name.

    Args:
        mongo_collection (pymongo.collection.Collection): The MongoDB collection.
        name (str): The school name to update.
        topics (list of str): The list of topics to be set for the school.
    """
    mongo_collection.update_many(
        {"name": name},
        {"$set": {"topics": topics}}
    )


if __name__ == "__main__":
    from pymongo import MongoClient
    from 8-all import list_all

    client = MongoClient('mongodb://127.0.0.1:27017')
    school_collection = client.my_db.school

    # Update topics
    update_topics(school_collection, "Holberton school", ["Sys admin", "AI", "Algorithm"])

    # List all schools
    schools = list_all(school_collection)
    for school in schools:
        print("[{}] {} {}".format(school.get('_id'), school.get('name'), school.get('topics', "")))

    # Update topics again
    update_topics(school_collection, "Holberton school", ["iOS"])

    # List all schools again
    schools = list_all(school_collection)
    for school in schools:
        print("[{}] {} {}".format(school.get('_id'), school.get('name'), school.get('topics', "")))
