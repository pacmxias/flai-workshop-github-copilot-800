#!/usr/bin/env python
"""
Verification script to check MongoDB connection and database contents
"""
from pymongo import MongoClient

def verify_database():
    # Connect to MongoDB
    client = MongoClient('localhost', 27017)
    db = client['octofit_db']
    
    print("=" * 60)
    print("OctoFit Database Verification")
    print("=" * 60)
    
    # List all collections
    collections = db.list_collection_names()
    print(f"\nCollections in octofit_db: {collections}")
    
    # Check each collection
    for collection_name in ['users', 'teams', 'activities', 'leaderboard', 'workouts']:
        if collection_name in collections:
            collection = db[collection_name]
            count = collection.count_documents({})
            print(f"\n{collection_name.upper()} Collection:")
            print(f"  Total documents: {count}")
            
            if count > 0:
                print(f"  Sample document:")
                sample = collection.find_one()
                for key, value in sample.items():
                    if key != '_id':
                        print(f"    {key}: {value}")
        else:
            print(f"\n{collection_name.upper()} Collection: NOT FOUND")
    
    print("\n" + "=" * 60)
    print("Verification complete!")
    print("=" * 60)

if __name__ == '__main__':
    verify_database()
