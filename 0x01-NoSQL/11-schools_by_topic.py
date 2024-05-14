#!/usr/bin/env python3
"""
Module for retrieving schools by topic.
"""


def schools_by_topic(mongo_collection, topic):
    """
    Returns the list of schools having a specific topic.

    Args:
        mongo_collection (pymongo.collection.Collection): The MongoDB collection.
        topic (str): The topic to search for.

    Returns:
        list: List of schools with the specified topic.
    """
    return list(mongo_collection.find({"topics": topic}))


if __name__ == "__main__":
    from pymongo import MongoClient
    from 9-insert_school import insert_school
    from 8-all import list_all

    client = MongoClient('mongodb://127.0.0.1:27017')
    school_collection = client.my_db.school

    j_schools = [
        { 'name': "Holberton school", 'topics': ["Algo", "C", "Python", "React"]},
        { 'name': "UCSF", 'topics': ["Algo", "MongoDB"]},
        { 'name': "UCLA", 'topics': ["C", "Python"]},
        { 'name': "UCSD", 'topics': ["Cassandra"]},
        { 'name': "Stanford", 'topics': ["C", "React", "Javascript"]}
    ]
    for j_school in j_schools:
        insert_school(school_collection, **j_school)

    schools = schools_by_topic(school_collection, "Python")
    for school in schools:
        print("[{}] {} {}".format(school.get('_id'), school.get('name'), school.get('topics', "")))
