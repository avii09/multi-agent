import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models.database import get_sync_collection, test_connection
from mock_data import *

def seed_database():
    """Populate database with mock data"""
    print("Starting database seeding...")
    
    #test connection
    if not test_connection():
        return False
    
    
    print("Generating mock data...")
    clients = generate_clients(50)
    courses = generate_courses(5)
    classes = generate_classes(25)
    orders = generate_orders(clients, courses, classes, 100)
    payments = generate_payments(orders)
    attendance = generate_attendance(classes, clients)
    
    #insert data into collections
    collections_data = {
        "clients": clients,
        "courses": courses,
        "classes": classes,
        "orders": orders,
        "payments": payments,
        "attendance": attendance
    }
    
    for collection_name, data in collections_data.items():
        if data:
            collection = get_sync_collection(collection_name)
            # clear existing data
            collection.drop()
            # insert new data
            collection.insert_many(data)
            print(f"Inserted {len(data)} records into {collection_name}")
    
    print("Database seeding completed!")
    return True

if __name__ == "__main__":
    seed_database() 
