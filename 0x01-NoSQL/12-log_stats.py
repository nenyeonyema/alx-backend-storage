#!/usr/bin/env python3
"""
Script to provide stats about Nginx logs stored in MongoDB.
"""

from pymongo import MongoClient


def log_stats(mongo_collection):
    """
    Displays stats about Nginx logs stored in MongoDB.

    Args:
        mongo_collection (pymongo.collection.Collection): The MongoDB collection.

    Returns:
        None
    """
    # Count the total number of documents
    total_logs = mongo_collection.count_documents({})

    # Count the number of documents for each method
    methods = ["GET", "POST", "PUT", "PATCH", "DELETE"]
    method_counts = {method: mongo_collection.count_documents({"method": method}) for method in methods}

    # Count the number of documents with method=GET and path=/status
    status_check = mongo_collection.count_documents({"method": "GET", "path": "/status"})

    # Display the stats
    print(f"{total_logs} logs")
    print("Methods:")
    for method, count in method_counts.items():
        print(f"    method {method}: {count}")
    print(f"{status_check} status check")


if __name__ == "__main__":
    client = MongoClient('mongodb://127.0.0.1:27017')
    db = client.logs
    nginx_collection = db.nginx

    log_stats(nginx_collection)
